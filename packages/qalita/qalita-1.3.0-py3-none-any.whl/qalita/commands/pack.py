"""
# QALITA (c) COPYRIGHT 2023 - ALL RIGHTS RESERVED -
"""
import click
import json
import os
import sys
import subprocess
import yaml
import logging
import base64
import re
from threading import Thread
from tabulate import tabulate
from qalita.internal.error_patterns import ERROR_PATTERNS
from qalita.cli import pass_config
from qalita.internal.utils import logger, make_tarfile, ask_confirmation
from qalita.internal.request import send_request

loggerPack = logging.getLogger(__name__)


def handle_stderr_line(read):
    """
    Determine the appropriate logging level for a line from stderr.
    Returns a logging level based on the content of the line.
    """
    for pattern, log_level in ERROR_PATTERNS.items():
        if re.search(pattern, read, re.IGNORECASE):
            return log_level
    return "INFO"


def pack_logs(pipe, loggers, error=False):
    while True:
        line = pipe.readline()
        if line:
            line = line.strip()
            if error:
                log_level = handle_stderr_line(line)
                for logger in loggers:
                    if log_level == "INFO":
                        logger.info(line)
                    else:
                        logger.error(line)
                        global has_errors
                        has_errors = True
            else:
                for logger in loggers:
                    logger.info(line)
        else:
            break


def setup_logger(pack_file_path):
    loggerPack.setLevel(logging.INFO)
    # Remove existing file handlers
    for handler in loggerPack.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            loggerPack.removeHandler(handler)

    # Create new log file path
    new_log_file_path = os.path.join(pack_file_path, "logs.txt")

    # Add new file handler
    handler = logging.FileHandler(new_log_file_path)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    loggerPack.addHandler(handler)
    return loggerPack


def run_pack(pack_file_path):
    global has_errors
    has_errors = False
    loggerPack = setup_logger(pack_file_path)
    loggerPack.info("------------- Pack Run -------------")
    logger.info("------------- Pack Run -------------")

    # Check if the run.sh file exists
    run_script = "run.sh"  # Only the script name is needed now
    if not os.path.isfile(os.path.join(pack_file_path, run_script)):
        loggerPack.error(
            f"run.sh script does not exist in the package folder {pack_file_path}"
        )
        return 1

    # Run the run.sh script and get the output
    process = subprocess.Popen(
        ["sh", run_script],
        cwd=pack_file_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    stdout_thread = Thread(
        target=pack_logs, args=(process.stdout, [loggerPack, logger])
    )
    stderr_thread = Thread(
        target=pack_logs, args=(process.stderr, [loggerPack, logger], True)
    )

    stdout_thread.start()
    stderr_thread.start()

    stdout_thread.join()
    stderr_thread.join()

    retcode = process.poll()

    # Decide the return value based on the has_errors flag
    if has_errors:
        loggerPack.error("Pack failed")
        logger.error("Pack failed")
        return 1
    else:
        loggerPack.info("Pack run completed")
        logger.info("Pack run completed")
        return 0


def check_name(name):
    all_check_pass = True
    if not name:
        logger.error("Error: Pack name is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_PACK_NAME='mypack'")
        logger.info("\tor add the name as a commandline argument : ")
        logger.info("\t\tqalita pack --name 'mypack'")
        logger.info(
            "\tthe prefered way is to create a file '.env-local' with the values : "
        )
        logger.info("\t\tQALITA_PACK_NAME=mypack")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-local)")
        all_check_pass = False
    if all_check_pass:
        return name
    else:
        sys.exit(1)


@click.group()
@click.option("-p", "--pack", type=int, help="Pack ID")
@click.pass_context
def pack(ctx, pack):
    """Manage Qalita Platform Packs"""
    ctx.ensure_object(dict)
    ctx.obj["PACK"] = pack


@pack.command()
@pass_config
def list(config):
    """List all available packs"""
    tab_packs = []
    agent_conf = config.load_agent_config()
    headers = ["ID", "Name", "Description"]

    r = send_request(
        request=f"{agent_conf['context']['local']['url']}/packs/1/all",
        mode="get",
    )
    if r.status_code == 200:
        packs = r.json()
        for pack in packs:
            tab_packs.append(
                [
                    pack.get("id", ""),
                    pack.get("name", ""),
                    pack.get("description", ""),
                    pack.get("visibility", ""),
                ]
            )
    elif r.status_code == 404:
        pass
    else:
        logger.error(
            f"Error cannot fetch pack list, make sure you are logged in with > qalita agent login : {r.status_code} - {r.reason}"
        )
        return

    print(tabulate(tab_packs, headers, tablefmt="simple"))


@pass_config
def validate_pack(config, name):
    """Validates pack arborescence, configurations etc...."""
    logger.info("------------- Pack Validation -------------")
    name = check_name(name)
    error_count = 0
    pack_folder = f"{name}_pack"
    if not os.path.exists(pack_folder):
        logger.error(f"Pack folder '{pack_folder}' does not exist.")
        error_count += 1

    mandatory_files = ["run.sh", "properties.yaml", "README.md"]
    for file in mandatory_files:
        file_path = os.path.join(pack_folder, file)
        if not os.path.exists(file_path):
            logger.error(f"Mandatory file '{file}' does not exist in the pack.")
            error_count += 1
        else:
            with open(file_path, "r") as f:
                content = f.read()
                if not content:
                    logger.error(f"File '{file}' is empty.")
                    error_count += 1
                if file == "properties.yaml":
                    properties = yaml.safe_load(content)
                    if "name" not in properties or properties["name"] != name:
                        logger.error(
                            f"Pack name in 'properties.yaml' is not set correctly."
                        )
                        error_count += 1
                    if "version" not in properties:
                        logger.error(f"Version in 'properties.yaml' is not set.")
                        error_count += 1

                    if "type" not in properties:
                        logger.error(f"Type in 'properties.yaml' is not set.")
                        error_count += 1

                    if "visibility" not in properties:
                        logger.warning(
                            f"Visibility in 'properties.yaml' is not set. Defaulting to [Private]"
                        )
                        properties["visibility"] = "private"

        # save file
        if file == "properties.yaml":
            with open(file_path, "w") as f:
                yaml.dump(properties, f)

    if error_count == 0:
        logger.success(f"Pack [{name}] validated.")
    else:
        logger.error(f"{error_count} error(s) found during pack validation.")

    return error_count


@pack.command()
@click.option(
    "-n",
    "--name",
    help="The name of the package, it will be used to identify the package in the Qalita platform",
    envvar="QALITA_PACK_NAME",
)
@pass_config
def validate(config, name):
    """validates pack arborescence, configurations etc...."""
    validate_pack(name)


@pack.command()
@click.option(
    "-n",
    "--name",
    help="The name of the package, it will be used to identify the package in the Qalita platform",
    envvar="QALITA_PACK_NAME",
)
@pass_config
def push(config, name):
    """Pushes a package to the Qalita Platform"""

    agent_conf = config.load_agent_config()

    # Validation of required options
    name = check_name(name)
    if name is not False:
        config.name = name

    error_count = validate_pack(name)
    if error_count > 0:
        logger.error(
            ">> There are errors with your pack, please resolve them before pushing it."
        )
        return

    logger.info("------------- Pack Push -------------")

    with open(f"./{name}_pack/properties.yaml", "r") as file:
        pack_properties = yaml.safe_load(file)

    api_url = agent_conf["context"]["local"]["url"]
    registry_id = agent_conf["registries"]["id"]
    pack_name = pack_properties.get("name")
    pack_version = pack_properties.get("version")
    pack_description = pack_properties.get("description", "")
    pack_type = pack_properties.get("type", "")
    pack_visibility = pack_properties.get("visibility", "private")
    user_id = agent_conf["user"]["id"]

    # check if file exist, and if , get the icon
    pack_icon = pack_properties.get("icon", "")
    if os.path.exists(f"./{name}_pack/icon.png"):
        with open(f"./{name}_pack/icon.png", "rb") as file:
            pack_icon = base64.b64encode(file.read()).decode("utf-8")
    else:
        pack_icon = ""

    # check if file exist, and if , get the readme
    readme = pack_properties.get("icon", "")
    if os.path.exists(f"./{name}_pack/README.md"):
        with open(f"./{name}_pack/README.md", "rb") as file:
            readme = base64.b64encode(file.read()).decode("utf-8")
    else:
        readme = ""

    # check if file pack_conf.json exists
    if os.path.exists(f"./{name}_pack/pack_conf.json"):
        with open(f"./{name}_pack/pack_conf.json", "r") as file:
            pack_config = json.load(file)
    else:
        pack_config = {}

    pack_config_str = json.dumps(pack_config)

    # Check if pack already published
    r = send_request(
        request=f"{api_url}/packs/?name={name}&type={pack_type}&user_id={user_id}",
        mode="get",
    )

    if r.status_code != 404:
        # check Pack versions
        pack_data = r.json()
        for version in pack_data["versions"]:
            if version == pack_version:
                logger.error(
                    f"Pack [{pack_name}] with version [{pack_version}] already exists. You need to increase the version in your [properties.yaml] in order to push the pack"
                )
                sys.exit(1)

        if pack_visibility != pack_data["visibility"]:
            pack_answer = ask_confirmation(
                "Are you sure you want to publish a public pack ? Public packs are made visible for partners. Be carefull about what you share with partners."
            )
            if pack_answer == False:
                sys.exit(1)

    r = send_request(
        request=f"{api_url}/packs/publish",
        mode="post",
        data={
            "name": pack_name.replace("_", " ").replace("-", " "),
            "avatar": pack_icon,
            "user_id": user_id,
            "config": pack_config_str,
            "type": pack_type,
            "description": pack_description,
            "version": pack_version,
            "visibility": pack_visibility,
            "readme": readme,
        },
    )

    if r.status_code == 200:
        logger.success(f"Pack [{pack_name}] published")
    elif r.status_code == 409:
        logger.info(f"Pack [{pack_name}] already exists. Fetching Pack data")
        r = send_request(
            request=f"{api_url}/packs/?name={name}&type={pack_type}&user_id={user_id}",
            mode="get",
        )
        if r.status_code != 200:
            logger.error(
                f"Pack [{pack_name}] could not be fetched. Are you the owner of the pack ? You need to login with the user id that published the pack : \n > qalita agent -n <owner> login"
            )
            sys.exit(1)

    else:
        logger.error(f"Pack [{pack_name}] could not be published.")

    # get data from the pack
    pack_data = r.json()
    pack_id = pack_data["id"]

    # check if pack_version is in pack_data.versions[]
    for version in pack_data["versions"]:
        if pack_version == version["sem_ver_id"]:
            logger.error(
                f"Pack [{pack_name}] with version [{pack_version}] already exist. You need to increase the version in your [properties.yaml] in order to push the pack"
            )
            sys.exit(1)

    logger.info(f"New pack version [{pack_version}] detected. Pushing pack version")

    ################################################################
    # Updating Pack Attributes

    # 1. Match values
    attributes_to_check = [
        ("icon", "avatar"),
        ("config", "config"),
        ("type", "type"),
        ("description", "description"),
        ("visibility", "visibility"),
        ("readme", "readme"),
    ]
    differences_detected = False

    for prop_attribute, backend_attribute in attributes_to_check:
        pack_data_value = pack_data.get(backend_attribute)
        pack_properties_value = pack_properties.get(prop_attribute)

        if pack_data_value != pack_properties_value:
            differences_detected = True
            break

    if pack_visibility != pack_data["visibility"]:
        pack_answer = ask_confirmation(
            "Are you sure you want to publish a public pack ? Public packs are made visible for partners. Be carefull about what you share with partners."
        )
        if pack_answer == False:
            sys.exit(1)

    # 2. Send an update query if there are differences
    if differences_detected:
        r = send_request(
            request=f"{api_url}/packs/{pack_id}",
            mode="put",
            data={
                "avatar": pack_icon,  # Using 'avatar' as the backend expects it
                "config": pack_config_str,
                "type": pack_type,
                "description": pack_description,
                "visibility": pack_visibility,
                "readme": readme,
            },
        )

        if r.status_code == 200:
            logger.success(f"Pack [{pack_name}] updated successfully")
        else:
            logger.error(
                f"Pack [{pack_name}] could not be updated. Error code {r.status_code}"
            )

    ################################################################
    # Pushing asset

    # Create tar.gz archive of directory
    output_filename = f"{name}.tar.gz"
    source_dir = (
        f"./{name}_pack"  # Assuming the directory is in the current working directory
    )
    make_tarfile(output_filename, source_dir)

    # Send the tar.gz file to the server
    r = send_request(
        request=f"{api_url}/assets/{registry_id}/upload",
        mode="post-multipart",
        file_path=output_filename,
        query_params={
            "name": pack_name,
            "bucket": "packs",
            "type": "pack",
            "version": pack_version,
            "description": pack_description,
            "visibility": pack_visibility,
            "user_id": user_id,
        },
    )

    if r.status_code == 200:
        asset_data = r.json()
        logger.success("Pack asset uploaded")

        # add pack_version
        r = send_request(
            request=f"{api_url}/packs/{pack_id}/version",
            mode="put",
            query_params={
                "sem_ver_id": pack_version,
                "asset_id": asset_data["id"],
            },
        )
        if r.status_code == 200:
            logger.success(f"Pack pushed !")

    elif r.status_code == 404:
        logger.info("No registry")
        sys.exit(1)
    elif r.status_code == 409:
        logger.info("Pack asset already uploaded")
        sys.exit(1)
    else:
        logger.error(
            f"Failed pushing the pack - HTTP Code : {r.status_code} - {r.text}"
        )

    # remove the file
    if os.path.exists(output_filename):
        os.remove(output_filename)


@pack.command()
@click.option(
    "-n",
    "--name",
    help="The name of the package, it will be used to identify the package in the Qalita platform",
    envvar="QALITA_PACK_NAME",
)
def run(name):
    """Dry run a pack"""
    # Validation of required options
    all_check_pass = True
    if not name:
        logger.error("Error: Pack name is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_PACK_NAME='mypack'")
        logger.info("\tor add the name as a commandline argument : ")
        logger.info("\t\tqalita pack --name 'mypack'")
        logger.info(
            "\tthe prefered way is to create a file '.env-local' with the values : "
        )
        logger.info("\t\tQALITA_PACK_NAME=mypack")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-local)")
        all_check_pass = False
    if not all_check_pass:
        return

    # Check if the pack folder exists
    pack_folder = os.path.join(os.getcwd(), name) + "_pack"
    if not os.path.exists(pack_folder):
        logger.error(f"Package folder {pack_folder} does not exist")
        return

    # Check if the run.sh file exists
    run_script = "run.sh"  # Only the script name is needed now
    if not os.path.isfile(os.path.join(pack_folder, run_script)):
        logger.error(
            f"run.sh script does not exist in the package folder {pack_folder}"
        )
        return

    status = run_pack(pack_folder)

    if status == 0:
        logger.success("Pack Run Success")
    else:
        logger.error("Pack Run Failed")


@pack.command()
@click.option(
    "-n",
    "--name",
    help="The name of the package, it will be used to identify the package in the Qalita platform",
    envvar="QALITA_PACK_NAME",
)
@pass_config
def init(config, name):
    """Initialize a pack"""
    # Validation of required options
    all_check_pass = True
    if not name:
        logger.error("Error: Pack name is required!")
        logger.info("\tTo do so, you can set an Environment Variable : ")
        logger.info("\t\texport QALITA_PACK_NAME='mypack'")
        logger.info("\tor add the name as a commandline argument : ")
        logger.info("\t\tqalita pack --name 'mypack'")
        logger.info(
            "\tthe prefered way is to create a file '.env-local' with the values : "
        )
        logger.info("\t\tQALITA_PACK_NAME=mypack")
        logger.info("\tand source it : ")
        logger.info("\t\texport $(xargs < .env-local)")
        all_check_pass = False
    if all_check_pass:
        config.name = name
    else:
        return

    """Initialize a package"""
    package_folder = name + "_pack"
    package_yaml = "properties.yaml"
    package_json = "pack_conf.json"
    package_py = "main.py"
    package_sh = "run.sh"
    package_requirements = "requirements.txt"
    package_readme = "README.md"

    # Check if the package folder already exists
    if os.path.exists(package_folder):
        logger.warning(f"Package folder '{package_folder}' already exists")
    else:
        # Create a package folder
        os.makedirs(package_folder)
        logger.info(f"Created package folder: {package_folder}")

    # Check if the file already exists
    if os.path.exists(os.path.join(package_folder, package_yaml)):
        logger.warning(f"Package file '{package_yaml}' already exists")
    else:
        # Create a file
        with open(os.path.join(package_folder, package_yaml), "w") as file:
            file.write(
                f'name: {name}\nversion: "1.0.0"\ndescription: "default template pack"\nvisibility: private\ntype: "pack"'
            )
        logger.info(f"Created file: {package_yaml}")

    # Check if the file already exists
    if os.path.exists(os.path.join(package_folder, package_json)):
        logger.warning(f"Package file '{package_json}' already exists")
    else:
        # Create a file
        with open(os.path.join(package_folder, package_json), "w") as file:
            json_data = {"name": name, "version": "1.0.0"}
            file.write(json.dumps(json_data, indent=4))
        logger.info(f"Created file: {package_json}")

    # Check if the file already exists
    if os.path.exists(os.path.join(package_folder, package_py)):
        logger.warning(f"Package file '{package_py}' already exists")
    else:
        # Create a file
        with open(os.path.join(package_folder, package_py), "w") as file:
            file.write("# Python package code goes here\n")
            file.write(
                "print('hello world ! This is a script executed by a pack ! Do whatever process you want to check your data quality, happy coding ;)')"
            )
        logger.info(f"Created file: {package_py}")
        logger.warning("Please update the main.py file with the required code")

    # Check if the file already exists
    if os.path.exists(os.path.join(package_folder, package_sh)):
        logger.warning(f"Package file '{package_sh}' already exists")
    else:
        # Create a file
        with open(os.path.join(package_folder, package_sh), "w") as file:
            file.write("#/bin/bash\n")
            file.write("python -m pip install -r requirements.txt\n")
            file.write("python main.py")
        logger.info(f"Created file: {package_sh}")
        logger.warning("Please update the run.sh file with the required commands")

    if os.path.exists(os.path.join(package_folder, package_requirements)):
        logger.warning(f"Package file '{package_requirements}' already exists")
    else:
        # Create a file
        with open(os.path.join(package_folder, package_requirements), "w") as file:
            file.write("numpy")
        logger.info(f"Created file: {package_requirements}")
        logger.warning(
            "Please update the requirements.txt file with the required packages depdencies"
        )

    if os.path.exists(os.path.join(package_folder, package_readme)):
        logger.warning(f"Package file '{package_readme}' already exists")
    else:
        # Define content
        readme_content = """# Package

## Description of a pack

### Pack content

A pack is composed of different files :

### Mandatory files

- `run.sh` : the script to run the pack
- `properties.yaml` : the pack properties file
- `README.md` : this file

### Optional files

- `pack_conf.json` : the configuration file for the runtime program
- `requirements.txt` : the requirements file for the runtime program
"""

        # Create the file
        with open(os.path.join(package_folder, package_readme), "w") as file:
            file.write(readme_content)
        logger.info(f"Created file: {package_readme}")
        logger.warning(
            "Please READ and update the README.md file with the description of your pack"
        )

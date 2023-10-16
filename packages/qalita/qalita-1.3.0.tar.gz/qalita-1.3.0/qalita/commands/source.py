"""
# QALITA (c) COPYRIGHT 2023 - ALL RIGHTS RESERVED -
"""
import os
import click
from tabulate import tabulate

from qalita.cli import pass_config
from qalita.internal.utils import logger, ask_confirmation
from qalita.internal.request import send_api_request


@click.group()
@click.option("-s", "--source", type=int, help="Source ID")
@click.pass_context
def source(ctx, source):
    """Manage Qalita Platform Sources"""
    ctx.ensure_object(dict)
    ctx.obj["SOURCE"] = source


@source.command()
@pass_config
def list(config):
    """List sources that are accessible to the agent"""
    config.load_source_config()

    sources = []
    headers = [
        "ID",
        "Name",
        "Type",
        "Reference",
        "Sensitive",
        "Visibility",
        "Description",
        "Validity",
    ]

    for source in config.config["sources"]:
        sources.append(
            [
                source.get("id", ""),
                source.get("name", ""),
                source.get("type", ""),
                source.get("reference", ""),
                source.get("sensitive", ""),
                source.get("visibility", ""),
                source.get("description", ""),
                source.get("validate", ""),
            ]
        )

    print(tabulate(sources, headers, tablefmt="simple"))


def source_version(source):
    """Determine the source version"""
    # La version de la source est déterminée en fonction de sa typologie,
    # Si la source est d'une version non gérée, elle aura la version 1.0.0

    version = "1.0.0"
    return version


@pass_config
def validate_source(config):
    """Validate a source configuration"""
    logger.info("------------- Source Validation -------------")
    config.load_source_config()
    agent_conf = config.load_agent_config()

    total_sources = 0
    error_count = 0

    source_names = []

    for i, source in enumerate(config.config["sources"]):
        total_sources += 1
        is_source_valid = True  # Assuming the source is valid initially

        # check for name
        if "name" not in source:
            logger.error(f"Source number [{total_sources}] has no name")
            is_source_valid = False
            return 1

        # check for type
        if "type" not in source:
            logger.error(f"Source number [{total_sources}] has no type")
            is_source_valid = False
            return 1

        # Check for duplicate names
        if source["name"] in source_names:
            logger.error(f"Duplicate source name: [{source['name']}]")
            is_source_valid = False
        else:
            source_names.append(source["name"])

        # check for description
        if "description" not in source:
            logger.warning(
                f"Source [{source['name']}] has no description, defaulting to empty string"
            )
            config.config["sources"][i]["description"] = ""

        # check for reference
        if "reference" not in source:
            logger.warning(
                f"Source [{source['name']}] has no reference status, defaulting to False"
            )
            config.config["sources"][i]["reference"] = False

        # check for Sensitive
        if "sensitive" not in source:
            logger.warning(
                f"Source [{source['name']}] has no sensitive status, defaulting to False"
            )
            config.config["sources"][i]["sensitive"] = False

        # check for visibility
        if "visibility" not in source:
            logger.warning(
                f"Source [{source['name']}] has no visibility status, defaulting to private"
            )
            config.config["sources"][i]["visibility"] = "private"

        # check for owner
        if "owner" not in source:
            logger.warning(
                f"Source [{source['name']}] must have a owner, if you publish without owner, it will be published under your name"
            )
            logger.warning(
                f"Source [{source['name']}] defaulting to owner: {agent_conf['user']['login']}"
            )
            source["owner"] = agent_conf["user"]["login"]
            source["owner_id"] = agent_conf["user"]["id"]

        # check type
        if source["type"] == "database":
            if "config" in source:
                for key, value in source["config"].items():
                    # If the value starts with '$', assume it's an environment variable
                    if str(value).startswith("$"):
                        env_var = value[1:]
                        # Get the value of the environment variable
                        env_value = os.getenv(env_var)
                        if env_value is None:
                            logger.warning(
                                f"The environment variable [{env_var}] for the source [{source['name']}] is not set"
                            )
                            is_source_valid = False
        elif source["type"] == "file":
            # check if config parameter is present
            if "config" not in source:
                logger.error(
                    f"Source [{source['name']}] is of type file but has no config"
                )
                is_source_valid = False
            else:
                # check for path in config
                if "path" not in source["config"]:
                    logger.error(
                        f"Source [{source['name']}] is of type file but has no path in config"
                    )
                    is_source_valid = False
                else:
                    # check for read access to path
                    path = source["config"]["path"]
                    if not os.access(path, os.R_OK):
                        logger.error(
                            f"Source [{source['name']}] has a path in config, but it cannot be accessed"
                        )
                        is_source_valid = False

        # If all checks pass, mark the source as valid
        if is_source_valid:
            source["validate"] = "valid"
            logger.success(f"Source [{source['name']}] validated")
        else:
            source["validate"] = "invalid"
            logger.error(f"Source [{source['name']}] is invalid")
            error_count += 1

    if error_count == 0:
        logger.success("All sources validated")
    else:
        logger.error(f"{error_count} out of {total_sources} sources are invalid")

    # Write the config file
    config.save_source_config()


@source.command()
def validate():
    """Validate a source configuration"""
    validate_source()


@source.command()
@pass_config
def push(config):
    """Publish a source to the Qalita Platform"""
    validate_source()
    logger.info("------------- Source Publishing -------------")
    logger.info("Publishing sources to the Qalita Platform...")
    invalid_count = 0  # to count failed publishing sources
    agent_conf = config.load_agent_config()
    config.load_source_config()

    if len(config.config["sources"]) == 0:
        logger.warning("No sources to publish, add new sources > qalita source add")
        return

    valid_source = 0
    # count number of valid sources
    for source in config.config["sources"]:
        if source["validate"] == "valid":
            valid_source += 1

    if valid_source == 0:
        logger.warning("No valid sources to publish")
        return

    for i, source in enumerate(config.config["sources"]):
        if source["validate"] == "valid":
            if "id" in source:
                # Try to get source info from name, type and owner_id
                r = send_api_request(
                    request="/sources/",
                    mode="get",
                    query_params={
                        "name": source["name"],
                        "type": source["type"],
                        "user_id": source["owner_id"],
                    },
                )

                if r.status_code == 200:
                    # On essaye de matcher les valeurs
                    response_data = r.json()

                    # Check if name, type and user_id match with the response data
                    if (
                        source["name"] == response_data["name"]
                        and source["type"] == response_data["type"]
                        and source["owner_id"] == response_data["user_id"]
                    ):
                        # If they match, this source is already published, skip to the next source
                        update_source = False
                        if response_data["versions"] != []:
                            if (
                                source_version(source)
                                == response_data["versions"][0]["sem_ver_id"]
                            ):
                                if (
                                    (
                                        source["visibility"]
                                        == response_data["visibility"]
                                    )
                                    and (
                                        source["description"]
                                        == response_data["description"]
                                    )
                                    and (
                                        source["sensitive"]
                                        == response_data["sensitive"]
                                    )
                                    and (
                                        source["reference"]
                                        == response_data["reference"]
                                    )
                                ):
                                    logger.info(
                                        f"Source [{source['name']}] already published with id [{source['id']}] and no updates detected. Skipping..."
                                    )
                                else:
                                    update_source = True
                            else:
                                logger.info("Version mismatch")
                                update_source = True
                        else:
                            logger.info("No version")
                            update_source = True

                        if update_source:
                            if source["visibility"] != response_data["visibility"]:
                                if (
                                    ask_confirmation(
                                        "Are you sure you want to publish a public source ? Public sources are made visible for partners. Be carefull about what you share with partners."
                                    )
                                    == False
                                ):
                                    continue

                            r = send_api_request(
                                request=f"/sources/{response_data['id']}",
                                mode="put",
                                query_params={
                                    "description": source["description"],
                                    "visibility": source["visibility"],
                                    "sensitive": source["sensitive"],
                                    "reference": source["reference"],
                                },
                            )
                            logger.success(f"Source [{source['name']}] updated")
                            continue
                        else:
                            continue

            logger.info(f"Publishing source [{source['name']}] ...")

            if source["visibility"] == "public":
                if (
                    ask_confirmation(
                        "Are you sure you want to publish a public source ? Public sources are made visible for partners. Be carefull about what you share with partners."
                    )
                    == False
                ):
                    continue

            # send the request to the Qalita Platform
            r = send_api_request(
                request=f"/sources/publish",
                mode="post",
                query_params={
                    "name": source["name"],
                    "type": source["type"],
                    "description": source["description"],
                    "reference": source["reference"],
                    "sensitive": source["sensitive"],
                    "visibility": source["visibility"],
                    "user_id": source["owner_id"],
                    "version": source_version(source),
                },
            )
            if r.status_code != 200:
                logger.warning(
                    f"Agent failed to publish source [{source['name']}] {r.status_code} - {r.text}"
                )
                if source["owner_id"] != agent_conf["user"]["id"]:
                    logger.error(
                        f"Agent cannot publish source [{source['name']}] because it is not the owner"
                    )
                    logger.error(
                        f"Owner id of the source : {source['owner_id']}, id of the agent : {agent_conf['user']['id']}"
                    )
                invalid_count += 1
            else:
                source_id = r.json()["id"]
                logger.success(f"Source published with id [{source_id}]")
                # Add the id to the corresponding source in config.config["sources"]
                config.config["sources"][i]["id"] = source_id
                # Save the updated configuration
                config.save_source_config()

    # after all sources have been processed, print a warning if there were any invalid sources
    if invalid_count > 0:
        logger.warning(f"{invalid_count} source(s) skipped due to validation errors.")


@source.command()
@pass_config
def add(config):
    """Add a source to the local Qalita Config"""

    # initialize the source dict
    source = {}

    # hardcode empty source config
    source["config"] = {}

    # ask for the source name
    source["name"] = click.prompt("Source name")

    # ask for the source type
    source["type"] = click.prompt(
        "Source type",
        type=click.Choice(["file", "database", "image", "..."], case_sensitive=False),
    )

    # if the source type is file, ask for the file path
    if source["type"] == "file":
        source["config"]["path"] = click.prompt("Source path")
    elif source["type"] == "database":
        source["config"]["host"] = click.prompt("Source host")
        source["config"]["port"] = click.prompt("Source port")
        source["config"]["username"] = click.prompt("Source username")
        source["config"]["password"] = click.prompt("Source password")
        source["config"]["database"] = click.prompt("Source database")

    # ask for the source description
    source["description"] = click.prompt("Source description")
    # ask for the source reference
    source["reference"] = click.prompt("Source reference", type=bool, default=False)
    # ask for the source sensitive
    source["sensitive"] = click.prompt("Source sensitive", type=bool, default=False)
    # ask for the source visibility
    source["visibility"] = click.prompt(
        "Source visibility",
        default="private",
        type=click.Choice(["private", "internal", "public"], case_sensitive=False),
    )

    config.load_source_config()
    if len(config.config["sources"]) > 0:
        # check if the source already exists
        for conf_source in config.config["sources"]:
            if conf_source["name"] == source["name"]:
                logger.error("Source already exists in config")
                return

    # add the source to the config
    config.config["sources"].append(
        {
            "name": source["name"],
            "config": source["config"],
            "type": source["type"],
            "description": source["description"],
            "reference": source["reference"],
            "sensitive": source["sensitive"],
            "visibility": source["visibility"],
        }
    )

    # save the config
    config.save_source_config()
    logger.success(f"Source [{source['name']}] added to the local config")

    validate_source()

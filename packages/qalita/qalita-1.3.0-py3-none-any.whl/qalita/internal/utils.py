"""
# QALITA (c) COPYRIGHT 2023 - ALL RIGHTS RESERVED -
"""
from qalita.internal.logger import init_logging
import tarfile
import os
import click

logger = init_logging()


def get_version():
    return "1.3.0"


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def ask_confirmation(message):
    """This function just asks for confirmation interactively from the user"""
    return click.confirm(message, default=False)

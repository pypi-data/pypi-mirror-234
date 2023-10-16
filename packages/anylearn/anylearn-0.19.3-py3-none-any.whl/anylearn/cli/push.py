import click
from requests import HTTPError
from typing import Optional

from anylearn.applications.algorithm_manager import sync_algorithm
from anylearn.cli.anylearn_cli_config import AnylearnCliConfig
from anylearn.cli.utils import (
    check_config,
    check_connection,
    cmd_confirm_or_abort,
    cmd_error,
    cmd_info,
    cmd_success,
    cmd_warning,
    get_cmd_command,
)
from anylearn.interfaces import Algorithm, Dataset, Project
from anylearn.interfaces.resource import SyncResourceUploader
from anylearn.utils.errors import AnylearnRequiredLocalCommitException


_option_force = click.option(
    '-f', '--force',
    is_flag=True,
    default=False,
    help="Skip prompt and force actions."
)


@click.group("push")
def commands():
    """
    Push local project or algorithm(s) or dataset(s) to remote Anylearn.
    """
    pass


@commands.command()
@click.argument('name')
@_option_force
@check_config()
@check_connection()
@get_cmd_command()
def algorithm(name :str, force: bool=False, async_upload: bool=False):
    """
    Create/update and/or upload local algorithm to remote Anylearn.
    """
    config = AnylearnCliConfig.load()
    try:
        algo = config.algorithms[name]
        dir = config.path['algorithm'][name]
        img = config.images[name]
    except KeyError:
        cmd_error(msg=(
            f"Algorithm named {name} or its path config does not exist."
        ))
        raise click.Abort
    uploader = SyncResourceUploader()
    algo = _push_1_algorithm(
        algorithm=algo,
        dir=dir,
        image=img,
        force=force,
    )
    config.algorithms[name] = algo
    AnylearnCliConfig.update(config)
    cmd_success(msg="PUSHED")


def _push_1_algorithm(
    algorithm: Algorithm,
    dir: Optional[str]=None,
    image: Optional[str]='QUICKSTART',
    force: bool=False,
    uploader=None,
    polling=5,
) -> Algorithm:
    if dir:
        return __push_local_algorithm(
            algorithm=algorithm,
            dir=dir,
            image=image,
            force=force,
        )
    else:
        return __push_remote_algorithm(
            algorithm=algorithm,
            force=force,
        )


def __push_local_algorithm(
    algorithm: Algorithm,
    dir: str,
    image: str,
    force: bool=False,
):
    try:
        algo, _ = sync_algorithm(
            name=algorithm.name,
            dir_path=dir,
            mirror_name=image,
            force=False,
        )
        return algo
    except AnylearnRequiredLocalCommitException as e:
        cmd_warning(msg=(
            f"Algorithm dir {dir} is not clean, commit required. "
            "Anylearn can make an auto-commit in this case "
            "(or you can cancel the operation and "
            "commit your changes yourself)."
        ))
        if not force:
            cmd_confirm_or_abort()
        algo, _ = sync_algorithm(
            name=algorithm.name,
            dir_path=dir,
            mirror_name=image,
            force=True,
        )
        return algo


def __push_remote_algorithm(algorithm: Algorithm, force: bool=False):
    try:
        remote_algo = Algorithm(id=algorithm.id, load_detail=True)
        if remote_algo == algorithm:
            cmd_info(msg="Metadata already up-to-date.")
        else:
            cmd_warning(msg=(
                "Remote algorithm "
                "("
                f"id={remote_algo.id}, "
                f"name={remote_algo.name}"
                ") will be overridden."
            ))
            if not force:
                cmd_confirm_or_abort()
            algorithm.save()
    except HTTPError:
        cmd_error(msg=(
            "Remote algorithm "
            "("
            f"id={algorithm.id}, "
            f"name={algorithm.name}"
            ") is unaccessible."
        ))
        raise click.Abort
    return algorithm

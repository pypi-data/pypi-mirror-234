"""
functions for executing commands and querying environment in the linux shell
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Optional, Tuple, Union

import typer

from .globals import Architecture
from .logging import log

EC_EPICS_DOMAIN = os.environ.get("EC_EPICS_DOMAIN") or os.environ.get("BEAMLINE")
EC_GIT_ORG = os.environ.get("EC_GIT_ORG")
EC_DOMAIN_REPO = os.environ.get("EC_DOMAIN_REPO", f"{EC_GIT_ORG}/{EC_EPICS_DOMAIN}")
EC_REGISTRY_MAPPING = os.environ.get(
    "EC_REGISTRY_MAPPING",
    "github.com=ghcr.io gitlab.diamond.ac.uk=gcr.io/diamond-privreg/controls/ioc",
)
EC_K8S_NAMESPACE = os.environ.get("EC_K8S_NAMESPACE", EC_EPICS_DOMAIN)
EC_LOG_URL = os.environ.get("EC_LOG_URL", None)
EC_CONTAINER_CLI = os.environ.get("EC_CONTAINER_CLI")  # default to auto choice


def run_command(command: str, interactive=True, error_OK=False) -> Union[str, bool]:
    """
    Run a command and return the output

    if interactive is true then allow stdin and stdout, return the return code,
    otherwise return True for success and False for failure
    """
    log.debug(
        f"running command:\n   {command}\n   "
        f"(interactive={interactive}, error_OK={error_OK})\n"
    )

    p_result = subprocess.run(command, capture_output=not interactive, shell=True)

    output = "" if interactive else p_result.stdout.decode() + p_result.stderr.decode()

    if p_result.returncode != 0 and not error_OK:
        log.error(f"Command Failed:\n{output}")
        raise typer.Exit(1)

    if interactive:
        result: Union[str, bool] = p_result.returncode == 0
    else:
        result = p_result.stdout.decode() + p_result.stderr.decode()
    log.debug(f"returning: {result}")
    return result


def check_ioc(ioc_name: str, domain: str):
    cmd = f"kubectl get -n {domain} deploy/{ioc_name}"
    if not run_command(cmd, interactive=False, error_OK=True):
        log.error(f"ioc {ioc_name} does not exist in domain {domain}")
        raise typer.Exit(1)


def check_domain(domain: Optional[str]):
    """
    Verify we have a good domain that exists in the cluster
    """
    if domain is None:
        log.error("Please set EC_EPICS_DOMAIN or pass --domain")
        raise typer.Exit(1)

    cmd = f"kubectl get namespace {domain} -o name"
    if not run_command(cmd, interactive=False, error_OK=True):
        log.error(f"domain {domain} does not exist")
        raise typer.Exit(1)

    log.info("domain = %s", domain)


def get_image_name(
    repo: str, arch: Architecture = Architecture.linux, target: str = "developer"
) -> str:
    registry = repo2registry(repo).lower().removesuffix(".git")

    image = f"{registry}-{arch}-{target}"
    log.info("repo = %s image  = %s", repo, image)
    return image


def get_git_name(folder: Path = Path(".")) -> Tuple[str, Path]:
    """
    work out the git repo name and top level folder for a local clone
    """
    os.chdir(folder)
    path = str(run_command("git rev-parse --show-toplevel", interactive=False))
    git_root = Path(path.strip())

    remotes = str(run_command("git remote -v", interactive=False))
    log.debug(f"remotes = {remotes}")

    matches = re.findall(r"((?:(?:git@)|(?:http[s]+:\/\/)).*) (?:.fetch.)", remotes)

    if len(matches) > 0:
        repo_name = str(matches[0])
    else:
        log.error(f"folder {folder.absolute()} cannot parse repo name {remotes}")
        raise typer.Exit(1)

    log.debug(f"repo_name = {repo_name}, git_root = {git_root}")
    return repo_name, git_root


# work out what the registry name is for a given repo remote e.g.
def repo2registry(repo_name: str) -> str:
    """convert a repo name to the related a container registry name"""

    log.debug("extracting fields from repo name %s", repo_name)

    match_git = re.match(r"git@([^:]*):(.*)\/(.*)(?:.git)", repo_name)
    match_http = re.match(r"https:\/\/([^\/]*)\/([^\/]*)\/([^\/]*)", repo_name)
    for match in [match_git, match_http]:
        if match is not None:
            source_reg, org, repo = match.groups()
            break
    else:
        log.error(f"repo {repo_name} is not a valid git remote")
        raise typer.Exit(1)

    log.debug("source_reg = %s org = %s repo = %s", source_reg, org, repo)

    if not EC_REGISTRY_MAPPING:
        log.error("environment variable EC_REGISTRY_MAPPING not set")
        raise typer.Exit(1)

    for mapping in EC_REGISTRY_MAPPING.split():
        if mapping.split("=")[0] == source_reg:
            registry = mapping.split("=")[1]
            registry = f"{registry}/{org}/{repo}"
            break
    else:
        log.error(f"repo {repo_name} does not match any registry mapping")
        log.error("please update the environment variable EC_REGISTRY_MAPPING")
        raise typer.Exit(1)

    return registry

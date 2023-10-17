import datetime
import re
import json
from typing import Union
from ..types import Setup, Project, Config, ConfigWithMeta
from .project import get_project, PROJECT_DIR
from ..error import NimuException


def save_config(setup: Setup, number: int, version: int, data: Config) -> Project:
    """
    Overwrite the configuration for the project.
    """
    project = get_project(setup, number)
    dir = setup["workdir"] / PROJECT_DIR / project["info"]["name"]
    if not dir.exists():
        raise NimuException(f"Bad project number {number}")
    (dir / f'version-{version}.json').write_text(json.dumps(data) + '\n')
    return project


def all_configurations(setup: Setup, number: int, with_meta: bool = False) -> Union[Config, ConfigWithMeta]:
    """
    Collect configuration versions for one project.
    """
    project = get_project(setup, number)
    dir = setup["workdir"] / PROJECT_DIR / project["info"]["name"]
    versions = []
    for json_path in dir.glob("version-*.json"):
        config = json.loads(json_path.read_text())
        if with_meta:
            created = json_path.stat().st_ctime
            version = re.match("version-([0-9]+).json", f"{json_path.name}")
            versions.append({
                "id": number,
                "project": project["info"]["name"],
                "version": int(version.group(1)),
                "config": config,
                "created": datetime.datetime.fromtimestamp(created).isoformat()
            })
        else:
            versions.append(config)
    return versions


def create_version(setup: Setup, number: int, conf: Config) -> Project:
    """
    Create new version of the configurations for the project.
    """
    version = len(all_configurations(setup, number)) + 1
    project = save_config(setup, number, version, conf)
    project["versions"] = version
    return project


def get_configuration(setup: Setup, number: int, version: int) -> Config:
    """
    Read the given configuration version.
    """
    project = get_project(setup, number)
    json_path = (setup["workdir"] / PROJECT_DIR / project["info"]["name"] /
                 f"version-{version}.json")
    return json.loads(json_path.read_text())

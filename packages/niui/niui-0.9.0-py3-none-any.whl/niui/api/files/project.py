import datetime
import json
from pathlib import Path
from typing import List
from ..types import Setup, ProjectInfo, Project
from ..error import NimuException


# Project version format.
VERSION = 1
# Name of the project directoru.
PROJECT_DIR = 'Projects'


def project_count(setup: Setup) -> int:
    """
    Count number of configuration projects.
    """
    return len(all_projects(setup))


def project_dir(setup: Setup, name: str) -> Path:
    """
    Ensure project directory exist creating if needed and return it.
    """
    path = setup["workdir"] / PROJECT_DIR / f'{name}'
    if not path.exists():
        path.mkdir(parents=True)
    return path


def allocate(setup: Setup, name: str) -> ProjectInfo:
    """
    Allocate new workdir subdir for file storage.
    """
    n = project_count(setup) + 1
    dir = project_dir(setup, name)
    stamp = datetime.datetime.now().isoformat()
    info = {
        "id": n,
        "version": VERSION,
        "created": stamp,
        "updated": stamp,
        "name": name,
    }
    (dir / 'nimu-project.json').write_text(json.dumps(info) + '\n')
    return info


def all_projects(setup: Setup) -> List[ProjectInfo]:
    """
    Gather info about all allocated configuration projects.
    """
    projects = []
    for dir in (setup["workdir"] / PROJECT_DIR).glob('*'):
        info_path = dir / 'nimu-project.json'
        if info_path.exists():
            info = json.loads(info_path.read_text())
            projects.append(info)
    return projects


def get_project(setup: Setup, number: int) -> Project:
    """
    Collect data for one project.
    """
    projects = list(filter(lambda p: p["id"] == number, all_projects(setup)))
    if len(projects):
        dir = setup["workdir"] / PROJECT_DIR / projects[0]["name"]
    else:
        raise NimuException(f"Bad project number {number}")
    info = json.loads((dir / 'nimu-project.json').read_text())
    return {
        "info": info
    }

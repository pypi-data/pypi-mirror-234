"""
API for accessing and storing the projects.
"""
from ..files.project import allocate, all_projects, get_project
from ..files.config import all_configurations
from ..types import Setup, Project, ProjectInfo
from typing import List


def index(setup: Setup) -> List[ProjectInfo]:
    index = all_projects(setup)
    index.sort(key=lambda item: -item["id"])
    return index


def create(setup: Setup, conf: ProjectInfo) -> ProjectInfo:
    return allocate(setup, conf['name'])


def get(setup: Setup, id: int) -> Project:
    project = get_project(setup, id)
    all = all_configurations(setup, id)
    project["versions"] = len(all)
    return project

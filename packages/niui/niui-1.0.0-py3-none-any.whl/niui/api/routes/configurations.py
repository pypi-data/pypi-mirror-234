"""
API for accessing and storing the configurations.
"""
from ..files.json import all_items
from ..files.config import create_version, all_configurations, save_config, get_configuration
from ..types import Setup, Config, Project, ConfigWithMeta
from ..can.read import fetch_config
from ..can.write import write_config
from typing import List


def index(setup: Setup, id: int) -> List[ConfigWithMeta]:
    all = all_configurations(setup, id, with_meta=True)
    all.sort(key=lambda item: -item["version"])
    return all


def create(setup: Setup, id: int, conf: Config) -> Project:
    return create_version(setup, id, conf)


def get(setup: Setup, id: int, version: int) -> Config:
    return get_configuration(setup, id, version)


def scan(setup: Setup, box_id: int, item_ids: List[int]):
    items = all_items(setup)
    return fetch_config(setup, items, box_id, item_ids)


def write(setup: Setup, box_id: int, config: Config):
    items = all_items(setup)
    return write_config(setup, items, box_id, config)


def update(setup: Setup, id: int, version: int, data: Config) -> Config:
    save_config(setup, id, version, data)
    return data

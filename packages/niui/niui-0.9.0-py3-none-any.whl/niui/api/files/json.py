import json
from pathlib import Path
from typing import Any, List, Dict
from ..types import Setup
from ..data import Item, ItemData, ItemDescription, DataMapping

IGNORE_DIRS = set(['.git', 'node_modules', '.cache'])
IGNORE_FILES = set(['tsconfig.json', 'package.json'])


def read_json(path: Path) -> Dict[str, Any]:
    """
    Read and parse named configuration description.
    """
    try:
        data = path.read_text()
        parsed = json.loads(data)
    except json.decoder.JSONDecodeError:
        parsed = {}
    except UnicodeDecodeError:
        parsed = {}
    except PermissionError:
        parsed = {}
    except IsADirectoryError:
        parsed = {}
    return parsed


def is_valid_json_file(path: Path) -> bool:
    """
    Check if the JSON file is our configuration file.
    """
    if path.name in IGNORE_FILES:
        return False
    content = read_json(path)
    try:
        return "datamappings" in content and "items" in content
    except TypeError:
        return False


def find_json_files(path: Path) -> List[Path]:
    """
    Scan for all valid JSON files from the given directory.
    """
    if not path.exists():
        path.mkdir(parents=True)
    json_files = list(filter(lambda f: is_valid_json_file(f), path.glob('*.json')))
    try:
        for dir in [p for p in path.iterdir() if p.is_dir()]:
            if dir.name not in IGNORE_DIRS:
                json_files += find_json_files(dir)
    except PermissionError:
        pass

    return json_files


def all_items(setup: Setup) -> Dict[int, Item]:
    """
    Gather all configuration items from JSON files.
    """
    datamappings = dict()
    for file_path in setup.get('json_files'):
        json = read_json(file_path)
        for mapping in json.get('datamappings'):
            data = DataMapping(**mapping)
            datamappings[data.name] = data

    items = dict()
    for file_path in setup.get('json_files'):
        json = read_json(file_path)
        for item in json.get('items', []):
            item['data'] = ItemData(**item['data'])
            item['description'] = ItemDescription(**item['description'])
            data = Item(**item)
            if data.type in datamappings:
                data.mapping = datamappings[data.type]
            items[data.id] = data

    return items

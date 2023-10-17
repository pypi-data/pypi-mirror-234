"""
Firmware storage.
"""
import datetime
import json
from pathlib import Path
from typing import List
from ..types import Setup, FirmwareInfo


FIRMWARE_DIR = "Firmwares"


def all_firmwares(setup: Setup) -> List[FirmwareInfo]:
    """
    Gather info about all uploaded firmwares.
    """
    firmwares = []
    for dir in (setup["workdir"] / FIRMWARE_DIR).glob('[0-9]*'):
        info_path = dir / 'firmware.json'
        if info_path.exists():
            info = json.loads(info_path.read_text())
            firmwares.append(info)
    return firmwares


def firmware_count(setup: Setup) -> int:
    """
    Count number of firmwares.
    """
    return len(all_firmwares(setup))


def firmware_dir(setup: Setup, number: str) -> Path:
    """
    Ensure firmware directory exist creating if needed and return it.
    """
    path = setup["workdir"] / FIRMWARE_DIR / f'{number}'
    if not path.exists():
        path.mkdir(parents=True)
    return path


def create_firmware(setup: Setup) -> int:
    """
    Allocate directory for new firmware.
    """
    id = firmware_count(setup) + 1
    dir = firmware_dir(setup, f'{id}')
    stamp = datetime.datetime.now().isoformat()
    info = {
        "id": id,
        "version": 1,
        "created": stamp,
        "files": [],
    }
    (dir / 'firmware.json').write_text(json.dumps(info) + '\n')
    return id


def save_firmware(setup: Setup, id: int, name: str, data: bytearray) -> None:
    """
    Ensure firmware storage directory and store a firmware.
    """
    stamp = datetime.datetime.now().isoformat()
    dir = firmware_dir(setup, f'{id}')
    info = get_firmware(setup, id)
    info['files'].append({
        'created': stamp,
        'name': name,
        'size': len(data)
    })
    (dir / 'firmware.json').write_text(json.dumps(info) + '\n')
    (dir / name).write_bytes(data)
    return info


def get_firmware(setup: Setup, id: int) -> FirmwareInfo:
    """
    Read the given firmware info.
    """
    json_path = (firmware_dir(setup, f'{id}')) / "firmware.json"
    return json.loads(json_path.read_text())


def get_firmware_path(setup: Setup, id: int) -> List[Path]:
    """
    Get the binary paths.
    """
    json = get_firmware(setup, id)
    dir = firmware_dir(setup, id)
    return list(map(lambda f: dir / f['name'], json.get('files', [])))

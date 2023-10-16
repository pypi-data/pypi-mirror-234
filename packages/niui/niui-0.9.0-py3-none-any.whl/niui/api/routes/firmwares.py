"""
API for managing firmwares.
"""
import base64
from ..files.firmware import save_firmware, all_firmwares, get_firmware, get_firmware_path, create_firmware
from ..types import Setup, Config, FirmwareInfo
from ..can.read import fetch_fw_info
from ..can.write import write_firmware
from ..error import NimuException
from typing import List


def index(setup: Setup) -> List[FirmwareInfo]:
    all = all_firmwares(setup)
    all.sort(key=lambda item: -item["id"])
    return all


def get(setup: Setup, id: int) -> FirmwareInfo:
    firmware = get_firmware(setup, id)
    return firmware


def create(setup: Setup, conf: Config) -> FirmwareInfo:
    id = create_firmware(setup)
    for file in conf.get('files'):
        name = file.get('name')
        data = base64.b64decode(file.get('data'))
        save_firmware(setup, id, name, data)
    return get_firmware(setup, id)


def write(setup: Setup, firmware_id: int, box_id: int) -> FirmwareInfo:
    firmware_path = get_firmware_path(setup, firmware_id)
    # TODO: Support for multibinary.
    binary = firmware_path[0].read_bytes()
    info = fetch_fw_info(setup, boxes=[box_id])[box_id]
    if not info:
        # TODO: Error handling in upper level and communicating to UI.
        raise NimuException(f'Cannot reach box {box_id}')

    setup["logger"].info(f'Starting flashing for the box {box_id}.')
    # TODO: Before doing this, we should check if version is needed etc.
    write_firmware(setup, box_id, binary)
    setup["logger"].info(f'Flashing completed for the box {box_id}.')

    return {}

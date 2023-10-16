"""
API for getting device info.
"""
from ..types import Setup, FirmwareInfo
from ..can.read import fetch_fw_info
from typing import List


def index(setup: Setup) -> List[FirmwareInfo]:
    info = fetch_fw_info(setup)
    messages = filter(lambda i: i is not None, info)
    boxes = list(map(lambda m: m.to_json(), messages))
    boxes.sort(key=lambda item: item["box_id"])
    return boxes

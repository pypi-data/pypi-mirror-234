import time
import can
from typing import Dict, Any
from ..data import Item, from_values
from ..types import Setup
from ..error import NimuException
from .messages import NimuMessage, DfuInitMessage, DfuDataMessage, ConfigWriteMessage, SaveAndResetMessage
from .listeners import FwWriteListener, ConfigWriteListener
from .bus import bus, notifier
from niui.helpers import crc


def send(setup: Setup, msg: NimuMessage) -> None:
    """
    Straightforward message sending.
    """
    bus.send(msg)


def write_firmware(setup: Setup, box_id: int, binary: bytearray, timeout: int = 60000) -> None:
    """
    Write a firmware.
    """
    listener = FwWriteListener(box_id)
    notifier.add_listener(listener)
    try:
        setup["logger"].info(f"Initializing firmware writing for the box {box_id}.")
        bus.send(DfuInitMessage(box_id, len(binary), crc(binary)))
    except can.CanError:
        setup["logger"].error("Sending the CAN bus message failed.")

    while True:
        while timeout > 0:
            next_chunk = listener.next_chunk()
            if next_chunk is not None:
                break
            time.sleep(0.001)
            timeout -= 1

        if next_chunk is None or timeout <= 0:
            notifier.remove_listener(listener)
            raise NimuException('Writing timed out.')

        if listener.is_complete():
            break

        offset = next_chunk * 8
        slice = binary[offset: offset+8]
        if len(slice) > 0:
            bus.send(DfuDataMessage(box_id, next_chunk, slice))
        time.sleep(0.001)

    notifier.remove_listener(listener)


def write_config(setup: Setup, items: Dict[int, Item], box_id: int, config: Dict[int, Any], timeout: int = 10000):
    """
    Write a configuration.
    """
    bytes = from_values(setup, items, config)

    listener = ConfigWriteListener(box_id)
    setup["logger"].info(f"Writing configuration for the box {box_id}.")
    notifier.add_listener(listener)

    for item_id in bytes:
        i = 0
        while i * 8 < len(bytes[item_id]):
            try:
                bus.send(ConfigWriteMessage(box_id, int(item_id), i, bytes[item_id][i*8:i*8 + 8]))
            except can.CanError:
                setup["logger"].error("Sending the CAN bus message failed.")
            i += 1
        time.sleep(0.01)

    setup["logger"].info(f"Sending saving and reset request to the box {box_id}.")
    bus.send(SaveAndResetMessage(box_id))
    while True:
        time.sleep(0.010)
        timeout -= 10

        if listener.is_complete():
            break

        if timeout <= 0:
            raise NimuException('Writing timed out.')

    notifier.remove_listener(listener)

    return {}

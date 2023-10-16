import time
import can
from typing import Any, Dict, List
from ..types import Setup
from ..data import Item, to_values
from ..error import NimuException
from .listeners import NimuListener, ConfigListener, FwInfoListener
from .messages import NimuMessage, QueryFwInfoMessage, FwInfoMessage
from .bus import bus, notifier

def listen(setup: Setup, listener: NimuListener, init: List[NimuMessage], timeout: int = 500, error_on_timeout: bool = False):
    """
    Helper to execute listening.
    """
    listeners = [listener]
    if setup['debug'] and not setup['quiet']:
        listeners.append(can.Printer())
    notifier.add_listener(listener)

    try:
        for msg in init:
            bus.send(msg)
            time.sleep(0.02)
        setup["logger"].info(f"Waiting messages for {listener.__class__.__name__} from the CAN bus.")
    except can.CanError:
        setup["logger"].error("Sending the CAN bus message failed.")

    while timeout > 0:
        if listener.is_complete():
            break
        time.sleep(0.01)
        timeout -= 10

    if error_on_timeout and timeout <= 0:
        raise NimuException(f"Request timed out.")

    [notifier.remove_listener(l) for l in listeners]
    return listener.result()


def fetch_config(setup: Setup, items: Dict[int, Item], box_id: int, item_ids: List[int],
                 timeout: int = 2500) -> Dict[int, Any]:
    """
    Ask configuration from the bus.
    """
    query = {}
    for id in item_ids:
        if not items[id]:
            raise NimuException(f"Unrecognized item ID ${id} given.")
        query[id] = items[id]
    listener = ConfigListener(box_id, items=query)
    query = listener.initial_query()
    resp = listen(setup, listener, query, timeout, error_on_timeout=True)
    return to_values(setup, items, resp)


def fetch_fw_info(setup: Setup, timeout: int = 500, boxes: List[int] = range(16),
                  no_poll: bool = False) -> Dict[str, Any]:
    """
    Ask firmware info for a box.
    """
    if no_poll:
        init = []
    else:
        init = list(map(lambda n: QueryFwInfoMessage(n), boxes))
    return listen(setup, FwInfoListener(boxes), init, timeout)


def wait_fw_info(setup: Setup, init: List[NimuMessage], timeout: int = 250) -> List[FwInfoMessage]:
    """
    Send messages and wait for response.
    """
    resp = listen(setup, FwInfoListener(list(set(map(lambda msg: msg.box_id, init)))), init, timeout)
    return list(filter(lambda r: r is not None, resp))

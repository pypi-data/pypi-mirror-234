from typing import List, Any, Dict, Optional
from .messages import NimuMessage, FwInfoMessage, ConfigValueMessage, QueryConfigMessage
from ..data import Item
import can


class NimuListener(can.Listener):
    """
    Base class for listeners.
    """

    def result(self: 'NimuListener') -> Any:
        """
        Function callecting results for listening.
        """
        return None

    def is_complete(self: 'NimuListener') -> bool:
        """
        Checker if we are satisfied the data collected so far.
        """
        return True


class ConfigListener(NimuListener):
    """
    CAN bus listener recording configuration items seen.
    """

    def __init__(self: 'ConfigListener', box_id: int, items=Dict[int, Item]) -> None:
        super().__init__()
        self.box_id = box_id
        self.items = items
        self.remains = set(dict.keys(items))
        self.values = {}

    def on_message_received(self: 'ConfigListener', msg: can.Message) -> None:
        nimu = NimuMessage.get(msg)
        if isinstance(nimu, ConfigValueMessage) and nimu.item_id in self.items:
            data = list(nimu.data)
            finished = False
            if len(data) == 0 and nimu.chunk_id == 0:
                # value not available
                self.values[nimu.item_id] = None
                finished = True
            else:
                item = self.items[nimu.item_id]
                if self.values.get(nimu.item_id) is None:
                    self.values[nimu.item_id] = [None] * len(item)

                n = nimu.chunk_id * 8
                for i in range(len(data)):
                    self.values[nimu.item_id][n + i] = data[i]
                finished = all(v is not None for v in self.values[nimu.item_id])
                
            if finished:
                self.remains = self.remains - set([nimu.item_id])

    def result(self: 'ConfigListener') -> Dict[int, ConfigValueMessage]:
        return self.values

    def is_complete(self: 'ConfigListener') -> bool:
        return len(self.remains) == 0

    def initial_query(self: 'ConfigListener') -> List[QueryConfigMessage]:
        return list(map(lambda item_id: QueryConfigMessage(self.box_id, item_id), self.remains))


class FwInfoListener(NimuListener):
    """
    CAN bus listener recording configuration items seen.
    """
    def __init__(self: 'FwInfoListener', boxes: List[int]) -> None:
        super().__init__()
        self.boxes = set(boxes)
        self.items = [None, None, None, None, None, None, None, None,
                      None, None, None, None, None, None, None, None]

    def on_message_received(self: 'ConfigListener', msg: can.Message) -> None:
        nimu = NimuMessage.get(msg)
        if isinstance(nimu, FwInfoMessage):
            self.items[nimu.box_id] = nimu
            self.boxes = self.boxes - set([nimu.box_id])

    def result(self: 'FwInfoListener') -> List[FwInfoMessage]:
        return self.items

    def is_complete(self: 'FwInfoListener') -> bool:
        return len(self.boxes) == 0


class FwWriteListener(NimuListener):
    """
    CAN bus listener for wrtinging firmware.
    """
    def __init__(self: 'FwWriteListener', box_id: int) -> None:
        super().__init__()
        self.box_id = box_id
        self.received = False
        self.chunk_id = None
        self.done = False

    def on_message_received(self: 'ConfigListener', msg: can.Message) -> None:
        nimu = NimuMessage.get(msg)
        if isinstance(nimu, FwInfoMessage) and nimu.box_id == self.box_id:
            self.received = True
            self.done = not nimu.updating
            if self.chunk_id is None:
                self.chunk_id = nimu.first_missing_chunk
            else:
                self.chunk_id = max(self.chunk_id, nimu.first_missing_chunk)

    def result(self: 'FwWriteListener') -> List[FwInfoMessage]:
        return self.chunk_id

    def next_chunk(self: 'FwWriteListener') -> Optional[int]:
        if not self.received:
            return None
        self.received = False
        return self.chunk_id

    def is_complete(self: 'FwWriteListener') -> bool:
        return self.done


class ConfigWriteListener(NimuListener):
    """
    CAN bus listener for writing configuration.
    """
    def __init__(self: 'ConfigWriteListener', box_id: int) -> None:
        super().__init__()
        self.box_id = box_id
        self.done = False

    def on_message_received(self: 'ConfigWriteListener', msg: can.Message) -> None:
        nimu = NimuMessage.get(msg)
        if isinstance(nimu, FwInfoMessage) and nimu.box_id == self.box_id:
            self.done = True

    def is_complete(self: 'ConfigWriteListener') -> bool:
        return self.done

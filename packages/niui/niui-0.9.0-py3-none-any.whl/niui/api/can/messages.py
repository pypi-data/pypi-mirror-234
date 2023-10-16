import can
from typing import Type, Optional, Any, List, Dict
from niui.helpers import bits, l16, h16, l24, m24, h24, w16, set_bit
from ..data import Item


class NimuMessage(can.Message):
    """
    Base class for CAN messages
    """

    def __str__(self: 'NimuMessage') -> None:
        return f'\033[1;34m{self.__class__.__name__}({super().__str__()})\033[0m'

    def to_json(self: 'NimuMessage') -> Dict[str, Any]:
        return {}

    @classmethod
    def match(cls: Type, msg: 'NimuMessage') -> bool:
        False

    @staticmethod
    def get(msg: can.Message) -> Optional['NimuMessage']:
        """
        Check the message and if familiar, instantiate our own class.
        """
        ret = None
        if QueryFwInfoMessage.match(msg):
            ret = QueryFwInfoMessage(0)
        elif FwInfoMessage.match(msg):
            ret = FwInfoMessage(0, 0, 0)
        elif DfuInitMessage.match(msg):
            ret = DfuInitMessage(0, 0, 0)
        elif DfuDataMessage.match(msg):
            ret = DfuDataMessage(0, 0, [])
        elif QueryConfigMessage.match(msg):
            ret = QueryConfigMessage(0, 0)
        elif ConfigValueMessage.match(msg):
            ret = ConfigValueMessage(0, 0, 0, [])
        elif ConfigWriteMessage.match(msg):
            ret = ConfigWriteMessage(0, 0, 0, [])
        elif SaveAndResetMessage.match(msg):
            ret = SaveAndResetMessage(0)

        if ret is not None:
            ret.arbitration_id = msg.arbitration_id
            ret.data = msg.data
            ret.is_remote_frame = msg.is_remote_frame

        return ret


class QueryConfigMessage(NimuMessage):
    """
    A message for requesting device configuration.
    """

    def __init__(self: 'QueryConfigMessage', box_id: int, item_id: int) -> None:
        super().__init__(arbitration_id=0x1e000000 | (item_id << 8) | box_id, is_remote_frame=True)

    @classmethod
    def match(cls: Type, msg: NimuMessage) -> bool:
        return msg.arbitration_id >= 0x1e000000 and msg.arbitration_id <= 0x1effffff and msg.is_remote_frame

    @property
    def box_id(self: 'QueryConfigMessage') -> int:
        return self.arbitration_id & 0xf

    @property
    def item_id(self: 'QueryConfigMessage') -> int:
        return (self.arbitration_id >> 8) & 0xffff


class ConfigValueMessage(NimuMessage):
    """
    A message desribing configuration item value.

    0x1e$$$$@#  NIMU->PC  CONF_ITEM_GET, where $$$$ = item_id, @ = chunk_id

        data: configuration item value.

        chunk_id = 0 && len = 0 denotes CONF ITEM NOT AVAILABLE
        Actual conf item size is the sum of all chunk sizes

        When requesting (using RTR frame), only request chunk 0. All chunks will be sent.

    """

    def __init__(self: 'ConfigValueMessage', box_id: int, item_id: int,
                 chunk_id: int, value: List[int]) -> None:
        super().__init__(arbitration_id=0x1e000000 | (item_id << 8) | (chunk_id << 4) | box_id, data=value)

    @classmethod
    def match(cls: Type, msg: NimuMessage) -> bool:
        return msg.arbitration_id >= 0x1e000000 and msg.arbitration_id <= 0x1effffff and not msg.is_remote_frame

    @property
    def box_id(self: 'QueryConfigMessage') -> int:
        return self.arbitration_id & 0xf

    @property
    def chunk_id(self: 'QueryConfigMessage') -> int:
        return (self.arbitration_id >> 4) & 0xf

    @property
    def item_id(self: 'QueryConfigMessage') -> int:
        return (self.arbitration_id >> 8) & 0xffff


class ConfigWriteMessage(NimuMessage):
    """
    A message for saving configuration values to the box.

    0x1d$$$$@# PC->NIMU   CONF_ITEM_SET, where $$$$ = item_id, @ = chunk_id

        data: new value to set.
    """

    def __init__(self: 'ConfigWriteMessage', box_id: int, item_id: int,
                 chunk_id: int, value: List[int]) -> None:
        super().__init__(arbitration_id=0x1d000000 | (item_id << 8) | (chunk_id << 4) | box_id, data=value)

    @classmethod
    def match(cls: Type, msg: NimuMessage) -> bool:
        return msg.arbitration_id >= 0x1d000000 and msg.arbitration_id <= 0x1dffffff and not msg.is_remote_frame

    @property
    def box_id(self: 'ConfigWriteMessage') -> int:
        return self.arbitration_id & 0xf

    @property
    def chunk_id(self: 'ConfigWriteMessage') -> int:
        return (self.arbitration_id >> 4) & 0xf

    @property
    def item_id(self: 'ConfigWriteMessage') -> int:
        return (self.arbitration_id >> 8) & 0xffff


class SaveAndResetMessage(NimuMessage):
    """
    Request for saving configuration and resetting the box.
    """
    def __init__(self: 'SaveAndResetMessage', box_id: int) -> None:
        super().__init__(arbitration_id=0x1c000030 | box_id)

    @classmethod
    def match(cls: Type, msg: NimuMessage) -> bool:
        return msg.arbitration_id >= 0x1c000030 and msg.arbitration_id <= 0x1c00003f and not msg.is_remote_frame

    @property
    def box_id(self: 'SaveAndResetMessage') -> int:
        return self.arbitration_id & 0xf


class QueryFwInfoMessage(NimuMessage):
    """
    A message for requesting firmware info.
    """

    def __init__(self: 'QueryFwInfoMessage', box_id: int) -> None:
        super().__init__(arbitration_id=0x1fffffe0 | box_id, is_remote_frame=True)

    @classmethod
    def match(cls: Type, msg: NimuMessage) -> bool:
        return msg.arbitration_id >= 0x1fffffe0 and msg.arbitration_id <= 0x1fffffef and msg.is_remote_frame

    @property
    def box_id(self: 'QueryFwInfoMessage') -> int:
        return self.arbitration_id & 0xf


class FwInfoMessage(NimuMessage):
    """
    A message describing firmware info.

    Byte  0 bits 0-1: currently running application
        0 = running single-linked firmware (always the same binary)
        1 = running A-linked firmware, expecting B binary;
        2 = running B-linked firmware, expecting A binary;
        3 = reserved
    Byte  0 bit  2  : Update initiated, waiting for data packets
    Byte  0 bit  3  : Update failed, verify parameters and try again
    Byte  0 bit  4  : Running secondary firmware because the primary one is not intact (e.g. corruption)

    Bytes 1-2     : Currently running firmware version ID (u16LE)
    Byte  3       : HW/FW revision ID (distinguish between hardware-incompatible versions, need to update with same ID)
    Bytes 4-5     : First missing chunk_idx (valid if update in progress) (u16LE)

    """

    def __init__(self: 'FwInfoMessage', box_id: int, version_id: int, revision: int) -> None:
        data = [
            bits(1, 0, 0, 0, 0),
            l16(version_id),
            h16(version_id),
            revision,
            0,
            0
        ]
        super().__init__(arbitration_id=0x1fffffe0 | box_id, data=data)

    def to_json(self: 'FwInfoMessage') -> Dict[str, Any]:
        return {
            'box_id': self.box_id,
            'running': self.running,
            'updating': self.updating,
            'failed': self.failed,
            'running_secondary': self.running_secondary,
            'version_id': hex(self.version_id),
            'revision': self.revision,
            'first_missing_chunk': self.first_missing_chunk
        }

    @classmethod
    def match(cls: Type, msg: NimuMessage) -> bool:
        return msg.arbitration_id >= 0x1fffffe0 and msg.arbitration_id <= 0x1fffffef and not msg.is_remote_frame

    @property
    def box_id(self: 'FwInfoMessage') -> int:
        return self.arbitration_id & 0xf

    @property
    def running(self: 'FwInfoMessage') -> str:
        a = (self.data[0] & (1 << 0)) > 0
        b = (self.data[0] & (1 << 1)) > 0
        if a and b:
            return 'reserved'
        if a:
            return 'A'
        if b:
            return 'B'
        return '1'

    @property
    def updating(self: 'FwInfoMessage') -> bool:
        return (self.data[0] & (1 << 2)) > 0

    @property
    def failed(self: 'FwInfoMessage') -> bool:
        return (self.data[0] & (1 << 3)) > 0

    @property
    def running_secondary(self: 'FwInfoMessage') -> bool:
        return (self.data[0] & (1 << 4)) > 0

    @property
    def version_id(self: 'FwInfoMessage') -> int:
        return w16(self.data[1], self.data[2])

    @property
    def revision(self: 'FwInfoMessage') -> int:
        return self.data[3]

    @property
    def first_missing_chunk(self: 'FwInfoMessage') -> int:
        return w16(self.data[4], self.data[5])

    # Touching property setters screws up can.Message.
    def set_updating(self: 'FwInfoMessage', value: bool) -> None:
        self.data[0] = set_bit(self.data[0], 2, value)

    def set_failed(self: 'FwInfoMessage', value: bool) -> None:
        self.data[0] = set_bit(self.data[0], 3, value)

    def set_first_missing_chunk(self: 'FwInfoMessage', value: int) -> None:
        self.data[4] = l16(value)
        self.data[5] = h16(value)


class DfuInitMessage(NimuMessage):
    """
    Initialize firmware flashing.

    0x1ffffff#  PC->NIMU  DFU_INIT
        Bytes 0-2       : Firmware length, bytes, u24LE
        Bytes 3-4       : crc16_Mcrf4Xx over the bytes. If len is odd, padding when calculating CRC with 0xff
    """

    def __init__(self: 'DfuInitMessage', box_id: int, len: int, crc: int) -> None:
        data = [
            l24(len),
            m24(len),
            h24(len),
            l16(crc),
            h16(crc)
        ]
        super().__init__(arbitration_id=0x1ffffff0 | box_id, data=data)

    @property
    def box_id(self: 'DfuInitMessage') -> int:
        return self.arbitration_id & 0xf

    @property
    def length(self: 'DfuInitMessage') -> int:
        return self.data[0] | (self.data[1] << 8) | (self.data[2] << 16)

    @classmethod
    def match(cls: Type, msg: NimuMessage) -> bool:
        return msg.arbitration_id >= 0x1ffffff0 and msg.arbitration_id <= 0x1fffffff and not msg.is_remote_frame


class DfuDataMessage(NimuMessage):
    """
    Data for firmware.

    0x1f$$$$$#  PC->NIMU  DFU_DATA, where $$$$$ = chunk_id
        Chunk content. 8 bytes. Only the last chunk may be shorter.
        Number of chunks must be ceil(firmware_length / 8)
    """

    def __init__(self: 'DfuDataMessage', box_id: int, chunk_id: int, data: bytearray) -> None:
        super().__init__(arbitration_id=0x1f000000 | box_id | (chunk_id << 4), data=data)

    @property
    def box_id(self: 'DfuDataMessage') -> int:
        return self.arbitration_id & 0xf

    @property
    def chunk_id(self: 'DfuDataMessage') -> int:
        return (self.arbitration_id >> 4) & 0xfffff

    @classmethod
    def match(cls: Type, msg: NimuMessage) -> bool:
        return msg.arbitration_id >= 0x1f000000 and msg.arbitration_id < 0x1ffffff0 and not msg.is_remote_frame

"""
Configuration item defintions.
"""
import struct
from dataclasses import dataclass, field
from typing import List, Any, Dict, Optional
from .types import Setup
from .error import NimuException
from functools import reduce
from operator import mul


def reshape(lst, shape):
    if len(shape) == 1:
        return lst
    n = reduce(mul, shape[1:])
    return [reshape(lst[i*n:(i+1)*n], shape[1:]) for i in range(len(lst)//n)]


@dataclass
class DataMapping:
    name: str
    type: str
    cname: str
    options: Dict[str, int] = field(default_factory=dict)


@dataclass
class ItemDescription:
    id: int
    group: List[str]
    name: str
    nameUI: str
    description: str
    public: bool = False


@dataclass
class ItemData:
    type: str
    constant: bool = False
    defaultValue: Any = None
    dimension: List[int] = field(default_factory=list)
    constraints: Any = None

    def __post_init__(self):
        # dimension must be a list of length 0 or 2, enforce this
        if len(self.dimension) == 0:
            self.dimension = [1]
        if len(self.dimension) == 1:
            self.dimension = [self.dimension[0], 1]
        if len(self.dimension) != 2:
            raise NimuException(f"Dimension must be a list of length 0 or 2, got {self.dimension}.")
        if self.dimension[0] < 1 or self.dimension[1] < 1:
            raise NimuException(f"Dimension must be positive, got {self.dimension}.")


@dataclass
class Item:
    description: ItemDescription
    data: ItemData
    mapping: Optional[DataMapping] = None

    @property
    def id(self):
        return self.description.id

    @property
    def name(self):
        return '.'.join(self.description.group) + '.' + self.description.name

    @property
    def type(self):
        if self.mapping:
            if self.mapping.type != 'scalar':
                return self.mapping.type
        return self.data.type

    def __len__(self):
        """
        How many data bytes value takes.
        """
        t = self.type
        if t == 'u32':
            return 4
        if t[0:4] == 'enum':
            return int(t[4:])
        if t == 'real':
            return reduce(lambda x1, x2: x1*x2, self.data.dimension, 1) * 4

        raise NimuException(f"Cannot determine length in bytes for type '{t}' in {self} (Not implemented).")


def signed(val: int, bytes: int) -> int:
    """
    Convert value to signed.
    """
    max_val = 1 << (bytes * 8)
    max_int = 1 << (bytes * 8 - 1)
    if val >= max_int:
        return val - max_val
    return val


def _enum2value(t: str, item: Item, bytes: List[int]):
    """
    Helper to parse enum value.
    """
    if t == 'enum1':
        index = signed(bytes[0], 1)
    if t == 'enum2':
        index = signed(bytes[0] | (bytes[1] << 8), 2)
    if t == 'enum4':
        index = signed(bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24), 4)

    for k in item.mapping.options:
        opt = item.mapping.options[k]
        if type(opt) == str and opt[0:2] == '0x':
            opt = int(opt, 16)
        if opt == index:
            return k

    raise NimuException(f"Cannot find matching option for value '{index}' from options of {item}.")


def _real2value(item: Item, bytes: List[int]):
    """
    Helper to parse real value.
    """
    i = 0
    floats = []
    while i * 4 < len(bytes):
        floats.append(struct.unpack('<f', bytearray(bytes[i * 4:i * 4 + 4]))[0])
        i += 1
    shape = item.data.dimension if len(item.data.dimension) > 0 else [1]
    matrix = reshape(floats, shape)
    return matrix


def device2value(setup: Setup, item: Item, bytes: List[int]):
    """
    Convert device bytes to value.
    """
    if len(list(filter(lambda v: v is None, bytes))) > 0:
        setup["logger"].warning(f"Incomplete value received for {item.name}.")
        return None

    t = item.type

    if t == 'u32':
        return bytes[0] | (bytes[1] << 8) | (bytes[2] << 16) | (bytes[3] << 24)

    if t[0:4] == 'enum':
        return _enum2value(t, item, bytes)

    if t == 'real':
        return _real2value(item, bytes)

    raise NimuException(f"Cannot determine value for type '{t}' in {item} (Not implemented).")


def value2device(setup: Setup, item: Item, value: Any):
    """
    Convert a configuration value to the list of device bytes.
    """

    t = item.type

    if t == 'u32':
        return [value & 0xff, (value >> 8) & 0xff, (value >> 16) & 0xff, (value >> 24) & 0xff]

    if t[0:4] == 'enum':
        option = item.mapping.options[value]
        if type(option) == str and option[0:2] == '0x':
            option = int(option, 16)
        if t == 'enum1':
            return [option & 0xff]
        if t == 'enum2':
            return [option & 0xff, (option >> 8) & 0xff]
        if t == 'enum4':
            return [option & 0xff, (option >> 8) & 0xff, (option >> 16) & 0xff, (option >> 24) & 0xff]

    if t == 'real':
        bytes = []
        for row in value:
            for e in row:
                bytes += list(bytearray(struct.pack('<f', e)))
        return bytes

    raise NimuException(f"Cannot convert value {value} of type '{t}' in {item} (Not implemented).")


def to_values(setup: Setup, items: Dict[int, Item], resp: Dict[int, List[int]]) -> Dict[int, Any]:
    """
    Parse all values from device byte arrays and construct mapping from item IDs to values.
    """
    ret = dict()
    for item_id in resp:
        if resp[item_id] is None:
            continue
        value = device2value(setup, items[item_id], resp[item_id])
        if value is not None:
            ret[item_id] = value
    return ret


def from_values(setup: Setup, items: Dict[int, Item], config: Dict[str, Any]) -> Dict[int, List[int]]:
    """
    Convert item values to array of bytes.
    """
    ret = dict()
    for item_id in config:
        value = value2device(setup, items[int(item_id)], config[item_id])
        if value is not None:
            ret[item_id] = value
    return ret

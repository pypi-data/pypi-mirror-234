def h16(byte: int) -> int:
    """
    Get higher byte of 16 bit int.
    """
    return (byte >> 8) & 0xff


def l16(byte: int) -> int:
    """
    Get lower byte of 16 bit int.
    """
    return byte & 0xff


def h24(byte: int) -> int:
    """
    Get higher byte of 24 bit int.
    """
    return (byte >> 16) & 0xff


def m24(byte: int) -> int:
    """
    Get lower byte of 24 bit int.
    """
    return (byte >> 8) & 0xff


def l24(byte: int) -> int:
    """
    Get lower byte of 24 bit int.
    """
    return byte & 0xff


def w16(low: int, high: int) -> int:
    """
    Get a 16-bit word from two bytes
    """
    return (high << 8) + low


def bits(b0: int, b1: int = 0, b2: int = 0, b3: int = 0, b4: int = 0, b5: int = 0, b6: int = 0, b7: int = 0) -> int:
    """
    Construct a byte from bits.
    """
    return (
        b0 |
        b1 << 1 |
        b2 << 2 |
        b3 << 3 |
        b4 << 4 |
        b5 << 5 |
        b6 << 6 |
        b7 << 7
    )


def set_bit(w: int, bit: int, value: bool):
    """
    Helper to change the value of a single bit.
    """
    mask = 1 << bit
    if value:
        return w | mask
    else:
        return w & (~mask)


def crc(binary: bytearray) -> int:
    """
    Calculate CRC for the binary.
    """
    pad = bytearray([])
    if len(binary) % 2:
        pad = bytearray([0xff])
    crc = 0xffff
    for b in binary + pad:
        crc ^= b
        for i in range(8):
            if (crc & 1):
                crc = ((crc >> 1) ^ 0x8408)
            else:
                crc = (crc >> 1)
    return crc

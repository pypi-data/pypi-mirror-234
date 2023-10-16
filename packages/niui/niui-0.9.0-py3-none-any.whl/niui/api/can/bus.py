import can

bus = None
notifier = None

def open_bus(setup):
    global bus, notifier

    filters = [
        {"can_id": 0x10000000, "can_mask": 0x10000000, "extended": True},
    ]

    bus = can.ThreadSafeBus(channel=setup['channel'], interface=setup['interface'], bitrate=setup['bitrate'], can_filters=filters)
    notifier = can.Notifier(bus, [])

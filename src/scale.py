from decimal import Decimal
from typing import Callable

from bluepy.btle import Scanner, DefaultDelegate


class ScanDelegate(DefaultDelegate):

    SERVICE_DATA_AD_TYPE = 22

    def __init__(self, mac_addr: str, callback: Callable):
        super().__init__()
        self._mac_addr = mac_addr
        self._callback = callback
        self._prev_data = None

    def handleDiscovery(self, dev, *args):
        if dev.addr.upper() != self._mac_addr.upper():
            return

        raw_data = next(
            bytes.fromhex(value[4:]) for (ad_type, _, value) in dev.getScanData()
            if ad_type == self.SERVICE_DATA_AD_TYPE
        )
        self.handle_data(raw_data)

    def handle_data(self, data: bytes):
        if data == self._prev_data:
            return

        self._prev_data = data

        is_stabilized = (data[0] & (1 << 5)) != 0
        is_load_removed = (data[0] & (1 << 7)) != 0
        if not is_stabilized or is_load_removed:
            return

        weight = (Decimal(int.from_bytes(data[1:3], byteorder="little")) / 100 / 2).quantize(Decimal("0.01"))
        self._callback(weight)


def watch_for_scale(mac_addr: str, callback: Callable):
    scanner = Scanner().withDelegate(ScanDelegate(mac_addr, callback))
    while True:
        scanner.start()
        scanner.process(1)
        scanner.stop()

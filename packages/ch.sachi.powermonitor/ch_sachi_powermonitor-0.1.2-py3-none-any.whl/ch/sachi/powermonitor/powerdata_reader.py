from typing import Optional

from victron_ble.devices import BatteryMonitorData, DeviceData

from ch.sachi.victron_ble.powermonitor_scanner import PowermonitorScanner


class PowerdataReader:
    result: BatteryMonitorData = None

    def __init__(self, id: str, key: str):
        self.id = id
        self.key = key

    def read(self) -> Optional[BatteryMonitorData]:
        keys = {self.id, self.key}
        scanner = self.create_scanner(keys)
        scanner.start()
        scanner.stop()
        return self.result

    def create_scanner(self, keys):
        return PowermonitorScanner(self.cb, keys)

    def cb(self, device_data: DeviceData):
        if isinstance(device_data, BatteryMonitorData):
            self.result = device_data

from typing import Callable

from bleak import BLEDevice
from victron_ble.devices import DeviceData
from victron_ble.exceptions import AdvertisementKeyMissingError, UnknownDeviceError
from victron_ble.scanner import Scanner, logger


class PowermonitorScanner(Scanner):
    def __init__(self,
                 callback_parsed: Callable[[DeviceData], None],
                 device_keys: dict[str, str] = {}) -> None:
        super().__init__(device_keys)
        self.callback_parsed = callback_parsed

    async def callback(self, ble_device: BLEDevice, raw_data: bytes):
        logger.debug(
            f"Received data from {ble_device.address.lower()}: {raw_data.hex()}"
        )
        try:
            device = self.get_device(ble_device, raw_data)
        except AdvertisementKeyMissingError:
            return
        except UnknownDeviceError as e:
            logger.error(e)
            return
        parsed = device.parse(raw_data)
        self.callback_parsed(parsed)
        await self.stop()

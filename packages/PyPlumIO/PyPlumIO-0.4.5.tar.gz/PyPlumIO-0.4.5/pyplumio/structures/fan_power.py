"""Contains fan power structure decoder."""
from __future__ import annotations

import math
from typing import Final

from pyplumio import util
from pyplumio.helpers.typing import EventDataType
from pyplumio.structures import StructureDecoder, ensure_device_data

ATTR_FAN_POWER: Final = "fan_power"


class FanPowerStructure(StructureDecoder):
    """Represents fan power sensor data structure."""

    def decode(
        self, message: bytearray, offset: int = 0, data: EventDataType | None = None
    ) -> tuple[EventDataType, int]:
        """Decode bytes and return message data and offset."""
        fan_power = util.unpack_float(message[offset : offset + 4])[0]
        offset += 4
        if not math.isnan(fan_power):
            return ensure_device_data(data, {ATTR_FAN_POWER: fan_power}), offset

        return ensure_device_data(data), offset

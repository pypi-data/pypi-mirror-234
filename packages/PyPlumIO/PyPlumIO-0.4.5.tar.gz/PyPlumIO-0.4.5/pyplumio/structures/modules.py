"""Contains modules structure decoder."""
from __future__ import annotations

from dataclasses import dataclass
import struct
from typing import Final

from pyplumio.const import BYTE_UNDEFINED
from pyplumio.helpers.typing import EventDataType
from pyplumio.structures import StructureDecoder, ensure_device_data

ATTR_MODULES: Final = "modules"
ATTR_MODULE_A: Final = "module_a"
ATTR_MODULE_B: Final = "module_b"
ATTR_MODULE_C: Final = "module_c"
ATTR_ECOLAMBDA: Final = "ecolambda"
ATTR_ECOSTER: Final = "ecoster"
ATTR_PANEL: Final = "panel"
MODULES: tuple[str, ...] = (
    ATTR_MODULE_A,
    ATTR_MODULE_B,
    ATTR_MODULE_C,
    ATTR_ECOLAMBDA,
    ATTR_ECOSTER,
    ATTR_PANEL,
)


@dataclass
class ConnectedModules:
    """Represents firmware version info for connected module."""

    module_a: str | None = None
    module_b: str | None = None
    module_c: str | None = None
    ecolambda: str | None = None
    ecoster: str | None = None
    panel: str | None = None


def _get_module_version(
    module_name: str, message: bytearray, offset: int = 0
) -> tuple[str | None, int]:
    """Get module version from a message."""
    if message[offset] == BYTE_UNDEFINED:
        return None, (offset + 1)

    version_data = struct.unpack("<BBB", message[offset : offset + 3])
    module_version = ".".join(str(i) for i in version_data)
    offset += 3

    if module_name == ATTR_MODULE_A:
        vendor_code, vendor_version = struct.unpack("<BB", message[offset : offset + 2])
        module_version += f".{chr(vendor_code)}{str(vendor_version)}"
        offset += 2

    return module_version, offset


class ModulesStructure(StructureDecoder):
    """Represents modules data structure."""

    def decode(
        self, message: bytearray, offset: int = 0, data: EventDataType | None = None
    ) -> tuple[EventDataType, int]:
        """Decode bytes and return message data and offset."""
        connected_modules = ConnectedModules()
        for module_name in MODULES:
            module_version, offset = _get_module_version(module_name, message, offset)
            setattr(connected_modules, module_name, module_version)

        return ensure_device_data(data, {ATTR_MODULES: connected_modules}), offset

from __future__ import annotations

from typing import Callable, Iterator, Self

from eth_utils.address import to_checksum_address

from atlantiscore.lib.exceptions import InvalidEVMAddress

EXAMPLE_ADDRESS_STRING = "0xa8E219Aa773fb12A812B7A3a4671b5B1933a49A8"
LiteralEVMAddress = str | int | bytes
PREFIXED_ADDRESS_LENGTH = 42
ADDRESS_BYTE_LENGTH = 20
PREFIX_SIZE = 2
BYTE_ORDER = "big"
NUMBER_OF_BITS_IN_BYTE = 8


class EVMAddress:
    _value: bytes

    def __init__(self, value: EVMAddress | LiteralEVMAddress) -> None:
        self._value = _address_to_bytes(value)

    def _to_checksum(self) -> str:
        return to_checksum_address(self._value)

    def __bytes__(self) -> bytes:
        return self._value

    def __int__(self) -> int:
        return int.from_bytes(self._value, BYTE_ORDER)

    def __str__(self) -> str:
        return self._to_checksum()

    def __eq__(self, other: any) -> bool:
        try:
            return hash(self) == hash(EVMAddress(other))
        except InvalidEVMAddress:
            return False

    def __ne__(self, other: any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return int(self)

    def __bool__(self) -> bool:
        return bool(int(self))

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable]:
        yield cls.validate

    @classmethod
    def validate(cls, v: EVMAddress | LiteralEVMAddress) -> Self:
        try:
            return cls(v)
        except InvalidEVMAddress as e:
            raise ValueError(str(e))

    @classmethod
    def __modify_schema__(cls, field_schema: dict) -> None:
        field_schema.update(type="string", example=EXAMPLE_ADDRESS_STRING)


def _address_to_bytes(value: EVMAddress | LiteralEVMAddress) -> bytes:
    try:
        if isinstance(value, EVMAddress):
            return bytes(value)

        if isinstance(value, str):
            address_bytes = _hex_to_bytes(value)
        elif isinstance(value, int):
            address_bytes = _int_to_bytes(value)
        elif isinstance(value, bytes):
            address_bytes = value
        else:
            raise TypeError

        if not _is_valid_address(address_bytes):
            raise ValueError

        return address_bytes
    except (ValueError, TypeError) as e:
        raise InvalidEVMAddress(value) from e


def _hex_to_bytes(address: str) -> bytes:
    if len(address) == PREFIXED_ADDRESS_LENGTH:
        address = address[PREFIX_SIZE:]
    return bytes.fromhex(address)


def _int_to_bytes(integer: int) -> bytes:
    return integer.to_bytes(_calculate_required_byte_count(integer), BYTE_ORDER).rjust(
        ADDRESS_BYTE_LENGTH, b"\x00"
    )


def _calculate_required_byte_count(integer: int) -> int:
    """Returns the minimum number of bytes required to represent the given int.

    Example:
    0 + 7 would require 0 bytes
    1 + 7 would require 1 byte
    """
    return (integer.bit_length() + 7) // NUMBER_OF_BITS_IN_BYTE


def _is_valid_address(address: bytes) -> bool:
    try:
        to_checksum_address(address)
        return True
    except ValueError:
        return False

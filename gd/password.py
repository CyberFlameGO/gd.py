from __future__ import annotations

from typing import BinaryIO, ClassVar, Optional, Type, TypeVar

from attrs import Attribute, define, field

from gd.binary import VERSION, Binary
from gd.binary_utils import Reader, Writer
from gd.encoding import decode_robtop_string, encode_robtop_string
from gd.enums import ByteOrder, Key
from gd.robtop import RobTop

__all__ = ("Password",)

COPYABLE_NO_PASSWORD = "copyable, no password"
COPYABLE_PASSWORD = "copyable, password {}"
NOT_COPYABLE = "not copyable"

NO_PASSWORD = 1

P = TypeVar("P", bound="Password")

COPYABLE_BIT = 0b10000000_00000000_00000000_00000000
PASSWORD_BIT = 0b01000000_00000000_00000000_00000000
PASSWORD_MASK = 0b00111111_11111111_11111111_11111111

DEFAULT_COPYABLE = False


@define()
class Password(Binary, RobTop):
    ADD: ClassVar[int] = 1000000

    password: Optional[int] = field(default=None)
    copyable: bool = field(default=DEFAULT_COPYABLE)

    @password.validator
    def check_password(self, attribute: Attribute[Optional[int]], password: Optional[int]) -> None:
        if password is not None:
            if password >= self.ADD:
                raise ValueError  # TODO: message?

    def __hash__(self) -> int:
        return self.to_value()

    def has_no_password(self) -> bool:
        return self.password is None

    def has_password(self) -> bool:
        return self.password is not None

    def is_copyable(self) -> bool:
        return self.copyable

    @classmethod
    def from_binary(
        cls: Type[P], binary: BinaryIO, order: ByteOrder = ByteOrder.DEFAULT, version: int = VERSION
    ) -> P:
        reader = Reader(binary)

        return cls.from_value(reader.read_u32(order))

    @classmethod
    def from_value(cls: Type[P], value: int) -> P:
        copyable_bit = COPYABLE_BIT
        password_bit = PASSWORD_BIT

        copyable = value & copyable_bit == copyable_bit
        password_present = value & password_bit == password_bit

        if password_present:
            password = value & PASSWORD_MASK

        else:
            password = None

        return cls(password=password, copyable=copyable)

    def to_value(self) -> int:
        value = self.password

        if value is None:
            value = 0

        else:
            value |= PASSWORD_BIT

        if self.is_copyable():
            value |= COPYABLE_BIT

        return value

    def to_binary(
        self, binary: BinaryIO, order: ByteOrder = ByteOrder.DEFAULT, version: int = VERSION
    ) -> None:
        writer = Writer(binary)

        writer.write_u32(self.to_value())

    def __str__(self) -> str:
        if self.is_copyable():
            password = self.password

            if password is None:
                return COPYABLE_NO_PASSWORD

            return COPYABLE_PASSWORD.format(password)

        return NOT_COPYABLE

    @classmethod
    def from_robtop_value(cls: Type[P], value: int) -> P:
        if value is None:
            return cls(password=None, copyable=False)

        if value == NO_PASSWORD:
            return cls(password=None, copyable=True)

        return cls(password=value % cls.ADD, copyable=True)

    def to_robtop_value(self) -> int:
        if self.copyable:
            password = self.password

            if password is None:
                return NO_PASSWORD

            return password + self.ADD

        return 0

    @classmethod
    def from_robtop(cls: Type[P], string: str) -> P:
        string = decode_robtop_string(string, Key.LEVEL_PASSWORD)

        if not string:
            value = 0

        else:
            value = int(string)

        return cls.from_robtop_value(value)

    def to_robtop(self) -> str:
        return encode_robtop_string(str(self.to_robtop_value()), Key.LEVEL_LEADERBOARD)

    @classmethod
    def can_be_in(cls, string: str) -> bool:
        return True

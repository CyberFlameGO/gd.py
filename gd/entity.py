from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO, Optional, Type, TypeVar

from attrs import Attribute, define, field
from typing_extensions import TypedDict

from gd.binary import VERSION, Binary
from gd.binary_utils import Reader, Writer
from gd.enums import ByteOrder
from gd.errors import ClientError
from gd.json import JSON

if TYPE_CHECKING:
    from gd.client import Client

__all__ = ("Entity", "EntityData")

E = TypeVar("E", bound="Entity")

CLIENT_NOT_ATTACHED = "`client` not attached to the entity: {}"


class EntityData(TypedDict):
    id: int


ID = "id"


@define()
class Entity(Binary, JSON[EntityData]):
    id: int = field()

    maybe_client: Optional[Client] = field(default=None, init=False, repr=False, eq=False)

    def __hash__(self) -> int:
        return hash(type(self)) ^ self.id

    @id.validator
    def check_id(self, attribute: Attribute[int], id: int) -> None:
        if id < 0:
            raise ValueError  # TODO: message?

    @property
    def client(self) -> Client:
        result = self.maybe_client

        if result is None:
            raise ClientError(CLIENT_NOT_ATTACHED.format(self))

        return result

    @client.setter
    def client(self, client: Client) -> None:
        self.maybe_client = client

    @client.deleter
    def client(self) -> None:
        self.maybe_client = None

    def maybe_attach_client(self: E, client: Optional[Client]) -> E:
        self.maybe_client = client

        return self

    def attach_client(self: E, client: Client) -> E:
        self.client = client

        return self

    def detach_client(self: E) -> E:
        del self.client

        return self

    def update_from(self: E, entity: Entity) -> E:
        vars(self).update(vars(entity))

        return self

    @classmethod
    def from_json(cls: Type[E], data: EntityData) -> E:
        return cls(id=data[ID])

    def to_json(self) -> EntityData:
        return EntityData(id=self.id)

    @classmethod
    def from_binary(
        cls: Type[E], binary: BinaryIO, order: ByteOrder = ByteOrder.DEFAULT, version: int = VERSION
    ) -> E:
        reader = Reader(binary)

        id = reader.read_u32(order)

        return cls(id)

    def to_binary(
        self, binary: BinaryIO, order: ByteOrder = ByteOrder.DEFAULT, version: int = VERSION
    ) -> None:
        writer = Writer(binary)

        writer.write_u32(self.id, order)
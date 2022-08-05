from itertools import count
from operator import attrgetter as get_attribute_factory
from typing import (
    AbstractSet, Iterable, Iterator, List, Optional, Sequence, Set, Type, TypeVar, Union, overload
)

from attrs import define, field

from gd.api.color_channels import ColorChannels
from gd.api.header import Header
from gd.api.objects import Object, has_target_group, object_from_binary, object_to_binary
from gd.enums import Speed, SpeedChange, SpeedMagic
from gd.errors import EditorError
from gd.typing import is_instance

__all__ = ("Editor", "get_time_length")

SPEED_TO_MAGIC = {
    Speed.SLOW: SpeedMagic.SLOW,
    Speed.NORMAL: SpeedMagic.NORMAL,
    Speed.FAST: SpeedMagic.FAST,
    Speed.FASTER: SpeedMagic.FASTER,
    Speed.FASTEST: SpeedMagic.FASTEST,
}

SPEED_CHANGE_TO_MAGIC = {
    SpeedChange.SLOW: SpeedMagic.SLOW,
    SpeedChange.NORMAL: SpeedMagic.NORMAL,
    SpeedChange.FAST: SpeedMagic.FAST,
    SpeedChange.FASTER: SpeedMagic.FASTER,
    SpeedChange.FASTEST: SpeedMagic.FASTEST,
}


def get_time_length(
    distance: float,
    start_speed: Speed = Speed.NORMAL,
    speed_changes: Iterable[Object] = (),
) -> float:
    """Computes the time (in seconds) to travel from `0` to `distance`, respecting speed portals.

    Parameters:
        distance: The distance to stop calculating at.
        start_speed: The starting speed (found in the header).
        speed_changes: Speed changes in the level, ordered by `x` position.

    Returns:
        The calculated time (in seconds).
    """
    magic = SPEED_TO_MAGIC[start_speed]

    if not speed_changes:
        return distance / magic

    last_x = 0.0
    total = 0.0

    for speed_change in speed_changes:
        x = speed_change.x

        if x > distance:
            break

        delta = x - last_x

        total += delta / magic

        magic = SPEED_CHANGE_TO_MAGIC[SpeedChange(speed_change.id)]

        last_x = x

    delta = distance - last_x

    total += delta / magic

    return total


DEFAULT_START = 1


def find_next(
    values: AbstractSet[int],
    start: int = DEFAULT_START,
) -> int:  # type: ignore
    for value in count(start):
        if value not in values:
            return value


DEFAULT_X = 0.0

X = "x"

get_x = get_attribute_factory(X)

E = TypeVar("E", bound="Editor")


@define()
class Editor(Sequence[Object]):
    header: Header = field(factory=Header)
    objects: List[Object] = field(factory=list)

    @classmethod
    def from_objects(cls: Type[E], *objects: Object, header: Header) -> E:
        return cls(header, list(objects))

    # callback

    @classmethod
    def from_object_iterable(cls: Type[E], objects: Iterable[Object], header: Header) -> E:
        return cls(header, list(objects))

    def __len__(self) -> int:
        return len(self.objects)

    @overload
    def __getitem__(self, index: int) -> Object:
        ...

    @overload
    def __getitem__(self: E, index: slice) -> E:
        ...

    def __getitem__(self: E, index: Union[int, slice]) -> Union[Object, E]:
        if is_instance(index, int):
            return self.objects[index]

        return self.from_object_iterable(self.objects[index], self.header)

    @property
    def color_channels(self) -> ColorChannels:
        return self.header.color_channels

    def set_header(self: E, header: Header) -> E:
        self.header = header

        return self

    def set_color_channels(self: E, color_channels: ColorChannels) -> E:
        self.header.color_channels = color_channels

        return self

    def iter_groups(self) -> Iterator[int]:
        for object in self.objects:
            yield from object.groups

            if has_target_group(object):
                yield object.target_group_id

    @property
    def groups(self) -> Set[int]:
        return set(self.iter_groups())

    @property
    def free_group(self) -> int:
        return find_next(self.groups)

    def iter_color_ids(self) -> Iterator[int]:
        for editor_object in self.objects:
            yield editor_object.base_color_id
            yield editor_object.detail_color_id

        yield from self.color_channels

    @property
    def color_ids(self) -> Set[int]:
        return set(self.iter_color_ids())

    @property
    def free_color_id(self) -> int:
        return find_next(self.color_ids)

    def iter_portals(self) -> Iterator[Object]:
        for object in self.objects:
            if object.is_portal():
                yield object

    @property
    def portals(self) -> List[Object]:
        return sorted(self.iter_portals(), key=get_x)

    def iter_speed_changes(self) -> Iterator[Object]:
        for object in self.objects:
            if object.is_speed_change():
                yield object

    @property
    def speed_changes(self) -> List[Object]:
        return sorted(self.iter_speed_changes(), key=get_x)

    def iter_triggers(self) -> Iterator[Object]:
        for object in self.objects:
            if object.is_trigger():
                yield object

    @property
    def triggers(self) -> List[Object]:
        return sorted(self.iter_triggers(), key=get_x)

    @property
    def x_length(self) -> float:
        return max(map(get_x, self.objects), default=DEFAULT_X)

    @property
    def start_speed(self) -> Speed:
        return self.header.speed

    @property
    def length(self, distance: Optional[float] = None) -> float:
        if distance is None:
            distance = self.x_length

        return get_time_length(distance, self.start_speed, self.speed_changes)

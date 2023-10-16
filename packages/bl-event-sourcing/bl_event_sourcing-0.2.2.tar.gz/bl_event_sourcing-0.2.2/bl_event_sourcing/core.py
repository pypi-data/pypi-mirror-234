# bl-event-sourcing --- Event sourcing library
# Copyright © 2021, 2022 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from datetime import datetime as DateTime
from datetime import timezone
from enum import Enum as Enumeration
from enum import auto
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Tuple

from bl_event_sourcing.utils import camel_to_snake


class IncompatibleVersions(Exception):
    pass


class EventNotHandled(Exception):
    def __init__(self, entity_name: str, event_name: str) -> None:
        super().__init__(
            f"Event not handled! [entity={entity_name}, event={event_name}]"
        )


@dataclass  # type: ignore
class DomainEvent(ABC):
    version: int

    @abstractproperty
    def id(self) -> str:
        ...


class Entity:
    PREFIX = "_apply_"
    _version: int

    def __init__(self, events: Sequence[DomainEvent]) -> None:
        self._version = 0
        for e in events:
            self._apply(e)

    def _apply(self, event: DomainEvent) -> None:
        """Apply an event and increment the aggregate version.

        An event is emitted by aggregate at a given version.
        It can only be applied to an aggregate at the same version.
        If history had to be rewritten, by removing or adding events,
        all the subsequent events should have their version modified.
        """
        if event.version != self._version:
            raise IncompatibleVersions(self._version, event.version)
        self._version = event.version + 1

        method_name = f"{self.PREFIX}{camel_to_snake(event.__class__.__name__)}"
        if method := getattr(self, method_name, None):
            method(event)
            return None
        raise EventNotHandled(self.__class__.__name__, event.__class__.__name__)


@dataclass
class Event:
    unixtime: int
    stream: str
    version: int  # Must be unique in a given stream
    name: str
    data: Dict[str, Any]
    id: Optional[int] = None  # Leave it to the event store

    @property
    def when(self) -> DateTime:
        return DateTime.fromtimestamp(self.unixtime, timezone.utc)


class EventStream(ABC):
    @abstractmethod
    def __iter__(self) -> Iterator[Event]:
        ...


class EventStore(ABC):
    @abstractmethod
    def record(self, event: Event) -> None:
        ...

    @abstractmethod
    def get_stream(
        self, name: str = "", start: int = 0, end: Optional[int] = None
    ) -> EventStream:
        ...

    @abstractmethod
    def last_position(self) -> int:
        ...


class Status(Enumeration):
    STALLED = auto()
    OK = auto()
    BROKEN = auto()
    RETIRED = auto()


class Ledger(ABC):
    """The Ledger keeps track of a projector's lifecycle.

    - NEW: never booted nor played
    - STALLED: ready to be booted
    - OK: successfully played
    - BROKEN: crashed while being played
    - RETIRED: never to be booted nor played again

    From <https://barryosull.com/blog/managing-projectors-is-harder-than-you-think/>.
    """

    class UnknownProjector(Exception):
        def __init__(self, name: str) -> None:
            super().__init__(f"Unknown projector [name={name}]")

    class ProjectorAlreadyRegistered(Exception):
        def __init__(self, name: str) -> None:
            super().__init__(f"Projector already registered [name={name}]")

    @abstractmethod
    def status(self, printer: Callable[[str, str, str], None]) -> bool:
        """Param.: status, name, position

        FIXME: This is not clear!! Pass a record instead?
        """
        ...

    @abstractmethod
    def knows(self, name: str) -> bool:
        ...

    @abstractmethod
    def register(self, name: str) -> None:
        ...

    @abstractmethod
    def forget(self, name: str) -> None:
        ...

    @abstractmethod
    def position(self, name: str) -> int:
        ...

    @abstractmethod
    def update_position(self, name: str, position: int) -> None:
        ...

    @abstractmethod
    def find(self, status: Optional[Status] = None) -> List[str]:
        ...

    @abstractmethod
    def mark_as(self, name: str, status: Status) -> None:
        ...


class Projector(ABC):
    def __init__(self, name: str, prefix: str = "when") -> None:
        self.__name = name
        # TODO: check that methods with this prefix exists
        self.__prefix = prefix
        self.logger = logging.getLogger(f"Projector/{name}")

    def register_to(self, register: Callable[[str, "Projector"], None]) -> None:
        if not self.__name:
            raise NotImplementedError("Projector needs a name!")
        register(self.__name, self)

    def boot(self, stream: EventStream) -> None:
        self.play(stream)

    def play(self, stream: EventStream) -> None:
        for event in stream:
            self.__when_event(event)

    def __when_event(self, event: Event) -> None:
        # Could be a decorator `@process("EventName")`.
        method_name = f"{self.__prefix}_{camel_to_snake(event.name)}"
        method = getattr(self, method_name, None)
        if method:
            self.logger.info(
                f"Processing event [projector={self.__class__.__name__}, "
                f"id={event.id}, name={event.name}]"
            )
            self.logger.debug(f"Data = {event.data}")
            method(event.when, event.data)


class RunFromBeginningProjector(Projector):
    """Plays all the events during the boot phase then keep on playing new ones.

    Used, for instance, to populate a projection.
    """

    pass


class RunFromNowProjector(Projector):
    """Skips the boot phase then play all the events as usual.

    Used, for instance, to send email notifications from now on.
    """

    def boot(self, stream: EventStream) -> None:
        pass


class RunOnceProjector(Projector):
    """Plays existing events during the boot phase then does not play anymore.

    Used, for instance, to add new events to the store based on the old ones.
    """

    def boot(self, stream: EventStream) -> None:
        super().play(stream)

    def play(self, stream: EventStream) -> None:
        # FIXME This will mark the projector as broken!
        #       It will be marked as stalled and played during
        #       the next boot phase!
        #       It should be marked as being retired or something!
        raise Exception("RunOnceProjector cannot play after boot!")


class ProjectorRegistry:
    def __init__(self, projectors: Sequence[Projector]) -> None:
        self.__projectors: List[Tuple[str, Projector]] = []
        for p in projectors:
            p.register_to(self.__register_projector)

    def __register_projector(self, name: str, projector: Projector) -> None:
        self.__projectors.append((name, projector))

    def __iter__(self) -> Iterator[Tuple[str, Projector]]:
        for n, p in self.__projectors:
            yield n, p

    def __getitem__(self, name: str) -> Projector:
        for n, p in self.__projectors:
            if n == name:
                return p
        raise KeyError(f"Projector has not been registered! [name={name}]")

    def __contains__(self, name: str) -> bool:
        for n, p in self.__projectors:
            if n == name:
                return True
        return False


class Projectionist:
    def __init__(
        self,
        event_store: EventStore,
        ledger: Ledger,
        projectors: ProjectorRegistry,
    ) -> None:
        self.__logger = logging.getLogger("Projectionist")
        self.__event_store = event_store
        self.__ledger = ledger
        self.__projectors = projectors
        self.__last_seen_position = 0

    def boot(self) -> None:
        self.__mark_new_projectors_as_stalled()
        self.__mark_broken_as_stalled()
        self.__boot_stalled_projectors()

    def __mark_new_projectors_as_stalled(self) -> None:
        for n, p in self.__projectors:
            if not self.__ledger.knows(n):
                self.__ledger.register(n)

    def __mark_broken_as_stalled(self) -> None:
        for name in self.__ledger.find(Status.BROKEN):
            self.__ledger.mark_as(name, Status.STALLED)

    def __boot_stalled_projectors(self) -> None:
        last_seen_position = self.__event_store.last_position()
        for name in self.__ledger.find(Status.STALLED):
            self.__boot_projector(name, until=last_seen_position)

    def __boot_projector(self, name: str, until: int) -> None:
        try:
            position = self.__ledger.position(name)
            stream = self.__event_store.get_stream(start=position, end=until)
            projector = self.__projectors[name]
            projector.boot(stream)
            self.__ledger.mark_as(name, Status.OK)
            self.__ledger.update_position(name, until)
        except Exception as exc:
            self.__ledger.mark_as(name, Status.BROKEN)
            self.__logger.error(exc)

    def play(self) -> None:
        # TODO: should play manage sleep intervals?!
        #       It's easier to test if it doesn't.
        last_seen_position = self.__event_store.last_position()
        if last_seen_position > self.__last_seen_position:
            for name in self.__ledger.find(Status.OK):
                if name in self.__projectors:
                    self.__play_projector(name, until=last_seen_position)
            self.__last_seen_position = last_seen_position

    def __play_projector(self, name: str, /, *, until: int) -> None:
        try:
            position = self.__ledger.position(name)
            stream = self.__event_store.get_stream(start=position, end=until)
            projector = self.__projectors[name]
            projector.play(stream)
            self.__ledger.update_position(name, until)
        except Exception as exc:
            self.__ledger.mark_as(name, Status.BROKEN)
            self.__logger.error(exc)

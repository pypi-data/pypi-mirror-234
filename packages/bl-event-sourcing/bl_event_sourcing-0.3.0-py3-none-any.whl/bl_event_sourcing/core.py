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

"""
Classes required to implement event sourcing.

@see <https://barryosull.com/blog/projection-building-blocks-what-you-ll-need-to-build-projections/>  # noqa

**TODO** rename `__init__` once `ddd` has been extracted.

## Life cycle


### Reading

- EVENT_STORE returns, for a given stream, an ordered list of
- EVENT [id, unique(stream, version), name, data, when]
- HISTORY converts (switch on `name`, pass `**data` to constructor) them to
- DOMAIN_EVENT
- REPOSITORY instanciate
- AGGREGATE
  * by passing domain events to the constructor;
  * only accepts domain events with `version` greater than its current version.


### Writing

- AGGREGATE emits a sequence (incremental version numbers) of
- DOMAIN_EVENT written to
- HISTORY which converts them to
- EVENT which are persisted to
- EVENT_STORE that does **not** accept events with the same (emitted_at_)version numbers
  for a given stream
"""

import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime as DateTime
from datetime import timezone
from enum import Enum as Enumeration
from enum import auto
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Tuple

from .ddd import DomainEvent
from .ddd import History as DomainEventHistory
from .utils import camel_to_snake


@dataclass(frozen=True)
class Event:
    unixtime: int
    stream: str
    version: int  # Must be unique in a given stream
    name: str
    data: Dict[str, Any]

    @property
    def when(self) -> DateTime:
        return DateTime.fromtimestamp(self.unixtime, timezone.utc)


class EventStream(ABC):
    """Represents a sequence of events.

    Contains event upgraders if they are required. They transform
    events from an older format to the current one.
    """

    @abstractmethod
    def __iter__(self) -> Iterator[Event]:
        ...


class EventStore(ABC):
    """Records and loads events for a given stream, starting from a given position…"""

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


class History(DomainEventHistory):
    EVENT_MODULE = sys.modules[__name__]

    class EvenNotHandled(NotImplementedError):
        def __init__(self, name: str) -> None:
            super().__init__(f"History cannot handle event `{name}`!")

    class ReadError(AttributeError):
        def __init__(self, name: str, data: dict[str, Any]) -> None:
            super().__init__(f"Cannot read event's data `{name}`: {data}")

    def __init__(self, event_store: EventStore, now: Callable[[], DateTime]) -> None:
        self.__store = event_store
        self.__now = now

    def read(self, stream: str) -> list[DomainEvent]:
        return [self.__event(e) for e in self.__store.get_stream(name=stream)]

    def __event(self, event: Event) -> DomainEvent:
        try:
            class_ = getattr(self.EVENT_MODULE, event.name)
            return class_(  # type: ignore
                # FIXME how is the `id_xxx` set?! Is it?!
                **event.data,
                version=event.version,
            )
        except AttributeError:
            raise History.EvenNotHandled(event.name)
        except TypeError:
            raise History.ReadError(event.name, event.data)

    def __lshift__(self, domain_events: list[DomainEvent]) -> None:
        for e in domain_events:
            self.__store.record(
                Event(
                    unixtime=int(self.__now().timestamp()),
                    stream=e.entity_unique_identifier,
                    version=e.version,
                    name=e.__class__.__name__,
                    data=self.__event_as_dict(e),
                )
            )

    def __event_as_dict(self, domain_event: DomainEvent) -> dict[str, Any]:
        data = asdict(domain_event)
        del data["version"]
        return data


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
    """Parses event's data and calls the proper projection method.

    Projectors exist in different types, that implement `boot` and `play` differently.
    """

    class EventHandlerCrashed(Exception):
        def __init__(self, method_name: str, exception: Exception) -> None:
            super().__init__(
                "Event handler raised an exception! "
                f"[handler: {method_name}, "
                f"exception: {exception.__class__.__name__}, "
                f"message: {exception}]"
            )

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
                f"stream={event.stream}, version={event.version}, "
                f"name={event.name}]"
            )
            self.logger.debug(f"Data = {event.data}")
            try:
                method(event.when, event.data)
            except Exception as exc:
                raise Projector.EventHandlerCrashed(method_name, exc)


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
    """In charge of booting and running all the registered projectors."""

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
            self.__logger.error(
                "Error while booting projector! "
                f"[projector={name}, error={exc.__class__.__name__}, "
                f"message={exc}]"
            )

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
            self.__logger.error(
                "Error while playing projector! "
                f"[projector={name}, error={exc.__class__.__name__}, "
                f"message={exc}]"
            )


class Projection:
    """A "point of view" on the data.

    They contain methods to write data to the chosen storage
    (SQL, no-SQL, in-memory…) and methods to query the data back.
    """

    pass

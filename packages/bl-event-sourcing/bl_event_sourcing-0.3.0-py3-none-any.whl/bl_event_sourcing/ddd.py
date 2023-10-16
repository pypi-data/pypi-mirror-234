# bl-event-sourcing --- Event sourcing library
# Copyright © 2022 Bioneland
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
**TODO** move to a dedicated package.
"""

from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import Any


class Entity(ABC):
    """
    An entity represents a domain concept with an identity.

    They have methods that implement business rules and behaviour.
    Those methods mutate the state of the entity and emit events
    reflecting the changes.

    In Python, there is no way to "emit" events, so they are returned
    by the methods. But they are not, so to speak, return values.
    """

    pass


@dataclass(frozen=True)
class EntityState(ABC):
    """Represents the state of an entity.

    A new state is created by applying an domain event to it.
    """

    class UnknownEvent(Exception):
        pass

    class IncompatibleVersions(Exception):
        pass

    version: int


@dataclass(frozen=True)  # type: ignore
class DomainEvent(ABC):
    """Represents an event that happened in the domain."""

    version: int

    @abstractproperty
    def entity_unique_identifier(self) -> str:
        """
        An identifier that uniquely identifies the entity
        that emitted the domain event.
        """
        ...


class History(ABC):
    """Represents a sequence of events that happened inside the domain."""

    class EvenNotHandled(NotImplementedError):
        def __init__(self, name: str) -> None:
            super().__init__(f"History cannot handle event `{name}`!")

    class ReadError(AttributeError):
        def __init__(self, name: str, data: dict[str, Any]) -> None:
            super().__init__(f"Cannot read event's data `{name}`: {data}")

    @abstractmethod
    def read(self, stream: str) -> list[DomainEvent]:
        ...

    @abstractmethod
    def __lshift__(self, domain_events: list[DomainEvent]) -> None:
        ...

# bl-event-sourcing-sqlalchemy --- Event sourcing implemented with SQLAlchemy
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

from dataclasses import asdict, dataclass
from typing import Any, Callable, Iterator, List, Optional

from bl_event_sourcing.core import Event
from bl_event_sourcing.core import EventStore as EventStoreInterface
from bl_event_sourcing.core import EventStream as EventStreamInterface
from bl_event_sourcing.core import Ledger as LedgerInterface
from bl_event_sourcing.core import Status
from sqlalchemy import (  # type: ignore
    JSON,
    Column,
    Enum,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import Query, Session, registry  # type: ignore


@dataclass
class Record:
    name: str
    status: Status
    position: int


class Ledger(LedgerInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def __record(self, name: str) -> Record:
        if record := self.__session.query(Record).filter(Record.name == name).first():
            return record  # type: ignore
        raise Ledger.UnknownProjector(name)

    def status(self, printer: Callable[[str, str, str], None]) -> bool:
        for i in self.__session.query(Record).all():
            printer(i.status.name, i.name, i.position)
        return True

    def knows(self, name: str) -> bool:
        try:
            _ = self.__record(name)
            return True
        except Exception:
            return False

    def register(self, name: str) -> None:
        if self.knows(name):
            raise Ledger.ProjectorAlreadyRegistered(name)
        self.__session.add(Record(name, Status.STALLED, 0))

    def forget(self, name: str) -> None:
        try:
            self.__session.delete(self.__record(name))
        except Ledger.UnknownProjector:
            pass

    def position(self, name: str) -> int:
        return self.__record(name).position

    def update_position(self, name: str, position: int) -> None:
        self.__record(name).position = position

    def find(self, status: Optional[Status] = None) -> List[str]:
        query = self.__session.query(Record)
        if status:
            query = query.filter(Record.status == status)
        return [r.name for r in query.all()]

    def mark_as(self, name: str, status: Status) -> None:
        self.__record(name).status = status


@dataclass
class PersistableEvent:
    unixtime: int
    stream: str
    version: int  # Must be unique in a given stream
    name: str
    data: dict[str, Any]
    id: Optional[int] = None


class EventStream(EventStreamInterface):
    def __init__(self, query: Query) -> None:
        self.__query = query

    def __iter__(self) -> Iterator[Event]:
        return (self.__from_persistable_event(event) for event in self.__query)

    def __from_persistable_event(self, event: PersistableEvent) -> Event:
        data = asdict(event)
        del data["id"]
        return Event(**data)


class EventStore(EventStoreInterface):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def record(self, event: Event) -> None:
        self.__session.add(PersistableEvent(**asdict(event)))

    def last_position(self) -> int:
        event = (
            self.__session.query(PersistableEvent)
            .order_by(events_table.c.id.desc())
            .limit(1)
            .first()
        )
        if event:
            return int(event.id)
        return 0

    def get_stream(
        self, name: str = "", start: int = 0, end: Optional[int] = None
    ) -> EventStream:
        """Get a stream from start (excluded) to end (included)."""
        query = self.__session.query(PersistableEvent)
        assert PersistableEvent.id
        if name:
            query = query.filter(PersistableEvent.stream == name)
        if start:
            query = query.filter(PersistableEvent.id > start)
        if end is not None:
            query = query.filter(PersistableEvent.id <= end)
        query = query.order_by(events_table.c.id)

        return EventStream(query)


EVENT_REGISTRY = registry()
events_table = Table(
    "events",
    EVENT_REGISTRY.metadata,
    Column("id", Integer, primary_key=True),
    Column("unixtime", Integer),
    Column("stream", String(36)),
    Column("version", Integer),
    Column("name", String(99)),
    Column("data", JSON),
    UniqueConstraint("stream", "version", name="stream_version"),
)
EVENT_REGISTRY.map_imperatively(PersistableEvent, events_table)

LEDGER_REGISTRY = registry()
ledger_records_table = Table(
    "ledger_records",
    LEDGER_REGISTRY.metadata,
    Column("name", String(50), primary_key=True),
    Column("status", Enum(Status)),
    Column("position", Integer),
)
LEDGER_REGISTRY.map_imperatively(Record, ledger_records_table)

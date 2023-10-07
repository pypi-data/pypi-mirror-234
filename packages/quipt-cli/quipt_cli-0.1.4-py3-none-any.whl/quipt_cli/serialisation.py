from __future__ import annotations
from uuid import uuid4
import attrs
from enum import IntEnum

all_actors = object()

class ItemType(IntEnum):
    DIVISION = 0
    TRIGGER = 1
    QUOTE = 2

@attrs.define
class SemanticString:
    byte_length: int
    division_count: int
    divisions: list[tuple[bool, str]]

@attrs.define
class Quote:
    actor_id: list[int]
    content: SemanticString

@attrs.define
class Trigger:
    uuid: bytes
    request_type: ItemType
    request: Quote | int
    response: Quote

@attrs.define
class OverviewTableItem:
    item_type: ItemType
    item: Trigger | str | int

@attrs.define
class File:
    actor_count: int
    actors: list[str]
    tbl_count: int
    overview_talbe: list[OverviewTableItem]

class Serializer:
    def __init__(self, others, _self) -> None:
        self.others: set[str] = others
        self.self_actor: str = _self
        self.all_actors = [*sorted(others), _self]
        self.items: list[OverviewTableItem] = []
        self.divisions = 0

    def new_division(self, name: str):
        self.items.append(OverviewTableItem(ItemType.DIVISION, name))
        self.divisions += 1

    def new_trigger(
            self,
            *,
            type: ItemType,
            content: list[tuple[bool, str]] | None = None,
            actors: set[str] | None = None,
            name: str | None = None,
            response: Quote
        ) -> Trigger:
        match type:
            case ItemType.TRIGGER:
                assert content is not None and actors is not None, "invalid calling convention" 
                request = self.quote_from_syntax(content, actors)
                type = ItemType.QUOTE
            case ItemType.DIVISION:
                assert name is not None, "invalid calling convention"
                self.items.append(OverviewTableItem(ItemType.DIVISION, name))
                request = self.divisions
                self.divisions += 1
            case _:
                assert False, "unreachable"

        uuid = uuid4()
        trigger = Trigger(uuid.bytes, type, request, response)
        self.items.append(OverviewTableItem(ItemType.TRIGGER, trigger))
        return trigger

    def quote_from_syntax(self, content: list[tuple[bool, str]], actors: set[str]) -> Quote:
        actor_id = []
        if actors is all_actors:
            actor_id = all_actors 
        else:
            for actor in actors:
                try:
                    idx = self.all_actors.index(actor) + 1
                except ValueError:
                    assert False, "invalid operation"
                if idx >= 0xff:
                    assert False, "to many actors"
                actor_id.append(idx)
        return Quote(actor_id, SemanticString(-1, len(content), content))

    def serialize_string(self, buffer: bytearray, string: str) -> int:
        bstring = string.encode()
        buffer.extend(bstring)
        buffer.append(0)
        return len(bstring) + 1

    def serialize_division(self, buffer: bytearray, division: tuple[bool, str]) -> int:
        italic, text = division
        buffer.append(italic)
        return self.serialize_string(buffer, text) + 1

    def serialize_semantic_str(self, buffer: bytearray, string: SemanticString) -> int:
        ibuff = bytearray()
        ibuff.extend(string.division_count.to_bytes(4, byteorder='little'))
        length = 4
        for division in string.divisions:
            length += self.serialize_division(ibuff, division)

        length += 4
        buffer.extend(len(ibuff).to_bytes(4, byteorder='little'))
        buffer.extend(ibuff)

        return length

    def serialize_quote(self, buffer: bytearray, quote: Quote) -> int:
        length = 0
        if quote.actor_id is all_actors:
            buffer.append(0xff)
            length += 1
        else:
            for actor_id in quote.actor_id:
                buffer.append(actor_id)
                length += 1
            buffer.append(0)
            length += 1
        length += self.serialize_semantic_str(buffer, quote.content)
        return length

    def serialize_trigger(self, buffer: bytearray, trigger: Trigger) -> int:
        assert len(trigger.uuid) == 16, "invalid trigger data"
        buffer.extend(trigger.uuid)
        buffer.append(trigger.request_type.value)
        length = 16 + 1
        match trigger.request_type:
            case ItemType.DIVISION:
                buffer.append(trigger.request)
                length += 1
            case ItemType.QUOTE:
                length += self.serialize_quote(buffer, trigger.request)
        length += self.serialize_quote(buffer, trigger.response)
        return length

    def serialize_triggers(self) -> bytearray:
        buffer = bytearray()
        current_pos = 0
        for item in self.items:
            if item.item_type != ItemType.TRIGGER:
                continue
            length = self.serialize_trigger(buffer, item.item)
            item.item = current_pos
            current_pos += length
        return buffer

    def serialize_file(self, file: File, triggers: bytearray) -> bytearray:
        buffer = bytearray()
        buffer.append(file.actor_count)
        for actor in file.actors:
            self.serialize_string(buffer, actor)
        reversed_buffer = bytearray()
        position = 0
        for item in reversed(self.items):
            if item.item_type == ItemType.DIVISION:
                sbuff = bytearray()
                position += self.serialize_string(sbuff, item.item)
                reversed_buffer.extend(reversed(sbuff))
            else:
                reversed_buffer.extend((item.item + position + 4).to_bytes(4, byteorder='big'))
                position += 4
            reversed_buffer.append(item.item_type)
            position += 1
        buffer.extend(file.tbl_count.to_bytes(4, byteorder='little'))
        reversed_buffer.reverse()
        buffer.extend(reversed_buffer)
        buffer.extend(triggers)
        return buffer
    
    @classmethod
    def from_file(cls, file: File) -> Serializer: 
        rv = cls(set(), '')
        rv.all_actors = file.actors
        rv.items = file.overview_talbe
        for item in rv.items:
            if item.item_type == ItemType.DIVISION:
                rv.divisions += 1
        return rv

    @property
    def file(self) -> File:
        return File(
            len(self.all_actors),
            self.all_actors,
            len(self.items),
            self.items
        )

    def save(self, save_file_path: str):
        file = File(
            len(self.all_actors),
            self.all_actors,
            len(self.items),
            self.items
        )
        serialized_triggers = self.serialize_triggers()
        sfile = self.serialize_file(file, serialized_triggers)
        with open(save_file_path, 'wb') as save_file:
            save_file.write(sfile)

class DeserializationError(Exception):
    pass

class Deserializer:
    def __init__(self):
        self.deserializer_pos = 0

    def deserialize_cstring(self, contents: bytes) -> tuple[int, str]:
        idx = contents.find(b'\x00')
        if idx == -1:
            raise DeserializationError("WTF?")
        try:
            string = contents[:idx].decode()
        except UnicodeDecodeError:
            raise DeserializationError("Invalid utf8")
        return idx + 1, string

    def deserialize_actors(self, contents: bytes) -> list[str]:
        actor_count = contents[0]
        length = 1
        actors = []
        for _ in range(actor_count):
            size, string = self.deserialize_cstring(contents[length:])
            length += size
            actors.append(string)
        self.deserializer_pos = length
        return actors

    def deserialize_semantic_str(self, contents: bytes) -> tuple[int, SemanticString]:
        byte_length = int.from_bytes(contents[:4], byteorder='little')
        length = 4
        division_count = int.from_bytes(contents[length:length + 4], byteorder='little')
        length += 4
        divisions: list[tuple[bool, str]] = []
        for _ in range(division_count):
            italic = bool(contents[length])
            length += 1
            size, text = self.deserialize_cstring(contents[length:])
            length += size
            divisions.append((italic, text))
        return length, SemanticString(byte_length, division_count, divisions)

    def deserialize_quote(self, contents: bytes) -> tuple[int, Quote]:
        length = 0
        if contents[0] == 0xff:
            length = 1
            actor_ids = all_actors
        else:
            idx = contents.find(b'\x00')
            actor_ids = list(contents[:idx])
            length = idx + 1
        size, sstring = self.deserialize_semantic_str(contents[length:])
        length += size
        return length, Quote(actor_ids, sstring)

    def deserialize_trigger(self, contents: bytes) -> Trigger:
        uuid = contents[:16]
        length = 16
        request_type = ItemType(contents[length])
        length += 1
        if request_type == ItemType.DIVISION:
            request = contents[length]
            length += 1
        elif request_type == ItemType.QUOTE:
            size, request = self.deserialize_quote(contents[length:])
            length += size
        _, response = self.deserialize_quote(contents[length:])
        return Trigger(uuid, request_type, request, response)

    def deserialize_table(self, contents: bytes) -> list[OverviewTableItem]:
        contents = contents[self.deserializer_pos:]
        tbl_count = int.from_bytes(contents[:4], byteorder='little')
        length = 4

        table: list[OverviewTableItem] = []
        for _ in range(tbl_count):
            item_type = ItemType(contents[length])
            length += 1
            if item_type == ItemType.DIVISION:
                size, item = self.deserialize_cstring(contents[length:])
                length += size
            elif item_type == ItemType.TRIGGER:
                quote_pos = int.from_bytes(contents[length:length + 4], byteorder='little')
                item = self.deserialize_trigger(contents[length + quote_pos:])
                length += 4
            table.append(OverviewTableItem(item_type, item))

        return table

    def load(self, load_file_path: str):
        with open(load_file_path, 'rb') as load_file:
            contents = load_file.read()
        actors = self.deserialize_actors(contents)
        table = self.deserialize_table(contents)
        return File(
            len(actors),
            actors,
            len(table),
            table
        )


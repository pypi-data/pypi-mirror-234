from __future__ import annotations
import re
import os
import shutil
import sys
import mmh3
import yaml
import difflib
import dataclasses

from uuid import UUID, uuid4
from enum import IntEnum
from typing import Any, Generator, Iterator, TextIO 
from rich import print as rprint

from .serialisation import Deserializer, File, ItemType, SemanticString, Serializer, Trigger, all_actors, OverviewTableItem, Quote as TQuote

TOKENS = [
    '[', ']', '(', ')', '\n', '\\', '#'
]

class TokenType(IntEnum):
    BRACKET = 0
    PARENTHESIS = 1
    NEWLINE = 2
    ESCAPE_CHR = 3
    TEXT = 4
    DIRECTIVE = 5
    EOF = 6

    @classmethod
    def from_char(cls, chr):
        match chr:
            case '[' | ']':
                return TokenType.BRACKET
            case '(' | ')':
                return TokenType.PARENTHESIS
            case '\n':
                return TokenType.NEWLINE
            case '\\':
                return TokenType.ESCAPE_CHR
            case '#':
                return TokenType.DIRECTIVE


@dataclasses.dataclass
class Token:
    start: int
    end: int
    lineno: int
    type: TokenType
    data: str


def _craft_re():
    return re.compile('|'.join(re.escape(t) for t in TOKENS))


def tokenize(input):
    token_re = _craft_re()
    current_pos = 0
    lineno = 1
    while True:
        m = token_re.search(input, pos=current_pos)
        if not m:
            break
        if m.start() > current_pos:
            yield Token(current_pos, m.start(), lineno, TokenType.TEXT, input[current_pos:m.start()])
        current_pos = m.end()
        token_chr = input[m.start():m.end()]
        token_type = TokenType.from_char(token_chr)
        if token_type == TokenType.NEWLINE:
            lineno += 1
        yield Token(m.start(), m.end(), lineno, token_type, token_chr)
    yield Token(current_pos, current_pos, lineno, TokenType.EOF, '')


class ParserError(Exception):
    def __init__(self, message: str, lineno: int):
        self.message = message
        self.lineno = lineno
        super().__init__(f"{message}; at line {lineno}")


@dataclasses.dataclass
class Quote:
    lineno: int
    actor: str
    content: list[tuple[bool, str]]

@dataclasses.dataclass
class SelfDeclaration:
    lineno: int
    name: str

@dataclasses.dataclass
class OthersDefinition:
    lineno: int
    others: list[str]

@dataclasses.dataclass
class DivisionNotation:
    lineno: int
    name: str

class Parse:

    def __init__(self, token_stream):
        self.token_stream: Iterator[Token] = token_stream
        self.hit_content = False

    def expect(self, *, type: TokenType = None, data: str = None):
        token = next(self.token_stream)
        if type and token.type != type:
            raise ParserError(f"Expected token {type.name}, got {token.type.name}", token.lineno)
        if data and token.data != data:
            raise ParserError(f"Expected {data!r}, got {token.data!r}", token.lineno)
        return token

    def self_directive(self, lineno, name):
        if self.hit_content:
            raise ParserError("Directive 'self' has to be written at the top level of a script", lineno)
        return SelfDeclaration(lineno, name)

    def others_directive(self, lineno, names_string: str):
        if self.hit_content:
            raise ParserError("Directive 'others' has to be written at the top level of a script", lineno)
        others = [name.strip() for name in names_string.split(',')]
        if len(min(others, key=len)) < 1:
            raise ParserError("Directive 'others' contains a syntax error", lineno)
        return OthersDefinition(lineno, others)

    def division_directive(self, lineno, name):
        self.hit_content = True
        return DivisionNotation(lineno, name)

    def parse_directive(self):
        content = self.expect(type=TokenType.TEXT)
        self.expect(type=TokenType.NEWLINE)
        directive, remainder = content.data.split(' ', maxsplit=1)
        if (function := getattr(self, f"{directive}_directive", None)) is not None:
            return function(content.lineno, remainder)
        raise ParserError(f"Unknown directive {directive!r}", content.lineno)

    def parse_quote(self):
        self.hit_content = True

        actor = self.expect(type=TokenType.TEXT)
        self.expect(type=TokenType.BRACKET, data=']')
        self.expect(type=TokenType.NEWLINE)

        content = [] 
        break_on_newline = False
        italic_mode = False
        while True:
            token = next(self.token_stream)
            if break_on_newline:
                if token.type == TokenType.NEWLINE:
                    break
                else:
                    break_on_newline = False
            match token:
                case Token(type=TokenType.PARENTHESIS):
                    if token.data in ('[', ']'):
                        raise ParserError(f"Unexpected {token.data!r} in the body of a Quest", token.lineno)
                    if token.data == '(' and italic_mode: # )
                        raise ParserError("Italic text is not nestible", lineno=token.lineno)
                    if token.data == ')' and not italic_mode:
                        raise ParserError("Nothing to close at level 0", lineno=token.lineno)
                    italic_mode = not italic_mode
                case Token(type=TokenType.TEXT):
                    content.append((italic_mode, token.data))
                case Token(type=TokenType.ESCAPE_CHR):
                    content.append((italic_mode, next(self.token_stream).data))
                case Token(type=TokenType.NEWLINE):
                    content.append((italic_mode, ' '))
                    break_on_newline = True
        
        if italic_mode:
            raise ParserError("Italic text was never closed", token.lineno)
        # self.expect(type=TokenType.NEWLINE)

        return Quote(actor.lineno, actor.data, list(simplify(content)))

    def parse(self):
        while True:
            token = next(self.token_stream)
            match token:
                case Token(type=TokenType.BRACKET):
                    yield self.parse_quote()
                case Token(type=TokenType.DIRECTIVE):
                    yield self.parse_directive()
                case Token(type=TokenType.EOF):
                    break

class Database:
    script_id: UUID

    def __init__(self, database_path: str, play_name: str):
        assert os.path.isdir(database_path)
        self.database_path = database_path
        self.play_name = play_name
        self.history_file_path = os.path.join(self.database_path, "history.yml")
        self.this_history: list[str] = []

    @property
    def actors(self) -> list[str]:
        if "actors" in self.__dict__:
            return self.__dict__["actors"]
        actors = getattr(self.serialized_file, "actors", [])
        self.__dict__["actors"] = actors
        return actors

    @property
    def divisions(self) -> list[str]:
        if "divisions" in self.__dict__:
            return self.__dict__["divisions"]
        table: list[OverviewTableItem] = getattr(self.serialized_file, "overview_talbe", [])
        divisions: list[str] = [] 
        for item in table:
            if item.item_type == ItemType.DIVISION:
                divisions.append(item.item)
        self.__dict__["divisions"] = divisions
        return divisions

    @property
    def history(self) -> list[dict]:
        if "history" in self.__dict__:
            return self.__dict__["history"]

        if not os.path.isfile(self.history_file_path):
            result = []
        else:
            with open(self.history_file_path) as history_file:
                data = yaml.safe_load(history_file)

            assert data["type"] == "quipt-version-control"
            self.__dict__["script_id"] = UUID(data["script"])

            result: list = data["history"]
            result.sort(key=lambda x: x["version"])

        self.__dict__["history"] = result
        return result

    @property
    def most_recent_version_path(self) -> str | None:
        if len(self.history) == 0:
            return None
        return os.path.join(self.database_path, self.history[-1]["filename"])

    @property
    def most_recent_version(self) -> int:
        if len(self.history) == 0:
            return 0
        return self.history[-1]["version"]

    @property
    def serialized_file(self) -> File | None:
        if "serialized_file" in self.__dict__:
            return self.__dict__["serialized_file"]
        if self.most_recent_version_path is None:
            _serialized_file = None
        else:
            dser = Deserializer()
            _serialized_file = dser.load(self.most_recent_version_path)
        self.__dict__["serialized_file"] = _serialized_file
        return _serialized_file 

    @classmethod
    def open(cls, database_location: str, play_name: str) -> Database | None:
        database_path = os.path.join(database_location, f"{play_name}.db")
        if not os.path.exists(database_path):
            return None
        if not os.path.isdir(database_path):
            raise ValueError("Database can't point to a not-directory")
        return cls(database_path, play_name)


    @classmethod
    def create_new(cls, database_location: str, play_name: str, new_file: File) -> tuple[UUID, str]:
        database_path = os.path.join(database_location, f"{play_name}.db")
        if os.path.exists(database_path):
            raise ValueError("Database already exists")
        os.makedirs(database_path, exist_ok=True)
        script_id = uuid4()

        changes: list[str] = []
        for item in new_file.overview_talbe:
            match item.item_type:
                case ItemType.DIVISION:
                    item_description = f"Division {item.item!r}"
                case _:
                    item_description = f"Trigger {UUID(bytes=item.item.uuid)!r}"
            changes.append(item_description)

        version = 0
        filename = f"./{play_name}-v{version:03d}.pv"
        history = [{
            "filename": filename,
            "version": version,
            "pushed": False,
            "changes": changes
        }] 
        resulting_yaml = {
            "type": "quipt-version-control",
            "script": str(script_id),
            "history": history
        }

        history_file_path = os.path.join(database_path, "history.yml")
        with open(history_file_path, 'w') as history_file:
            yaml.safe_dump(resulting_yaml, history_file)

        return script_id, os.path.join(database_path, filename)


    def add_actor(self, actor: str, all_actors: list[str]):
        rprint(f"Added Actor: [yellow]{actor!r}[/]")
        self.this_history.append(f"Actor Added: {actor!r}")
        self.__dict__['actors'] = all_actors

    def remove_actor(self, actor: str, all_actors: list[str]):
        rprint(f"Removed Actor: [yellow]{actor!r}[/]")
        self.this_history.append(f"Actor Removed: {actor!r}")
        self.__dict__['actors'] = all_actors

    def replace_item_compare(self, old_item: OverviewTableItem, new_item: OverviewTableItem) -> bool:
        if old_item.item_type == ItemType.DIVISION:
            rprint(f"Renamed Division from [yellow]{old_item.item!r}[/] to [yellow]{new_item.item!r}[/]")

            old_div_name = old_item.item.replace(' ', '\x1b')
            new_div_name = new_item.item.replace(' ', '\x1b')
            self.this_history.append(
                    f"Changed Division from {old_div_name} to {new_div_name}")
            return True
        else:
            old_trigger: Trigger = old_item.item
            new_trigger: Trigger = new_item.item
            changed = set()

            if old_trigger.request_type != new_trigger.request_type:
                return False

            old_actors = '->'.join(trigger_get_actor_string(old_trigger, self.actors))
            new_actors = '->'.join(trigger_get_actor_string(new_trigger, self.actors))
            if old_actors != new_actors:
                changed.add('actors')

            old_content_tpl = trigger_get_content_string(old_trigger, self.divisions)
            new_content_tpl = trigger_get_content_string(new_trigger, self.divisions)
            for old_content, new_content in zip(old_content_tpl, new_content_tpl):
                matcher = difflib.SequenceMatcher(None, old_content, new_content)
                if matcher.quick_ratio() < 0.50:
                    return False
                if old_content != new_content:
                    changed.add('content')

            uuid = UUID(bytes=old_trigger.uuid)
            rprint(f"Trigger Changed: [italic green]{uuid}[/]")
            if 'content' in changed:
                for old_content, new_content in zip(old_content_tpl, new_content_tpl):
                    old_content = old_content.split()
                    new_content = new_content.split()
                    differ = difflib.Differ()
                    for word in differ.compare(old_content, new_content):
                        if word.startswith('?'):
                            print(f"  {word}")
                        if word.startswith('+'):
                            rprint(f"  [green]{word}[/]")
                        if word.startswith('-'):
                            rprint(f"  [red]{word}[/]")
            if 'actors' in changed:
                rprint(f"Changed Actors from [yellow]{old_actors}[/] to [yellow]{new_actors}[/]")

            self.this_history.append(f"Changed Trigger {uuid}")
            return True

    def insert(self, oitem: OverviewTableItem, prev: str):
        if oitem.item_type == ItemType.DIVISION:
            rprint(f"Inserted Division: [yellow]{oitem.item!r}[/]")
            self.this_history.append(
                    f"Inserted Division {oitem.item.replace(' ', chr(0x1b))} after {prev}")
        elif oitem.item_type == ItemType.TRIGGER:
            trigger: Trigger = oitem.item
            uuid = UUID(bytes=trigger.uuid)
            request_actor, response_actor = trigger_get_actor_string(trigger, self.actors)

            self.this_history.append(f"Inserted Trigger {uuid} after {prev}")
            rprint(f"Inserted Trigger: [italic green]{uuid}[/]")
            rprint(f"  {request_actor}[yellow]->[/]{response_actor}")
            rprint(f"  [italic]{trigger.response.content.divisions[0][1][:22]}[/]...") 
    
    def delete(self, oitem: OverviewTableItem):
        if oitem.item_type == ItemType.DIVISION:
            self.this_history.append(f"Deleted Division {oitem.item.replace(' ', chr(0x1b))}")
            rprint(f"Delted Division: [yellow]{oitem.item!r}[/]")
        elif oitem.item_type == ItemType.TRIGGER:
            trigger: Trigger = oitem.item
            uuid = UUID(bytes=trigger.uuid)
            request_actor, response_actor = trigger_get_actor_string(trigger, self.actors)

            self.this_history.append(f"Deleted Trigger {uuid}")
            rprint(f"Deleted Trigger: [italic green]{uuid}[/]")
            rprint(f"  {request_actor}[yellow]->[/]{response_actor}")
            rprint(f"  [italic]{trigger.response.content.divisions[0][1][:22]}[/]...")

    def write_pushed(self):
        resulting_yaml = {
            "type": "quipt-version-control",
            "history": self.history,
            "script": str(self.script_id)
        }

        self.history[-1]["pushed"] = True

        with open(self.history_file_path, 'w') as history_file:
            yaml.safe_dump(resulting_yaml, history_file)

    def write_out(self) -> str | None:
        if len(self.this_history) == 0:
            return None
        history = self.history
        resulting_yaml = {
            "type": "quipt-version-control",
            "history": history,
            "script": str(self.script_id)
        }

        new_version = self.most_recent_version + 1
        new_filename = f"./{self.play_name}-v{new_version:03d}.pv"
        history.append({
            "filename": new_filename,
            "version": new_version,
            "pushed": False,
            "changes": self.this_history
        }) 

        with open(self.history_file_path, 'w') as history_file:
            yaml.safe_dump(resulting_yaml, history_file)

        return os.path.join(self.database_path, new_filename)

    def remove(self):
        _ = self.history
        rprint(f"Removing version database for [italic green]{self.script_id}[/]")
        shutil.rmtree(self.database_path)

    def restore_to_version(self, version: int) -> Serializer|None:
        try:
            history_version = self.history[version]
            if history_version["version"] != version:
                raise RuntimeError
        except (IndexError, RuntimeError):
            rprint(f"Specified version {version} is invalid")
            return

        version_file = history_version["filename"]

        version_path = os.path.join(self.database_path, version_file)
        deser = Deserializer()
        file = deser.load(version_path)

        if self.serialized_file is None:
            rprint(f"Script [italic green]{self.script_id}[/] needs a version history")
            return

        detect_changes(self, file, self.serialized_file)
        
        rprint(f"Restoring version {version} for Script [italic green]{self.script_id}[/]")
        file_path = os.path.join(os.getcwd(), f'{self.play_name}-v{version}.txt')
        with open(file_path, "w") as outfile:
            dump_file(file, outfile)
        print("Script restored")

        with open(file_path) as infile:
            serializer = parse_text(infile.read() + '\n\n\n')
        return serializer


def dump_file(file: File, io: TextIO):
    print(file=io)
    print(f"#self {file.actors[-1]}", file=io)
    print(f"#others {', '.join(file.actors[:-1])}", file=io)
    print(file=io)
    for item in file.overview_talbe:
        if item.item_type == ItemType.DIVISION:
            print(f"#division {item.item}", file=io)
            print(file=io)
        else:
            dump_trigger(file, item.item, io)
            print(file=io)

def dump_trigger(file: File, trigger: Trigger, io: TextIO):
    if trigger.request_type != ItemType.DIVISION:
        dump_quote(file, trigger.request, io)
        print(file=io)
    dump_quote(file, trigger.response, io)

def dump_quote(file: File, quote: TQuote, io: TextIO):
    if quote.actor_id is all_actors:
        print("[.all]", file=io)
    else:
        quote_actor_string = ' & '.join(file.actors[id - 1] for id in quote.actor_id)
        print(f"[{quote_actor_string}]", file=io)
    dump_semantic_text(quote.content, io)

def dump_semantic_text(text: SemanticString, io: TextIO):
    buffer: list[str] = []
    for division in text.divisions:
        if division[0]:
            sdiv = f"({division[1]})"
        else:
            sdiv = division[1]
        buffer.append(sdiv)
    serialized_text = ''.join(buffer)
    dump_text(serialized_text, io)

AUTO_LINIEBREAK = 80
def dump_text(text: str, io: TextIO):
    new_lines = []
    for line in text.splitlines():
        while True:
            if len(line) <= AUTO_LINIEBREAK:
                new_lines.append(line)
                break
            if (idx := line.rfind(' ', 0, AUTO_LINIEBREAK)) == -1:
                new_lines.append(line)
                break
            ln1, line = line[:idx], line[idx:].lstrip()
            new_lines.append(ln1)
    print(*new_lines, sep='\n', file=io)

def simplify(segments):
    current_content = ""
    last_v = None
    for v, c in segments:
        if v != last_v and current_content:
            yield last_v, current_content
            current_content = c  # flush
        else:
            current_content += c
        last_v = v
    yield last_v, current_content

def _check_self_others_integrity(self_actor, other_actors, current_def):
    if self_actor is None or other_actors is None:
        return
    if self_actor in other_actors:
        raise ParserError(
                f"The actor name {self_actor!r} is defined for 'self' and 'others'; This is invalid",
                current_def.lineno)

def parse_actor(definition: Quote) -> set[str]:
    if '&' in definition.actor:
        actors = [actor.strip() for actor in definition.actor.split('&')]
        if len(actors) == 0:
            raise ParserError("Quote's actor tag contains no actors", definition.lineno)
        if len(min(actors, key=len)) < 1:
            raise ParserError("Quote's actor tag contains a syntax error", definition.lineno)
        actors_set = set(actors)
        if len(actors_set) != len(actors):
            raise ParserError("Quote's actor tag has one or more duplicates", definition.lineno)
        return actors_set
    elif definition.actor.startswith('.'):
        actor_class = definition.actor[1:]
        if actor_class != 'all':
            raise ParserError(f"Quote's actor tag: Unknwon actor class {actor_class!r}", definition.lineno)
        return all_actors
    return {definition.actor}

def handle_quote(definition: Quote, valid_actors: set[str]) -> set[str]:
    actors = parse_actor(definition)
    if actors is not all_actors and not actors.issubset(valid_actors):
        raise ParserError(f"Quote's actor tag contains unkown actor", definition.lineno)
    return actors

def trigger_get_actor_string(trigger: Trigger, actors: list[str]) -> tuple[str, str]:
    match trigger.request_type:
        case ItemType.DIVISION:
            request_actor = '.meta'
        case ItemType.QUOTE:
            if trigger.request.actor_id is all_actors:
                request_actor = '.all'
            else:
                request_actor = ' & '.join(sorted(actors[id - 1] for id in trigger.request.actor_id))
        case _:
            raise ValueError("Encountered Invalid Data")

    if trigger.response.actor_id is all_actors:
        response_actor = '.all'
    else:
        response_actor = ' & '.join(sorted(actors[id - 1] for id in trigger.response.actor_id))
    
    return request_actor, response_actor

def trigger_get_content_string(trigger: Trigger, divisions) -> tuple[str, str]:
    match trigger.request_type:
        case ItemType.DIVISION:
            request_content = divisions[trigger.request]
        case ItemType.QUOTE:
            request_content = ''.join(d[1] for d in trigger.request.content.divisions)
        case _:
            raise ValueError("Encountered Invalid Data") 
    response_content = ''.join(d[1] for d in trigger.response.content.divisions)

    return request_content, response_content

def file_to_sequence(file) -> Generator[str, None, None]:
    divisions: list[str] = []
    for item in file.overview_talbe:
        if item.item_type == ItemType.DIVISION:
            yield f"{('#' * 20)} {item.item} {('#' * 20)}"
            divisions.append(item.item)
            continue

        trigger = item.item

        request, response = trigger_get_actor_string(trigger, file.actors)
        request_content, response_content = trigger_get_content_string(trigger, divisions)

        request_hash = mmh3.hash(request_content, signed=False)
        response_hash = mmh3.hash(response_content, signed=False)
        yield f"{request}({request_hash})->{response}({response_hash})"

def detect_changes(database: Database, new_file: File, old_file: File):
    try:
        new_collected = list(file_to_sequence(new_file))
    except ValueError:
        assert False, "serializer invalid"

    prev_collected = list(file_to_sequence(old_file))
    
    cruncher = difflib.SequenceMatcher(None, prev_collected, new_collected)
    for tag, i1, i2, j1, j2 in cruncher.get_opcodes():
        if tag == 'replace':
            if len(range(i1, i2)) == len(range(j1, j2)):
                break_outer_loop = False
                for old_line, new_line in zip(prev_collected[i1:i2], new_collected[j1:j2]):
                    new_item = new_file.overview_talbe[new_collected.index(new_line)]
                    old_item = old_file.overview_talbe[prev_collected.index(old_line)]
                    if new_item.item_type != old_item.item_type:
                        break
                    if database.replace_item_compare(old_item, new_item):
                        if old_item.item_type != ItemType.DIVISION:
                            new_item.item.uuid = old_item.item.uuid
                        break_outer_loop = True
                if break_outer_loop:
                    continue
            for old_line in prev_collected[i1:i2]:
                old_item = old_file.overview_talbe[prev_collected.index(old_line)]
                database.delete(old_item)
            for new_line in new_collected[j1:j2]:
                new_item = new_file.overview_talbe[new_collected.index(new_line)]
                database.insert(new_item, get_prev_item_as_str(new_file, new_item))
        elif tag == 'delete':
            for idx, old_line in enumerate(prev_collected[i1:i2]):
                old_item = old_file.overview_talbe[prev_collected.index(old_line)]
                database.delete(old_item)
        elif tag == 'insert':
            for new_line in new_collected[j1:j2]:
                new_item = new_file.overview_talbe[new_collected.index(new_line)]
                database.insert(new_item, get_prev_item_as_str(new_file, new_item))
        elif tag == 'equal':
            for old_line, new_line in zip(prev_collected[i1:i2], new_collected[j1:j2]):
                new_item = new_file.overview_talbe[new_collected.index(new_line)]
                old_item = old_file.overview_talbe[prev_collected.index(old_line)]
                if new_item.item_type != old_item.item_type:
                    raise ValueError("WTF? By brain is not braining")
                if new_item.item_type == ItemType.DIVISION:
                    continue
                new_item.item.uuid = old_item.item.uuid
        else:
            raise ValueError('unknown tag %r' % (tag,))

def get_prev_item_as_str(file: File, item: OverviewTableItem) -> str:
    index = file.overview_talbe.index(item)
    if index == 0:
        return 'Top'
    item = file.overview_talbe[index - 1]
    if item.item_type == ItemType.DIVISION:
        return item.item.replace(' ', '\x1b')
    return str(UUID(bytes=item.item.uuid))

def parse_text(in_file_content: str) -> Serializer:
    parser = Parse(tokenize(in_file_content))

    self_actor: str | None = None
    other_actors: set[str] | None = None

    defs_gen = parser.parse()
    definition = None
    for definition in defs_gen:
        match definition:
            case Quote() | DivisionNotation():
                break
            case SelfDeclaration(lineno, name=self_name):
                if self_actor is not None:
                    raise ParserError("Can't declare 'self' twice (directive can only be used once)", lineno)
                self_actor = self_name
                _check_self_others_integrity(self_actor, other_actors, definition)
            case OthersDefinition(lineno, others=others_list):
                if other_actors is not None:
                    raise ParserError("Can't define 'others' twice (directive can only be used once)", lineno)
                other_actors = set(others_list)
                if len(other_actors) != len(others_list):
                    raise ParserError("'others' definition contains one or multiple duplicates", lineno)
                _check_self_others_integrity(self_actor, other_actors, definition)
    else:
        if definition is None:
            raise ParserError("'self' directive is missing", 1)
        assert False, "unreachable"

    if self_actor is None:
        raise ParserError("'self' directive is missing", definition.lineno)
    if other_actors is None:
        raise ParserError("'others' directive is missing", definition.lineno)

    all_actors = {*other_actors, self_actor}

    state = Serializer(other_actors, self_actor)
    lookahead_defintion: Quote | DivisionNotation | None = None
    while True:
        kwargs = {}
        match definition:
            case Quote(content=quote_content):
                actors = handle_quote(definition, all_actors)
                kwargs.update(type=ItemType.TRIGGER, content=quote_content, actors=actors)
            case DivisionNotation(name=division_name):
                try:
                    lookahead_defintion = next(defs_gen)
                except StopIteration:
                    pass

                division_is_request = False
                if isinstance(lookahead_defintion, Quote):
                    speculative_actors = handle_quote(lookahead_defintion, all_actors)
                    if self_actor in speculative_actors:
                        # the next definition (Quote) is a response,
                        # so treat this division as request
                        kwargs.update(type=ItemType.DIVISION, name=division_name)
                        division_is_request = True

                if not division_is_request:
                    state.new_division(division_name)
                    definition = lookahead_defintion
                    lookahead_defintion = None
                    continue

        if lookahead_defintion is not None:
            definition = lookahead_defintion
            lookahead_defintion = None
        else:
            try:
                definition = next(defs_gen)
            except StopIteration:
                raise ParserError(
                    "Unexpected EOF expected a response quote", definition.lineno
                )
        if isinstance(definition, DivisionNotation):
            raise ParserError(
                "'division' directive is invalid as a response", definition.lineno
            )
        
        actors = handle_quote(definition, all_actors)
        if actors is not all_actors_obj_alias and self_actor not in actors:
            raise ParserError(
                f"Self actor {self_actor!r} is not contained in respone's actor tag", definition.lineno
            )
        kwargs.update(response=state.quote_from_syntax(definition.content, actors))
        state.new_trigger(**kwargs)

        try:
            definition = next(defs_gen)
        except StopIteration:
            break
    serialized_file = state.file

    num_triggers = len([i for i in serialized_file.overview_talbe if i.item_type == ItemType.TRIGGER])
    if num_triggers == 0:
        lineno = getattr(definition, "lineno", 0)
        raise ParserError("Source contains no triggers", lineno)

    return state

all_actors_obj_alias = all_actors
def convert_with_error(in_file_path: str, database_location: str):
    with open(in_file_path, 'r') as in_file:
        in_file_content = in_file.read() + '\n\n\n'
    
    state = parse_text(in_file_content)
    serialized_file = state.file

    play_name = os.path.basename(in_file_path).rsplit('.', maxsplit=1)[0]
    if (database := Database.open(database_location, play_name)) is not None:
        if database.serialized_file is None:
            database.history
            rprint(f"Script [italic green]{database.script_id}[/] needs a version history")
            return
        detect_changes(database, serialized_file, database.serialized_file)
        if (out_file_path := database.write_out()) is not None:
            state.save(out_file_path)
            rprint(f"Staged changes [italic green]{database.script_id}[/] for [yellow]{play_name}[/]")
        else:
            print("Exit with no changes")
    else:
        uuid, out_file_path = Database.create_new(database_location, play_name, serialized_file)
        state.save(out_file_path)
        rprint(f"Created Script [italic green]{uuid}[/] for [yellow]{play_name}[/]")

def handle_parser_error(error: ParserError, in_file_path: str):
    with open(in_file_path, 'r') as in_file:
        lines = in_file.read().splitlines()
    line = lines[error.lineno - 1]
    print(f"File {in_file_path!r}, line {error.lineno}", file=sys.stderr)
    print(f"    {line}", file=sys.stderr)
    print(f"    {'^' * len(line)}", file=sys.stderr)
    print(f"Parser Error: {error.message}", file=sys.stderr)

def convert_handle_error(in_file_path: str, database_location: str): 
    in_file_path = os.path.abspath(in_file_path)
    database_location = os.path.abspath(database_location)

    try:
        convert_with_error(in_file_path, database_location)
    except ParserError as parser_error:
        handle_parser_error(parser_error, in_file_path)


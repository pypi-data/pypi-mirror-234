from __future__ import annotations
from enum import IntEnum
import os
from uuid import UUID, uuid4
import pyqrcode
import dbm
import platform

from typing import Any, Callable, cast
from rich import print as rprint
from base64 import b64encode
from websockets.sync.client import connect, ClientConnection

from .serialisation import File, ItemType, OverviewTableItem, Quote, Trigger, all_actors

errorno = 0
# WS_URI = "wss://quipt.app/ws-connect"
WS_URI = "ws://localhost:5000/ws-connect"
COOKIE_FILE = "quiptcontext.w"

class ErrorReason(IntEnum):
    UserCanceledOperation = 0
    Other = 2

class OperationalError(Exception):
    def __init__(self, reason: ErrorReason):
        super().__init__()
        self.reason = reason

class MessageTypes:
    LoginRequest = b'LR'
    Authentication = b'AT'
    ScriptCreation = b'CS'
    TriggerDeletion = b'DT'
    DivisionDeletion = b'DD'
    TriggerInsertion = b'IT'
    DivisionInsertion = b'ID'
    TriggerChange = b'CT'
    DivisionChange = b'CD'
    AlternateScript = b'AS'
    LeaveAlternate = b'AL'
    
class ScriptContext:
    def __init__(self, websocket: ClientConnection, script_id: UUID):
        self.websocket = websocket
        self.script_id = script_id
    
    def __enter__(self) -> Any:
        buffer = bytearray()
        buffer.extend(MessageTypes.AlternateScript)
        buffer.extend(self.script_id.bytes)
        self.websocket.send(buffer)

        if (response := self.check_error()) is None:
            return None

        assert response == self.script_id.bytes, "Invalid Client Data"

        return self

    def __exit__(self, *_):
        self.websocket.send(MessageTypes.LeaveAlternate)
        self.check_error()

    def delete_trigger(self, trigger_id: UUID):
        self.websocket.send(MessageTypes.TriggerDeletion + trigger_id.bytes)
        self.check_error()

    def delete_division(self, name: str):
        self.websocket.send(MessageTypes.DivisionDeletion + name.encode())
        self.check_error()

    def insert_trigger(self, prev: str, new_trigger: Trigger):
        buffer = bytearray()
        buffer.extend(MessageTypes.TriggerInsertion)  
        encode_previous(buffer, prev) 
        serialize_trigger(buffer, new_trigger)
        self.websocket.send(buffer)
        self.check_error()

    def insert_division(self, prev: str, name: str):
        buffer = bytearray()
        buffer.extend(MessageTypes.DivisionInsertion)
        encode_previous(buffer, prev) 
        buffer.extend(name.encode())
        self.websocket.send(buffer)
        self.check_error()

    def change_trigger(self, new_trigger: Trigger):
        buffer = bytearray()
        buffer.extend(MessageTypes.TriggerChange)
        serialize_trigger(buffer, new_trigger)
        self.websocket.send(buffer)
        self.check_error()

    def change_division(self, old_name: str, new_name: str):
        buffer = bytearray()
        buffer.extend(MessageTypes.DivisionChange)
        buffer.extend(old_name.encode() + b'\x00')
        buffer.extend(new_name.encode())
        self.websocket.send(buffer)
        self.check_error()

    def check_error(self) -> bytes:
        if (result := handle_error(self.websocket)) is not None:
            return result
        raise OperationalError(ErrorReason.Other)

class QuiptContext:
    def __init__(self, db: dbm._Database):
        self.db = db

    @classmethod
    def open(cls, data_path: str, filename: str) -> QuiptContext:
        context_path = os.path.join(data_path, filename)
        if os.path.exists(context_path):
            try:
                return cls(dbm.open(context_path, flag='w'))
            except Exception:
                pass
        os.makedirs(data_path, exist_ok=True)
        db = dbm.open(context_path, flag='c')
        db[b'client_info'] = f'{platform.system()} {platform.node()}'
        db[b'client_uuid'] = uuid4().bytes
        return cls(db)

    @property
    def cookie(self) -> bytes|None:
        return self.db.get(b'cookie', None)
    
    @cookie.setter
    def cookie(self, value: bytes|None):
        if value is None:
            del self.db[b'cookie']
        else:
            self.db[b'cookie'] = value

    @property
    def client_info(self) -> str:
        return self.db[b'client_info'].decode()

    @property
    def client_uuid(self) -> UUID:
        return UUID(bytes=self.db[b'client_uuid'])
    
    def __enter__(self) -> QuiptContext:
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        self.db.close()

class QuiptApp:
    def __init__(
            self, 
            websocket: ClientConnection, 
            uuid: UUID,
            data_path: str
        ):
        self.data_path = data_path

        self.websocket = websocket
        self.uuid = uuid

    @classmethod
    def login(cls, data_path: str) -> Any:
        with QuiptContext.open(data_path, COOKIE_FILE) as context:
            connection = connect(WS_URI)

            logged_in = False
            if context.cookie is not None:
                logged_in, user_uuid = authenticate(connection, context)
                if not logged_in:
                    context.cookie = None

            if not logged_in:
                user_uuid = login(connection, context)

            return cls(connection, user_uuid, data_path)

    def create_script(self, script_file: File, script_id: UUID, script_name: str):
        buffer = bytearray(MessageTypes.ScriptCreation)
        buffer.extend(script_id.bytes)
        buffer.extend(script_name.encode())
        buffer.extend(b'\x00')

        buffer.extend(
            b'\f'.join(actor.encode() for actor in script_file.actors)
        )
        buffer.extend(b'\v')

        for item in script_file.overview_talbe:
            serialize_item(buffer, item)
        self.websocket.send(buffer)
        if handle_error(self.websocket) is None:
            raise OperationalError(ErrorReason.Other)

    def alternate_script(self, script_id: UUID) -> ScriptContext:
        return ScriptContext(self.websocket, script_id)

    def close(self):
        self.websocket.close()

def encode_previous(buffer: bytearray, prev: str): 
    if prev == 'Top':
        buffer.extend(b'T')
    elif (uuid := str_to_uuid(prev)) is not None:
        buffer.extend(b'U' + uuid.bytes)
    else:
        buffer.extend(b'D' + prev.replace('\x1b', ' ').encode() + b'\x00')

def str_to_uuid(test: str) -> UUID | None:
    try:
        return UUID(test)
    except ValueError:
        return

def serialize_item(buffer: bytearray, item: OverviewTableItem):
    if item.item_type == ItemType.DIVISION:
        buffer.append(0x05)
        buffer.extend(item.item.encode())
        buffer.append(0x00)
    elif item.item_type == ItemType.TRIGGER:
        buffer.append(0x04)
        serialize_trigger(buffer, item.item)

def serialize_trigger(buffer: bytearray, trigger: Trigger):
    buffer.extend(trigger.uuid)
    if trigger.request_type == ItemType.DIVISION:
        buffer.append(0x1A)
    else:
        if trigger.request.actor_id is all_actors:
            buffer.append(0x19)
        else:
            actor_string = bytes(id - 1 for id in trigger.request.actor_id)
            buffer.extend(actor_string)
    buffer.extend(b'\t')
    if trigger.response.actor_id is all_actors:
        buffer.append(0x19)
    else:
        actor_string = bytes(id - 1 for id in trigger.response.actor_id)
        buffer.extend(actor_string)
    buffer.extend(b'\v')
    serialize_text(buffer, trigger.request_type, trigger.request, trigger.response)

def serialize_text(buffer: bytearray, request_type: ItemType, request: int | Quote, response: Quote):
    if request_type == ItemType.DIVISION:
        buffer.append(request)
    else:
        request = cast(Quote, request)
        if request.content.divisions[0][0]:
            buffer.extend(b'\x10')
        request_content_str = b'\x10'.join(div[1].encode() for div in request.content.divisions)
        buffer.extend(request_content_str)
    buffer.extend(b'\t')
    if response.content.divisions[0][0]:
        buffer.extend(b'\x10') # )
    response_content_str = b'\x10'.join(div[1].encode() for div in response.content.divisions)
    buffer.extend(response_content_str)

def authenticate(websocket: ClientConnection, context: QuiptContext) -> tuple[bool, UUID|None]: 
    websocket.send(MessageTypes.Authentication + context.cookie)
    expected = {11,}
    if (response := handle_error(websocket, expected=expected)) is None:
        if errorno not in expected:
            websocket.close()
            raise OperationalError(ErrorReason.Other)
        return False, None
    uuid, cookie = deserialize_login_cookie(response)
    context.cookie = cookie
    return True, uuid

def login(connection: ClientConnection, context: QuiptContext) -> UUID:
    data = context.client_uuid.bytes + context.client_info.encode()
    connection.send(MessageTypes.LoginRequest + data)
    if (connection_token := handle_error(connection)) is None:
        raise OperationalError(ErrorReason.Other)
    connection_token = b64encode(connection_token).decode()

    print_qr_for_token(connection_token)
    rprint("Scan with your Smartphone or press ^C to cancel")

    try:
        if (response := handle_error(connection)) is None:
            raise OperationalError(ErrorReason.Other)
        uuid, cookie = deserialize_login_cookie(response)
    except KeyboardInterrupt:
        connection.close()
        raise OperationalError(ErrorReason.UserCanceledOperation)
    context.cookie = cookie
    return uuid

def deserialize_login_cookie(response: bytes) -> tuple[UUID, bytes]:
    uuid, cookie = response[:16], response[16:]
    uuid = UUID(bytes=uuid)
    rprint(f"Connected with user [italic green]{uuid}[/]")

    return uuid, cookie

def handle_error(websocket: ClientConnection, *, expected: set[int]|None = None) -> bytes | None:
    global errorno
    response = websocket.recv()
    if response[0] == 0x00:  # success
        return response[1:]

    errorno = response[0]
    message = response[1:].decode()
    if errorno not in (expected or set()):
        rprint(f"Request failed with {errorno}: [italic red]{message}[/]")

    return None

def print_qr_for_token(token: str):
    code = pyqrcode.create(token)
    print(code.terminal(quiet_zone=0, background='default', module_color='white'))

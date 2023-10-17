import socket
from .message import Message
from .message_event import MessageEvent
from .message_list import MessageList
from .connection import Connection
from .router import Router
from json_cpp import JsonList


class MessageClient:
    def __init__(self):
        self.failed_messages = None
        self.running = False
        self.registered = False
        self.router = Router()
        self.router.unrouted_message = self.__unrouted__
        self.ip = ""
        self.port = 0
        self.messages = MessageList()
        self.connection = None
        self._request_time_out = 500

    def __unrouted__(self, message: Message):
        self.messages.queue(message)

    def connect(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((self.ip, self.port))
        except socket.error as msg:
            return False
        self.connection = Connection(s, self.failed_messages)
        self.router.attend(self.connection)
        return True

    def send_request(self, message: Message, time_out: int = -1) -> Message:
        event = MessageEvent()
        self.router.add_message_event(request_id=message.id, event=event)
        if time_out < 0:
            time_out = self._request_time_out
        self.send_message(message)
        response = event.wait(time_out)
        if response:
            return response
        raise TimeoutError("the request has timed_out")

    def set_request_time_out(self, time_out: int):
        self._request_time_out = time_out

    def send_async_request(self, message: Message, call_back):
        event = MessageEvent(call_back=call_back)
        self.router.add_message_event(request_id=message.id, event=event)
        self.send_message(message)

    def get_manifest(self):
        return self.send_request(Message("!manifest")).get_body(JsonList)

    def subscribe(self):
        return self.send_request(Message("!subscribe")).body == "success"

    def unsubscribe(self):
        return self.send_request(Message("!unsubscribe")).body == "success"

    def send_message(self, message: Message):
        self.connection.send(message)

    def disconnect(self):
        self.running = False

    def __del__(self):
        self.disconnect()

    def __bool__(self):
        return self.connection is True

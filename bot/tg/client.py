import marshmallow_dataclass
import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token: str):
        self.token = token

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        request = requests.get(
            self.get_url('getUpdates'),
            params={'offset': offset, 'timeout': timeout}
        ).json()
        RequestSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)
        return RequestSchema().load(request)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        request = requests.get(
            self.get_url('sendMessage'),
            params={'chat_id': chat_id, 'text': text}
        ).json()
        RequestSchema = marshmallow_dataclass.class_schema(SendMessageResponse)
        return RequestSchema().load(request)

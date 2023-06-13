from typing import Optional

import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist.settings import TG_TOKEN


class TgClient:
    def    __init__(self, token: Optional[str] = None) -> None:
        self.token = token if token else TG_TOKEN

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url("getUpdates")
        response = requests.get(url, params={"offset": offset, "timeout": timeout})
        return GetUpdatesResponse.Schema().load(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        response = requests.post(url, params={"chat_id": chat_id, "text": text})
        return SendMessageResponse.Schema().load(response.json())

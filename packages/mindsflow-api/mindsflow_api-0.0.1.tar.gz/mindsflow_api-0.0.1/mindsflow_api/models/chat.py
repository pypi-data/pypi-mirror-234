import requests
from typing import Optional
from ..utils.http_request import post_request


class Chat:
    headers: Optional[dict] = {}
    base_url: Optional[str] = "https://api.mindsflow.ai"
    path_messages: Optional[str] = "/chat/messages"

    def messages(self, data) -> str:
        if data.get('stream'):
            raise Exception("Don't support stream'")
        resp = requests.post(
            url=self.base_url + self.path_messages,
            headers=self.headers,
            json=data
        )
        if 200 <= resp.status_code < 300:
            resp = resp.json()
            content = resp.get("choices")[0].get("message", {}).get("content", "")
            if content == "":
                content = resp.get("choices")[0].get("delta", {}).get("content", "")
            return content
        else:
            return resp.text

    async def amessages(self, data: dict) -> str:
        if data.get('stream'):
            raise Exception("Don't support stream'")
        url = f"{self.base_url}{self.path_messages}"
        resp = await post_request(url, headers=self.headers, data=data)
        chat_msg: dict = await resp.json()
        content = chat_msg.get("choices")[0].get("message", {}).get("content", "")
        if content == "":
            content = chat_msg.get("choices")[0].get("delta", {}).get("content", "")
        return content

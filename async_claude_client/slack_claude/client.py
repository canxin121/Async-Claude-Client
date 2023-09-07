import asyncio

from slack_sdk.web.async_client import AsyncWebClient

from .types import Text, ChatUpdate
from ..util import retry


class Slack_Claude_Client:
    slack_user_token: str
    claude_id: str
    channel_id: str
    slack_client: AsyncWebClient
    pre_msg: str

    def __init__(
        self,
        slack_user_token: str,
        claude_id: str,
        channel_id: str,
        pre_msg: str = "<忽略'@Claude',不说没看到也不说看到>",
    ):
        self.slack_user_token = slack_user_token
        self.claude_id = claude_id
        self.channel_id = channel_id
        self.slack_client = AsyncWebClient(token=self.slack_user_token)
        self.pre_msg = pre_msg

    def create_new_chat(self):
        return {"thread_ts": "", "msg_ts": ""}

    @retry(3, "Failed to send message to slack")
    async def send_message(self, question: str, chat: dict):
        result = await self.slack_client.chat_postMessage(
            channel=self.channel_id,
            text=f"<@{self.claude_id}>{question}",
            thread_ts=chat["thread_ts"],
        )
        if result["ok"]:
            chat["msg_ts"] = result["ts"]
            if not chat["thread_ts"]:
                chat["thread_ts"] = result["ts"]
            return chat
        else:
            raise Exception(f"Error: {result}")

    async def get_stream_message(self, chat: dict):
        retry = 3
        detail_error = "Unknown error"
        while True:
            if retry <= 0:
                raise Exception(detail_error)
            try:
                text = await self.get_reply(chat)
                yield text
                if text.finished:
                    break
            except Exception as e:
                detail_error = str(e)
                retry -= 1

    @retry(3, "Failed to get reply from slack claude: ")
    async def get_reply(self, chat: dict) -> Text:
        result = await self.slack_client.conversations_replies(
            ts=chat["thread_ts"],
            channel=self.channel_id,
            oldest=chat["msg_ts"],
        )
        for message in result.data["messages"][::-1]:
            text = message.get("text", "")
            user = message.get("user", "")
            msg_ts = float(message.get("ts", 0))
            if (
                text.rstrip("_Typing…_")
                and (not text.startswith("\n&gt; _*Please note:*"))
                and (msg_ts > float(chat["msg_ts"]))
                and user == self.claude_id
            ):
                return Text(
                    content=text.rstrip("\n\n_Typing…_"),
                    finished=bool(not text.endswith("_Typing…_")),
                )
        await asyncio.sleep(2)
        raise Exception("Claude didn't response")

    async def ask_stream_raw(self, question: str, chat: dict):
        # new_ts可以理解为新发送的消息的id,而self.botdata.thread_ts则是一个消息列的id
        new_chat = await self.send_message(question, chat)
        yield ChatUpdate(content=new_chat)
        last_text = ""
        async for data in self.get_stream_message(new_chat):
            text = data.content
            finished = data.finished
            yield Text(content=text[len(last_text) :], finished=finished)
            last_text = text

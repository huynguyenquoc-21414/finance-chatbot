from uuid import uuid4
import chainlit as cl

from llm.finance import FinanceAssistant


@cl.on_chat_start
async def start():
    """
    Khởi tạo chat session mới
    """
    cl.user_session.set("assistant", FinanceAssistant())
    cl.user_session.set("user_id", str(uuid4()))


@cl.on_message
async def main(message: cl.Message):
    """
    Xử lý mỗi tin nhắn từ người dùng
    """
    assistant = cl.user_session.get("assistant")
    user_id = cl.user_session.get("user_id")

    msg = cl.Message(content="")
    async for response_chunk in assistant.submit_message(
        user_id=user_id,
        user_message=message.content,
    ):
        await msg.stream_token(response_chunk)

    await msg.send()

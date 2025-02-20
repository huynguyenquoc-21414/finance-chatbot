import asyncio
from multiprocessing import cpu_count
import os
from typing import AsyncIterable, Dict
from uuid import uuid4
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages.base import BaseMessage
from langchain_core.messages.tool import ToolMessage

from constants.environments import DEEPINFRA_API_KEY, DEEPINFRA_MODEL_VARIANT, DEEPINFRA_URL
from llm.tools.functions.company import (
    GetCompanyDividends,
    GetCompanyEvents,
    GetCompanyInsiderDeals,
    GetCompanyNews,
    GetCompanyOfficers,
    GetCompanyOverview,
    GetCompanyProfile,
    GetCompanyShareholders,
    GetCompanySubsidiaries,
)
from llm.tools.functions.income_statement import GetBalanceSheet, GetCashFlow, GetIncomeStatement, GetRatio
from llm.tools.functions.quote import GetQuoteHistory
from llm.tools.schemas import CustomBaseTool


class FinanceAssistant:
    def __init__(
        self,
        limit_history=10,
    ):
        """Initialize the Finance Assistant"""
        self.tools: list = [
            GetCompanyProfile(),
            GetCompanyOverview(),
            GetCompanyShareholders(),
            GetCompanyOfficers(),
            GetCompanySubsidiaries(),
            GetCompanyNews(),
            GetCompanyDividends(),
            GetCompanyInsiderDeals(),
            GetCompanyEvents(),
            GetIncomeStatement(),
            GetBalanceSheet(),
            GetCashFlow(),
            GetRatio(),
            GetQuoteHistory(),
        ]
        self.tool_choice = {f"{tool.name}": tool for tool in self.tools}
        self.sem = asyncio.Semaphore(min(len(self.tools), cpu_count()))

        self.llm = ChatOpenAI(
            name="Finance Assistant",
            model=DEEPINFRA_MODEL_VARIANT,
            base_url=DEEPINFRA_URL,
            api_key=DEEPINFRA_API_KEY,
            temperature=0.1,
            top_p=0.1,
            streaming=True,
            cache=False,
            seed=0,
        )

        self.prompt: str = self._load_prompt()
        self.conversation_history: Dict[str, list] = {}
        self.limit_history: int = limit_history

    @staticmethod
    def _load_prompt() -> str:
        """Load and cache the prompt file"""
        prompt_path: str = os.path.join(os.getcwd(), "src/llm/prompt.md")
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    def _get_or_create_history(self, user_id: str) -> list:
        """Get existing conversation history or create new one"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = [SystemMessage(content=self.prompt)]
        return self.conversation_history[user_id]

    async def execute_tool(self, tool_call):
        async with self.sem:
            id: str = tool_call.get("id")
            name: str = tool_call.get("name")
            arguments: dict = tool_call.get("args", {})

            tool_choice: CustomBaseTool = self.tool_choice[name]
            tool_result = await tool_choice.ainvoke(arguments)

            return ToolMessage(
                content=tool_result,
                tool_call_id=id,
            )

    async def submit_message(self, user_id: str, user_message: str) -> AsyncIterable[str]:
        messages: list = self._get_or_create_history(user_id)
        messages.append(HumanMessage(content=user_message))

        first = True
        async for chunk in self.llm.astream(messages):
            if chunk.content:
                yield chunk.content

            if first:
                gathered: BaseMessage = chunk
                first = False
            else:
                gathered = gathered + chunk

        messages.append(
            AIMessage(
                content=gathered.content,
                additional_kwargs=gathered.additional_kwargs,
            )
        )

        if gathered.tool_calls:
            tool_calls = gathered.tool_calls
            tool_tasks = [self.execute_tool(tool) for tool in tool_calls]

            tool_results = await asyncio.gather(*tool_tasks)
            messages.extend(tool_results)

            content: str = ""
            async for chunk in self.llm.astream(messages):
                if chunk:
                    yield chunk.content
                    content += chunk.content

            messages.append(AIMessage(content=content))

        if len(messages) > self.limit_history:
            messages[1:] = messages[1 - self.limit_history :]


async def main():
    # Initialize detector once
    social_listening_assistant = FinanceAssistant()

    # Prepare test data
    user_id = str(uuid4())
    test_messages = [""]

    # Batch process messages
    for message in test_messages:
        print(f"User: {message}")
        print("Chatbot: ", end="")

        async for chunk in social_listening_assistant.submit_message(user_id, message):
            print(chunk, end="", flush=True)

        print("\n")


if __name__ == "__main__":
    asyncio.run(main())

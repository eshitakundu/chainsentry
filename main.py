import asyncio

from dotenv import load_dotenv
from nooa import Agent
from nooa.unifiedllm.registry import get_llm_client


load_dotenv()


llm = get_llm_client(
    "openrouter/auto"
)


class TestAgent(Agent, llm=llm):
    """You are a concise assistant."""

    async def answer(self, question: str) -> str:
        """Answer the question in one sentence."""
        ...


async def main():
    agent = TestAgent()

    result = await agent.answer(
        "What is blockchain?"
    )

    print(result)


asyncio.run(main())
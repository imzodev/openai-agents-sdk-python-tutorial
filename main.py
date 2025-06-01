import os
from dotenv import load_dotenv
from agents import Agent, Runner
from openai import AsyncOpenAI
import asyncio
from agents import set_default_openai_client, set_default_openai_api, set_tracing_disabled


async def main():
    load_dotenv()
    BASE_URL = os.getenv("LLM_API_URL") or ""
    API_KEY = os.getenv("LLM_API_KEY") or ""
    MODEL_NAME = os.getenv("LLM_MODEL") or ""
    
    client = AsyncOpenAI(
        base_url=BASE_URL,
        api_key=API_KEY,
    )
    
    set_default_openai_client(client=client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(True)

    agent = Agent(
        name="Assistant",
        instructions="Eres un asistente que responde en español",
        model=MODEL_NAME,
    )

    result = await Runner.run(agent, "¿Quien eres? De que compañía eres?")
    print(result.final_output)

    
if __name__ == "__main__":
    asyncio.run(main())
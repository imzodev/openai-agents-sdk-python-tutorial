import os
from agents.mcp import MCPServerStdio
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
    
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["@playwright/mcp@latest", "--headless", "--viewport-size=1720,920"],
        }
    ) as server:
        tools = await server.list_tools()
        # print([tool.name for tool in tools])

        agent = Agent(
        name="Experto en SEO",
            instructions="Eres un experto navegando y extrayendo información para formatearla en un JSON estructurado.",
            model=MODEL_NAME,
            mcp_servers=[server],
        )

        result = await Runner.run(agent, "Ve a esta direccion https://www.bing.com y busca 'mecánico en medellin'. Despues da click en Mapas. Dame la informacion que veas")
        print(result.final_output)

    
if __name__ == "__main__":
    asyncio.run(main())
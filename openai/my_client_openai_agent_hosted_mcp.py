import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI, DefaultAioHttpClient
from openai.types.responses import ResponseTextDeltaEvent
from agents import (
    Agent,
    Runner,
    set_tracing_export_api_key,
    OpenAIResponsesModel,
    HostedMCPTool
)

_ = load_dotenv('.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MCP_URL = os.getenv("MCP_URL", "http://localhost:8080/mcp")
set_tracing_export_api_key(OPENAI_API_KEY)

async def main(input: str):
    client = AsyncOpenAI(
        api_key=OPENAI_API_KEY,
        http_client=DefaultAioHttpClient(),
    )
    
    try:
        agent = Agent(
            name="Agent",
            model=OpenAIResponsesModel(
                openai_client=client,
                model="gpt-4.1",
            ),
            instructions="You're a helpful agent",
            tools=[
                HostedMCPTool(
                    tool_config={
                        "type": "mcp",
                        "server_label": "my_mcp_server",
                        "server_description": "My MCP server to greet user",
                        "server_url": MCP_URL,
                        "require_approval": "never",
                    }
                )
            ],
        )

        result = Runner.run_streamed(
            agent,
            input,
        )

        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
    finally:
        await client.close()


if __name__ == "__main__":
    user_input = "Hi, this is Markchen1214, how are you?"
    asyncio.run(main(user_input))
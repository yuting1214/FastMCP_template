import asyncio
import os
from dotenv import load_dotenv
from fastmcp import Client

_ = load_dotenv('.env')
MCP_URL = os.getenv("MCP_URL")
client = Client(MCP_URL)

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

if __name__ == "__main__":
    asyncio.run(call_tool("Ford"))
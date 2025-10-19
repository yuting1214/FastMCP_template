import asyncio
from fastmcp import Client

RAILWAY_URL = "https://your-railway-url.up.railway.app/mcp"
client = Client(RAILWAY_URL)

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

if __name__ == "__main__":
    asyncio.run(call_tool("Ford"))
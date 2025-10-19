"""
Client for connecting to a FastMCP server running in Docker via HTTP.
Usage:
    export HOST_URL="http://localhost:8080"
    uv run docker-client.py
"""
import os
import asyncio
from fastmcp import Client

PORT = os.getenv("PORT", "8080")
HOST_URL = os.getenv("HOST_URL", "http://localhost")
client = Client(f"{HOST_URL}:{PORT}/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

if __name__ == "__main__":
    asyncio.run(call_tool("Ford"))

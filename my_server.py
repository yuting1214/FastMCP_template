import asyncio
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

async def main():
    await mcp.run_async()

if __name__ == "__main__":
    asyncio.run(main())

    

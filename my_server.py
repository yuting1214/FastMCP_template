import os
import uvicorn
from fastmcp import FastMCP
from fastapi import FastAPI

mcp = FastMCP(
    "My MCP Server",
    stateless_http=True
    )

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Create ASGI app from MCP server
mcp_app = mcp.http_app(path='/mcp')

# Key: Pass lifespan to FastAPI
app = FastAPI(title="My MCP Server", lifespan=mcp_app.lifespan)

# Mount the MCP server
app.mount("/", mcp_app)

if __name__ == "__main__":
    uvicorn.run(
        app="my_server:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 5000)),
        # reload=True,
        workers=2
    )

    

# FastMCP Template

This is a FastMCP template project that works seamlessly in local, Docker, and cloud environments. **Get started instantly by deploying to Railway with one click!**

## 🚀 Quick Deploy to Railway (Recommended)

The fastest way to get your FastMCP server running in the cloud:

### One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/YOUR_TEMPLATE_URL)

Or manually:
1. Go to [railway.app](https://railway.app)
2. Create a new project → "Deploy from GitHub repo"
3. Select this repository
4. Railway automatically detects the `Dockerfile` and deploys
5. Your server gets a public URL: `https://your-railway-url.up.railway.app/mcp`

### Connect Remote Client to Railway

Once deployed, use this client to connect from anywhere:

**Simple Method (Direct URL):**
```python
# my_client_remote.py
import asyncio
from fastmcp import Client

# Replace with your Railway URL
RAILWAY_URL = "https://your-railway-url.up.railway.app/mcp"
client = Client(RAILWAY_URL)

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)

if __name__ == "__main__":
    asyncio.run(call_tool("Ford"))
```

Run it:
```bash
uv run my_client_remote.py
```

**With Environment Variable (More Flexible):**
```bash
export RAILWAY_URL="https://your-railway-url.up.railway.app/mcp"
uv run my_client_remote.py
```

### Railway Benefits

✅ **One-Click Deploy** - No infrastructure setup needed  
✅ **Automatic HTTPS** - SSL/TLS certificates included  
✅ **Global Access** - Your API accessible worldwide  
✅ **Auto-Deploy** - Updates when you push to GitHub  
✅ **Built-in Monitoring** - Logs and performance metrics  
✅ **Custom Domain** - Add your own domain easily  

---

## Project Structure

- `my_server.py` - FastMCP server with a `greet` tool (works locally, Docker, and Railway)
- `my_client.py` - Local/Docker client that connects via HTTP
- `my_client_remote.py` - Remote client for Railway connections
- `Dockerfile` - Container configuration for all cloud deployments

## Local Development

Perfect for testing and development on your machine.

### Terminal 1 - Start the server:
```bash
uv run fastmcp run my_server.py:mcp --transport http --port 8080
```

### Terminal 2 - Run the client:
```bash
export PORT=8080
export HOST_URL="http://localhost"
uv run my_client.py
```

Output: `Hello, Ford!`

## Docker Deployment

Deploy locally with Docker or on any container platform.

**Build the Docker image:**
```bash
docker build -t fastmcp-server .
```

**Run the Docker container:**
```bash
docker run -p 8080:8080 fastmcp-server
```

**Connect the client:**
```bash
export PORT=8080
export HOST_URL="http://localhost"
uv run my_client.py
```

## Environment Variables

### Local & Docker Deployments

- `HOST_URL` - The server host URL (default: `http://localhost`)
- `PORT` - The server port (default: `8080`)

**Examples:**
```bash
# Custom port
export PORT=3000
uv run fastmcp run my_server.py:mcp --transport http --port 3000
export PORT=3000
uv run my_client.py

# Custom host
export HOST_URL="http://192.168.1.100"
export PORT=8080
uv run my_client.py
```

### Railway Deployment

- `RAILWAY_URL` - Full Railway endpoint URL (e.g., `https://your-url.up.railway.app/mcp`)
- Configure additional variables in Railway dashboard → Variables tab

## Architecture

### Why This Approach?

This template uses **HTTP transport** for consistency across all deployment scenarios:

1. **Consistency** - Same protocol everywhere
2. **Simplicity** - Just two files for any scenario
3. **Scalability** - HTTP enables cloud deployment
4. **Flexibility** - Easy to modify URLs/ports per environment

### Deployment Options

```
┌──────────────────────────────────────────────┐
│  🚀 RECOMMENDED: Railway Cloud                 │
│  • One-click deployment                        │
│  • Automatic HTTPS & CDN                       │
│  • Global access                               │
│  URL: https://your-url.up.railway.app/mcp     │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  🐳 Docker (Local or Any Cloud)               │
│  • Full control                                │
│  • Works anywhere with Docker                  │
│  URL: http://localhost:8080/mcp               │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│  🏠 Local Development                         │
│  • Perfect for testing                        │
│  • Two terminal setup                         │
│  URL: http://localhost:8080/mcp               │
└──────────────────────────────────────────────┘
```

## Configuration Details

### Server (my_server.py)

The server uses the FastMCP framework with a simple `greet` tool:

```python
@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

When run locally with:
```bash
uv run fastmcp run my_server.py:mcp --transport http --port 8080
```

When run in Docker via `Dockerfile`:
```dockerfile
CMD ["sh", "-c", "uv run fastmcp run my_server.py:mcp --transport http --host 0.0.0.0 --port $PORT"]
```

### Client (my_client.py)

Local/Docker client connects with environment variables:

```python
PORT = os.getenv("PORT", "8080")
HOST_URL = os.getenv("HOST_URL", "http://localhost")
client = Client(f"{HOST_URL}:{PORT}/mcp")
```

### Remote Client (my_client_remote.py)

Railway/remote client connects with direct URL or environment variable:

```python
RAILWAY_URL = os.getenv("RAILWAY_URL", "https://your-url.up.railway.app/mcp")
client = Client(RAILWAY_URL)
```

## Troubleshooting

### Railway Connection Issues

**Server not responding:**
1. Check Railway deployment logs in dashboard
2. Verify URL: `https://your-url.up.railway.app/mcp`
3. Test with curl: `curl https://your-railway-url.up.railway.app/mcp`

**Finding your Railway URL:**
1. Go to Railway project dashboard
2. Select the deployment
3. Go to "Settings"
4. Copy the domain URL
5. Append `/mcp` for the endpoint

**Custom Domain on Railway:**
- Go to Service Settings → Custom Domain
- Add your domain (e.g., `mcp.example.com`)

### Local Development Issues

**Connection failed:**
1. Check if server is running: `ps aux | grep fastmcp`
2. Verify port accessible: `curl http://localhost:8080/mcp`
3. Ensure PORT and HOST_URL environment variables are set

**Port already in use:**
```bash
# Use different port
export PORT=3000
uv run fastmcp run my_server.py:mcp --transport http --port 3000
export PORT=3000
uv run my_client.py
```

### Docker Issues

1. Check if container is running: `docker ps`
2. View logs: `docker logs <container-id>`
3. Verify port mapping: `docker run -p 8080:8080 ...`
4. Test connectivity: `curl http://localhost:8080/mcp`

## Summary

This FastMCP template provides multiple deployment options:

- ✅ **Railway** - Fastest cloud deployment (recommended)
- ✅ **Docker** - Full control, works anywhere
- ✅ **Local** - Perfect for development and testing
- ✅ **Same codebase** - No changes needed for different deployments
- ✅ **Just change URLs** - Environment variables handle all variations

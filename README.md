# FastMCP Template

This is a FastMCP template project that works seamlessly in both local and Docker environments using a unified HTTP transport approach.

## Project Structure

- `my_server.py` - FastMCP server with a `greet` tool (works locally and in Docker)
- `my_client.py` - Universal client that connects via HTTP (works with both local and Docker servers)
- `Dockerfile` - Docker configuration for running the server

## Quick Start

### Local Development

**Terminal 1 - Start the server:**
```bash
uv run fastmcp run my_server.py:mcp --transport http --port 8080
```

**Terminal 2 - Run the client:**
```bash
export PORT=8080
export HOST_URL="http://localhost"
uv run my_client.py
```

Output: `Hello, Ford!`

## Docker Deployment

**Build the Docker image:**
```bash
docker build -t fastmcp-server .
```

**Run the Docker container:**
```bash
docker run -p 8080:8080 fastmcp-server
```

This starts the server on `http://localhost:8080/mcp`

**From another terminal, run the client:**
```bash
export PORT=8080
export HOST_URL="http://localhost"
uv run my_client.py
```

## Environment Variables

Both local and Docker setups use the same environment variables:

- `HOST_URL` - The server host URL (default: `http://localhost`)
- `PORT` - The server port (default: `8080`)

### Local Examples

```bash
# Default (localhost:8080)
uv run my_client.py

# Custom port
export PORT=3000
uv run fastmcp run my_server.py:mcp --transport http --port 3000
# Then in another terminal:
export PORT=3000
uv run my_client.py

# Custom host
export HOST_URL="http://192.168.1.100"
export PORT=8080
uv run my_client.py
```

### Docker Examples

```bash
# Run on custom port
docker run -p 9000:9000 -e PORT=9000 fastmcp-server

# Then connect with:
export PORT=9000
export HOST_URL="http://localhost"
uv run my_client.py
```

## Architecture

### Why This Approach?

This unified design uses **HTTP transport for both local and Docker deployments**, providing:

1. **Consistency** - Same protocol and code paths whether local or containerized
2. **Simplicity** - Just two files for any deployment scenario
3. **Scalability** - HTTP makes it easy to scale across multiple machines
4. **Flexibility** - Easy to modify HOST_URL for different environments

### How It Works

```
┌─────────────────────────────────────────┐
│          Local Development              │
│                                         │
│  Terminal 1:                            │
│  uv run fastmcp run                     │
│    my_server.py:mcp                     │
│    --transport http --port 8080         │
│           │                             │
│           ↓ (HTTP)                      │
│  http://localhost:8080/mcp              │
│           ↑                             │
│  Terminal 2:                            │
│  uv run my_client.py                    │
│  (connects via HTTP)                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│         Docker Deployment               │
│                                         │
│  docker run -p 8080:8080                │
│  fastmcp-server                         │
│           │                             │
│           ↓ (HTTP on port 8080)         │
│  http://localhost:8080/mcp              │
│           ↑                             │
│  Host Machine:                          │
│  uv run my_client.py                    │
│  (connects via HTTP)                    │
└─────────────────────────────────────────┘
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

The client connects to the HTTP endpoint and calls tools:

```python
PORT = os.getenv("PORT", "8080")
HOST_URL = os.getenv("HOST_URL", "http://localhost")
client = Client(f"{HOST_URL}:{PORT}/mcp")
```

## Troubleshooting

### "Connection failed" error

**Local:**
1. Check if server is running: `ps aux | grep fastmcp`
2. Verify port is accessible: `curl http://localhost:8080/mcp`
3. Ensure PORT and HOST_URL environment variables are set correctly

**Docker:**
1. Check if container is running: `docker ps`
2. Check container logs: `docker logs <container-id>`
3. Verify port mapping: `docker run -p 8080:8080 ...`
4. Test connectivity from host: `curl http://localhost:8080/mcp`

### Port Already in Use

If port 8080 is already in use, use a different port:

```bash
# Local server on port 3000
uv run fastmcp run my_server.py:mcp --transport http --port 3000

# Client connects to port 3000
export PORT=3000
uv run my_client.py
```

### Docker Network Issues

If connecting from outside the Docker host (e.g., from a different machine):

```bash
# Use the actual IP of the Docker host
export HOST_URL="http://192.168.1.100"
export PORT=8080
uv run my_client.py
```

The `--host 0.0.0.0` in the Dockerfile ensures the server listens on all interfaces, making it accessible from any machine on the network.

## Summary

This FastMCP template demonstrates a clean, unified approach where:
- ✅ Same two files work locally and in Docker
- ✅ Same client code for all scenarios
- ✅ Simple environment variable configuration
- ✅ HTTP transport for consistency and scalability

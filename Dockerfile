# Use the official Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Install system dependencies including PostgreSQL client libraries
RUN apt-get update && \
    apt-get install -y \
        libpq-dev \
        && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Set environment variables
ENV UV_SYSTEM_PYTHON=1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PORT=8080

# Copy pyproject.toml and uv.lock* first to leverage Docker cache
COPY pyproject.toml uv.lock* ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy the application code
COPY . .

# Command to run the uvicorn server
CMD ["uv", "run", "my_server.py"]
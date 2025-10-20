import os
from dotenv import load_dotenv
from openai import OpenAI

_ = load_dotenv('.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MCP_URL = os.getenv("MCP_URL")

client = OpenAI(api_key=OPENAI_API_KEY)

resp = client.responses.create(
    model="gpt-4.1",
    tools=[
        {
            "type": "mcp",
            "server_label": "my_mcp_server",
            "server_description": "My MCP server to greet user",
            "server_url": MCP_URL,
            "require_approval": "never",
        },
    ],
    input="Hi, this is Markchen1214, how are you?",
)

print(resp)
print(resp.output_text)
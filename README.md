# MCP Demo

A small demo of the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) using LangChain and LangGraph. A ReAct agent, backed by a Groq-hosted LLM, connects to two MCP servers and calls their tools:

| Server | File | Transport | Tools |
|---|---|---|---|
| Math | `mathserver.py` | `stdio` (started by the client) | `add(a, b)`, `multiply(a, b)` |
| Weather | `weather.py` | `streamable-http` at `http://localhost:8000/mcp` | `get_weather(location)` (returns a fixed placeholder response) |

`client.py` uses `MultiServerMCPClient` from `langchain-mcp-adapters` to load tools from both servers. It then builds an agent with `create_react_agent` and asks it a math question and a weather question.

## Project structure

```
.
├── client.py         # MCP client + LangGraph ReAct agent
├── mathserver.py     # Math MCP server (stdio)
├── weather.py        # Weather MCP server (streamable HTTP)
├── main.py           # Placeholder entry point
├── requirements.txt
└── pyproject.toml
```

## Requirements

- Python 3.13+
- A [Groq API key](https://console.groq.com/keys)

## Setup

1. Create and activate a virtual environment, then install dependencies:

   ```bash
   # with uv
   uv venv
   uv pip install -r requirements.txt python-dotenv

   # or with pip
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   # source .venv/bin/activate   # macOS/Linux
   pip install -r requirements.txt python-dotenv
   ```

2. Create a `.env` file in the project root:

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Running

1. Start the weather server in one terminal:

   ```bash
   python weather.py
   ```

   It serves on `http://localhost:8000/mcp`.

2. Run the client in a second terminal, from the project root:

   ```bash
   python client.py
   ```

   The client starts the math server itself over stdio, so you don't need to run `mathserver.py` separately.

Expected output (exact wording depends on the model):

```
Math response: (3 + 5) × 12 = 96
Weather response: It's always raining in California.
```

## Adding your own tools

Define a function with the `@mcp.tool()` decorator in either server. Its type hints and docstring become the tool's schema and description:

```python
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    return a - b
```

To add a new server, add an entry to the `MultiServerMCPClient` config in `client.py`.

## Notes

- `client.py` runs `mathserver.py` by relative path, so run it from the project root (or switch to an absolute path).
- The weather tool is a stub. Replace `get_weather` with a call to a real weather API for live data.
- The model is set in `client.py` (`ChatGroq(model="openai/gpt-oss-120b")`). Any Groq model that supports tool calling will work.

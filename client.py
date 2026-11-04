from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio
import sys

import os
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

async def main():
    client=MultiServerMCPClient(
            {
                "math":{
                    "command":sys.executable,
                    "args":["mathserver.py"], ## Ensure correct absolute path
                    "transport":"stdio",
                
                },
                "weather": {
                    "url": "http://localhost:8000/mcp",  # Ensure server is running here
                    "transport": "streamable_http",
                }
    
            }
        )
    tools=await client.get_tools()
    model=ChatGroq(model="openai/gpt-oss-120b")
    agent=create_react_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)
    

if __name__ == "__main__":
    asyncio.run(main())
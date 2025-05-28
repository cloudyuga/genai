import asyncio
import sys
import os
from typing import Optional
from contextlib import AsyncExitStack
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()  # Load .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str):
        """Connect to MCP server"""
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")

        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(command=command, args=[server_script_path], env=None)

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        print("Connected to server")

    async def process_query(self, query: str) -> str:
        """Use OpenAI with MCP tools to process user query"""

        # List tools from MCP server
        tool_response = await self.session.list_tools()
        tools = tool_response.tools

        # Prepare OpenAI tool schema
        tool_specs = []
        for tool in tools:
            tool_specs.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
        })

        # Step 1: Initial user message
        messages = [{"role": "user", "content": query}]
    
        # Step 2: First call to OpenAI to get tool call suggestion
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tool_specs
        )

        choice = response.choices[0].message
        messages.append(choice)

        if choice.tool_calls:
            tool_call = choice.tool_calls[0]
            fn_name = tool_call.function.name
            fn_args = eval(tool_call.function.arguments)

            # Step 3: Call the actual tool
            tool_result = await self.session.call_tool(fn_name, fn_args)

            # Step 4: Append tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result.content
            })

            # Step 5: Call OpenAI again for final answer
            final_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            result = final_response.choices[0].message.content
            return result

        return "No tool call was made by the model."


    async def close(self):
        await self.exit_stack.aclose()


# Async wrapper for Gradio
client = MCPClient()
loop = asyncio.get_event_loop()

async def setup():
    await client.connect_to_server("hr.py")  # Use your script name here

def ask_openai(user_input):
    return loop.run_until_complete(client.process_query(user_input))


# Launch Gradio after connecting
loop.run_until_complete(setup())

demo = gr.Interface(
    fn=ask_openai,
    inputs=gr.Textbox(lines=2, placeholder="Ask about HR tools or automation..."),
    outputs="text",
    title="MCP + OpenAI Chatbot",
    description="Chat with tools exposed via MCP using OpenAI function calling."
)

demo.launch()

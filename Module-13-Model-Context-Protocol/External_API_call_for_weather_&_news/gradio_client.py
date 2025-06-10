import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastmcp.client import Client
from fastmcp.client.transports import SSETransport
import gradio as gr

# Load OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Global tool list cache
tool_list = []

# Load available tools from MCP
async def load_tools():
    async with Client(transport=SSETransport("http://localhost:8000/sse")) as client:
        tools = await client.list_tools()
        tool_list.clear()
        for tool in tools:
            tool_list.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            })

# Render 🛠️ tool list as HTML
def show_tool_list():
    if not tool_list:
        asyncio.run(load_tools())

    html = "<ul style='padding-left: 1.2em;'>"
    for tool in tool_list:
        html += f"<li>🛠️ <b>{tool['name']}</b>: {tool['description']}</li>"
    html += "</ul>"
    return html

# Main query processor (now handles multiple tools)
async def process_query(query: str):
    async with Client(transport=SSETransport("http://localhost:8000/sse")) as client:
        tools = await client.list_tools()
        tool_specs = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
            } for tool in tools
        ]

        messages = [{"role": "user", "content": query}]
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tool_specs
        )
        choice = response.choices[0].message
        messages.append(choice)

        tool_used_names = []
        tool_outputs = []

        if choice.tool_calls:
            for tool_call in choice.tool_calls:
                fn_name = tool_call.function.name
                fn_args = eval(tool_call.function.arguments)
                tool_result = await client.call_tool(fn_name, fn_args)

                tool_used_names.append(fn_name)
                tool_outputs.append(str(tool_result))

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                })

        final_response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        result = final_response.choices[0].message.content

        return result, ", ".join(tool_used_names) if tool_used_names else "No tool used", "\n\n".join(tool_outputs) if tool_outputs else "N/A"

# Wrapper to run async inside Gradio
def ask_openai(user_input):
    return asyncio.run(process_query(user_input))

# Launch Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# MCP + OpenAI Chatbot")
    gr.Markdown("Chat with tools exposed via MCP using OpenAI function calling.")

    tool_display = gr.HTML()
    demo.load(fn=show_tool_list, inputs=None, outputs=tool_display)

    with gr.Row():
        user_input = gr.Textbox(lines=2, placeholder="Ask about current Weather and News ...", label="Your Question")
        output = gr.Textbox(label="Final Answer")

    with gr.Row():
        tool_used = gr.Textbox(label="Tool Used")
        tool_output = gr.Textbox(label="Tool Output")

    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=ask_openai, inputs=user_input, outputs=[output, tool_used, tool_output])

demo.launch()

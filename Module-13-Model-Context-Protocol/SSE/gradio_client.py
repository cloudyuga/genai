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
openai_client = OpenAI()

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

# Main query processor
async def process_query(query: str):
    async with Client(transport=SSETransport("http://localhost:8000/sse")) as client:
        # Build tool spec for OpenAI function calling
        tools = await client.list_tools()
        tool_specs = [ {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
        } for tool in tools ]

        messages = [{"role": "user", "content": query}]
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

            # Call the selected tool
            tool_result = await client.call_tool(fn_name, fn_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

            final_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            result = final_response.choices[0].message.content
            return result, fn_name, tool_result
        else:
            # ✅ No tool call, just ask GPT again for a normal response
            final_response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            result = final_response.choices[0].message.content
            return result, "No tool used", "N/A"

# Wrapper to run async inside Gradio
def ask_openai(user_input):
    return asyncio.run(process_query(user_input))

# Launch Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# MCP + OpenAI Chatbot")
    gr.Markdown("Chat with tools exposed via MCP using OpenAI function calling.")

    # 🛠️ Show available tools
    tool_display = gr.HTML()
    demo.load(fn=show_tool_list, inputs=None, outputs=tool_display)

    with gr.Row():
        user_input = gr.Textbox(lines=2, placeholder="Ask about HR tools or automation...", label="Your Question")
        output = gr.Textbox(label="Final Answer")

    with gr.Row():
        tool_used = gr.Textbox(label="Tool Used")
        tool_output = gr.Textbox(label="Tool Output")

    submit_btn = gr.Button("Submit")
    submit_btn.click(fn=ask_openai, inputs=user_input, outputs=[output, tool_used, tool_output])

demo.launch()

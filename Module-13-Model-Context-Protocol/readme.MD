

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

-> $env:Path = "C:\Users\hardi\.local\bin;$env:Path"   

# Create a new directory for our project
uv init weather
cd weather

# Create virtual environment and activate it
uv venv
-> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.venv\Scripts\activate

.venv\Scripts\Activate

# Install dependencies
uv add mcp[cli] httpx

# Create our server file
new-item weather.py

code $env:AppData\Claude\claude_desktop_config.json
python weather.py

pip install modelcontextprotocol

What’s happening under the hood
When you ask a question:

The client sends your question to Claude
Claude analyzes the available tools and decides which one(s) to use
The client executes the chosen tool(s) through the MCP server
The results are sent back to Claude
Claude formulates a natural language response
The response is displayed to you!

## Install Claude Desktop

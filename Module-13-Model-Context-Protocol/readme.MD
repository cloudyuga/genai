# Install "uv" : Python package manager

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
pip install modelcontextprotocol

# Create our server file
new-item weather.py

What’s happening under the hood? When you ask a question:

- The client sends your question to Claude

- Claude analyzes the available tools and decides which one(s) to use

- The client executes the chosen tool(s) through the MCP server

- The results are sent back to Claude

- Claude formulates a natural language response

- The response is displayed to you!

# Install Claude Desktop
Visit https://claude.ai/download to download claude desktop in local machine.

Open Claude Application 

- Menu -> Open File -> Settings
- Select Developer mode 
- Edit Config
  It will move to claude_desktop_config.json (refer our codebase). Here we have to run our MCP server for claude.
- We should add our MCP Servers files (hr.py, weather.py, news_weather.py, hrdataset) from where our claude.exe is running
    - for example: In local machine the path is "C:\Users\hardi\AppData\Local\AnthropicClaude\app-0.9.2"
- Refresh/ Reload claude app
- You can see the tools in claude chatbot. 
- You can verify the MCP server from
    - Main Menu -> File -> Settings -> Developer window 
    - You can see the list of Servers
- Your claude desktop is now ready to answer real time weather, news or hrdataset questions.

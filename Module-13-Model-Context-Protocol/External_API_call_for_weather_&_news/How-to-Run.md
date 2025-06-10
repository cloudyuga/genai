## SSE RUN:
### open a terminal

`cd weather -> .venv\Scripts\Activate`

Install fastmcp if it is not there in your venv

`fastmcp run mcp_weather_news.py:mcp --transport sse` 

### Another Terminal(split):

`.venv\Scripts\Activate`

`python gradio_client.py`

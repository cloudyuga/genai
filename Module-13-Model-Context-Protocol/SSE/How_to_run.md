## SSE RUN:
### open a terminal

`cd weather -> .venv\Scripts\Activate`

Install fastmcp if it is not there in your venv

`fastmcp run hr.py:mcp --transport sse` 

### Another Terminal(split):

`.venv\Scripts\Activate`

`python sse_client_new.py`

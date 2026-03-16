from fastmcp import FastMCP

mcp = FastMCP("JournalsMCPServer")

@mcp.tool(
    name="greet_custom",
    description="Greets the user with a custom message.", 
    tags={"greeting", "user interaction"},
    meta={"version": "1.0.0", "author": "ravin"} 
)
async def greet_custom(name: str) -> str:
    """Greets the user with a custom message."""
    return f"Hello, {name}! Lol Welcome to our pizza restaurant! 🍕"

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    transport = "http"
    mcp.run(transport=transport, host=host, port=port)
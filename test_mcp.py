import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp():
    python_path = r"C:\Users\waqas\anaconda3\envs\mcp-env\python.exe"
    server_script = os.path.abspath("mcp_server.py")
    
    print(f"Starting MCP server with: {python_path} {server_script}")
    
    # Define server parameters
    server_params = StdioServerParameters(
        command=python_path,
        args=[server_script],
        env=None
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                print("Initializing session...")
                await session.initialize()
                print("Session initialized.")

                # List tools
                print("Listing tools...")
                tools = await session.list_tools()
                print("Successfully connected to MCP Server!")
                print(f"Available tools: {[tool.name for tool in tools.tools]}")

                # Test list_patients with a search
                if any(t.name == "list_patients" for t in tools.tools):
                    print("\nTesting 'list_patients' tool...")
                    result = await session.call_tool("list_patients", arguments={"search": "John"})
                    print(f"Result content: {str(result.content)[:500]}...")
                else:
                    print("\n'list_patients' tool not found!")

    except Exception as e:
        print(f"Error during MCP test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp())

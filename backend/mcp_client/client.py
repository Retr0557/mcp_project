"""
MCP Client for Zomato with Claude AI Integration
"""

import asyncio
import json
import os
from typing import Optional, List, Dict, Any
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()


class ZomatoMCPClient:
    """MCP Client that connects to Zomato server and uses Claude for AI interactions."""
    
    def __init__(self):
        self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.session: Optional[ClientSession] = None
        self.available_tools = []
        self.conversation_history = []
        
    async def connect_to_server(self):
        """Connect to the Zomato MCP server."""
        server_params = StdioServerParameters(
            command="python",
            args=["-u", "backend/zomato_server/server.py"],
            env=None
        )
        
        stdio_transport = await stdio_client(server_params)
        self.stdio, self.write = stdio_transport
        self.session = ClientSession(self.stdio, self.write)
        
        await self.session.initialize()
        
        # List available tools
        response = await self.session.list_tools()
        self.available_tools = response.tools
        print(f"Connected to Zomato MCP Server. Available tools: {len(self.available_tools)}")
        
    async def process_user_request(self, user_message: str) -> str:
        """Process user request through Claude and execute MCP tools as needed."""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare tools for Claude
        claude_tools = []
        for tool in self.available_tools:
            claude_tools.append({
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            })
        
        # Initial Claude request
        response = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            tools=claude_tools,
            messages=self.conversation_history
        )
        
        # Process tool calls
        while response.stop_reason == "tool_use":
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            # Execute tool calls
            tool_results = []
            for content_block in response.content:
                if content_block.type == "tool_use":
                    tool_name = content_block.name
                    tool_args = content_block.input
                    
                    print(f"\nExecuting tool: {tool_name}")
                    print(f"Arguments: {json.dumps(tool_args, indent=2)}")
                    
                    # Call MCP tool
                    result = await self.session.call_tool(tool_name, tool_args)
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content_block.id,
                        "content": result.content[0].text
                    })
            
            # Add tool results to history
            self.conversation_history.append({
                "role": "user",
                "content": tool_results
            })
            
            # Continue conversation with Claude
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
                tools=claude_tools,
                messages=self.conversation_history
            )
        
        # Extract final text response
        final_response = ""
        for content_block in response.content:
            if hasattr(content_block, "text"):
                final_response += content_block.text
        
        # Add final assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": final_response
        })
        
        return final_response
    
    async def close(self):
        """Close the MCP session."""
        if self.session:
            await self.session.__aexit__(None, None, None)


async def main():
    """Main function for testing the MCP client."""
    client = ZomatoMCPClient()
    
    try:
        print("Connecting to Zomato MCP Server...")
        await client.connect_to_server()
        print("Connected!\n")
        
        # Interactive loop
        print("Zomato AI Assistant (powered by Claude)")
        print("=" * 50)
        print("You can ask me to:")
        print("- Search for restaurants")
        print("- View menus")
        print("- Place orders with Cash on Delivery")
        print("- Check order status")
        print("\nType 'quit' to exit\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
            
            if not user_input:
                continue
            
            try:
                response = await client.process_user_request(user_input)
                print(f"\nAssistant: {response}\n")
            except Exception as e:
                print(f"\nError: {str(e)}\n")
    
    finally:
        await client.close()
        print("Disconnected from server.")


if __name__ == "__main__":
    asyncio.run(main())

"""
MCP Client for Zomato with OpenAI Integration
"""

import asyncio
import json
import os
from typing import Optional, List, Dict, Any
from openai import OpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()


class ZomatoMCPClient:
    """MCP Client that connects to Zomato server and uses OpenAI for AI interactions."""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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
        """Process user request through OpenAI and execute MCP tools as needed."""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare tools for OpenAI
        openai_tools = []
        for tool in self.available_tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })
        
        # Initial OpenAI request
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            max_tokens=4096,
            tools=openai_tools if openai_tools else None,
            messages=self.conversation_history
        )
        
        # Process tool calls
        while response.choices[0].finish_reason == "tool_calls":
            assistant_message = response.choices[0].message
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            })
            
            # Execute tool calls
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)
                
                print(f"\nExecuting tool: {tool_name}")
                print(f"Arguments: {json.dumps(tool_args, indent=2)}")
                
                # Call MCP tool
                result = await self.session.call_tool(tool_name, tool_args)
                
                # Add tool result to history
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result.content[0].text
                })
            
            # Continue conversation with OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                max_tokens=4096,
                tools=openai_tools if openai_tools else None,
                messages=self.conversation_history
            )
        
        # Extract final text response
        final_response = response.choices[0].message.content or ""
        
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
        print("Zomato AI Assistant (powered by OpenAI)")
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

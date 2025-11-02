"""
FastAPI Backend for Zomato MCP Client
Provides REST API endpoints for the React frontend
"""

import asyncio
import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import sys

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_client.client import ZomatoMCPClient

load_dotenv()

app = FastAPI(title="Zomato MCP API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global client instance
mcp_client: ZomatoMCPClient = None


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    session_id: str


# Store sessions
sessions: Dict[str, ZomatoMCPClient] = {}


@app.on_event("startup")
async def startup_event():
    """Initialize MCP client on startup."""
    global mcp_client
    print("Initializing Zomato MCP Client...")
    mcp_client = ZomatoMCPClient()
    await mcp_client.connect_to_server()
    print("MCP Client connected and ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Close MCP client on shutdown."""
    if mcp_client:
        await mcp_client.close()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Zomato MCP API"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user message through OpenAI GPT and MCP tools.
    """
    try:
        if not mcp_client:
            raise HTTPException(status_code=503, detail="MCP client not initialized")
        
        response = await mcp_client.process_user_request(request.message)
        
        return ChatResponse(
            response=response,
            session_id=request.session_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List available MCP tools."""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
            for tool in mcp_client.available_tools
        ]
    }


@app.post("/reset")
async def reset_conversation():
    """Reset the conversation history."""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    mcp_client.conversation_history = []
    return {"status": "conversation reset"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

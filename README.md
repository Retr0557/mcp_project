# Zomato MCP Client Project

A comprehensive MCP (Model Context Protocol) client application that communicates with a Zomato MCP server to access restaurant data and perform actions like placing orders with Cash on Delivery payment method. The application uses OpenAI GPT as the AI interface and features a React.js frontend.

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────────┐
│  React Frontend │ <──> │  FastAPI Backend │ <──> │  Zomato MCP Server  │
│   (Port 3000)   │ HTTP │   (Port 8000)    │ MCP  │      (stdio)        │
└─────────────────┘      └──────────────────┘      └─────────────────────┘
                                  │
                                  │
                         ┌────────▼─────────┐
                         │    OpenAI GPT    │
                         │      API         │
                         └──────────────────┘
```

## Features

- 🍕 **Restaurant Search**: Search for restaurants by cuisine type or name
- 📋 **Menu Viewing**: View detailed menus for any restaurant
- 🛒 **Order Placement**: Place orders with Cash on Delivery (COD) payment
- 📦 **Order Tracking**: Check the status of placed orders
- 🤖 **AI-Powered**: Natural language interaction powered by OpenAI GPT
- 💬 **Interactive Chat**: Beautiful, responsive chat interface

## Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend Server

From the `backend` directory:
```bash
python api.py
```

The FastAPI server will start on `http://localhost:8000`

### Start the Frontend

From the `frontend` directory:
```bash
npm run dev
```

The React app will start on `http://localhost:3000`

### Testing the MCP Client Directly (Optional)

You can test the MCP client without the frontend:
```bash
cd backend
python mcp_client/client.py
```

## Usage Examples

Once the application is running, you can interact with it using natural language:

- "Show me Italian restaurants"
- "What's on the menu at Pizza Palace?"
- "I want to order a Margherita Pizza from Pizza Palace, deliver to 123 Main St"
- "Place an order for 2 burgers from Burger Barn with cash on delivery to 456 Oak Ave"
- "Check the status of order ORD1001"

## Project Structure

```
mcp_project/
├── backend/
│   ├── mcp_client/
│   │   └── client.py           # MCP client with Claude integration
│   ├── zomato_server/
│   │   └── server.py           # Zomato MCP server
│   ├── api.py                  # FastAPI REST API
│   ├── requirements.txt        # Python dependencies
│   └── .env.example           # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatMessage.jsx
│   │   │   ├── ChatMessage.css
│   │   │   ├── ChatInput.jsx
│   │   │   └── ChatInput.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## API Endpoints

### POST /chat
Send a message to the AI assistant
```json
{
  "message": "Show me Italian restaurants",
  "session_id": "default"
}
```

### GET /tools
List available MCP tools

### POST /reset
Reset the conversation history

## MCP Tools

The Zomato MCP server provides the following tools:

1. **search_restaurants**: Search for restaurants by cuisine or name
2. **get_restaurant_menu**: Get the menu for a specific restaurant
3. **place_order**: Place an order with COD payment
4. **get_order_status**: Check the status of an order

## Technologies Used

### Backend
- **Python**: Core language
- **MCP**: Model Context Protocol for server communication
- **OpenAI GPT**: AI model for natural language processing
- **FastAPI**: REST API framework
- **Uvicorn**: ASGI server

### Frontend
- **React.js**: UI framework
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **CSS3**: Styling

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_api_key_here
```

## Development

### Adding New Restaurants

Edit `backend/zomato_server/server.py` and add entries to the `RESTAURANTS` list.

### Adding New MCP Tools

1. Add tool definition in `list_tools()` function
2. Add tool handler in `call_tool()` function

### Customizing the Frontend

- Modify components in `frontend/src/components/`
- Update styles in the corresponding `.css` files
- Adjust layout in `frontend/src/App.jsx`

## Troubleshooting

### Backend won't start
- Ensure Python dependencies are installed: `pip install -r requirements.txt`
- Check that your OPENAI_API_KEY is set in `.env`

### Frontend can't connect to backend
- Ensure the backend is running on port 8000
- Check CORS settings in `api.py`

### MCP server communication issues
- Verify that the server path in `client.py` is correct
- Ensure the server script has execute permissions

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
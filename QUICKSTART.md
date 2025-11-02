# Quick Start Guide

## Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- OpenAI API key (get it from https://platform.openai.com/)

## Setup Instructions

### 1. Get Your OpenAI API Key
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (it starts with `sk-`)

### 2. Configure the Backend
```bash
cd backend
cp .env.example .env
# Edit .env and paste your API key
```

Your `.env` file should look like:
```
OPENAI_API_KEY=sk-...
```

### 3. Install Dependencies

#### Backend (Python)
```bash
cd backend
pip install -r requirements.txt
```

#### Frontend (Node.js)
```bash
cd frontend
npm install
```

### 4. Start the Application

#### Option A: Using the startup script (Recommended for Unix/Linux/Mac)
```bash
./start.sh
```

#### Option B: Manual startup

**Terminal 1 - Start Backend:**
```bash
cd backend
python api.py
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

## Accessing the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Usage Examples

### 1. Search for Restaurants
```
User: "Show me Italian restaurants"
```

### 2. View Menu
```
User: "What's on the menu at Pizza Palace?"
```

### 3. Place an Order
```
User: "I want to order a Margherita Pizza from Pizza Palace, deliver to 123 Main Street"
```

Or be more specific:
```
User: "Place an order for 2 Pepperoni Pizzas from Pizza Palace with cash on delivery to 456 Oak Avenue"
```

### 4. Check Order Status
```
User: "What's the status of order ORD1001?"
```

## Available Restaurants

1. **Pizza Palace** (Italian)
   - Margherita Pizza - ₹299
   - Pepperoni Pizza - ₹399
   - Veggie Supreme - ₹349

2. **Burger Barn** (American)
   - Classic Burger - ₹199
   - Cheese Burger - ₹249
   - Veggie Burger - ₹179

3. **Sushi Station** (Japanese)
   - California Roll - ₹449
   - Salmon Nigiri - ₹399
   - Vegetable Tempura - ₹299

4. **Curry Corner** (Indian)
   - Chicken Tikka Masala - ₹349
   - Paneer Butter Masala - ₹299
   - Biryani - ₹279

## Payment Method

This application only supports **Cash on Delivery (COD)** as the payment method. When placing orders, the system automatically uses COD.

## Troubleshooting

### Backend won't start
- **Issue:** `ModuleNotFoundError: No module named 'openai'`
  - **Solution:** Run `pip install -r requirements.txt` in the backend directory

- **Issue:** `Error: OPENAI_API_KEY not set`
  - **Solution:** Create a `.env` file in the backend directory and add your API key

### Frontend won't start
- **Issue:** `Cannot find module 'react'`
  - **Solution:** Run `npm install` in the frontend directory

- **Issue:** `Port 3000 is already in use`
  - **Solution:** Stop other applications using port 3000 or change the port in `vite.config.js`

### Connection Issues
- **Issue:** Frontend can't connect to backend
  - **Solution:** Ensure backend is running on port 8000
  - Check the browser console for CORS errors

### API Key Issues
- **Issue:** `401 Unauthorized` errors
  - **Solution:** Verify your OpenAI API key is correct and has sufficient credits

## Advanced Usage

### Testing the MCP Client Directly (CLI)
You can test the MCP client without the web interface:

```bash
cd backend
python mcp_client/client.py
```

This starts an interactive CLI where you can chat directly with the AI assistant.

### Resetting the Conversation
Click the "Reset Chat" button in the top-right corner of the web interface, or send a POST request to `/reset`.

### Viewing Available Tools
Visit http://localhost:8000/tools to see all available MCP tools and their schemas.

## Security Notes

- Never commit your `.env` file with the API key
- Keep your OpenAI API key secure
- The `.env` file is already in `.gitignore` to prevent accidental commits

## Support

If you encounter issues:
1. Check the browser console for errors
2. Check the backend terminal for error messages
3. Ensure all dependencies are installed
4. Verify your API key is valid

## Next Steps

- Add more restaurants to the database
- Implement additional payment methods
- Add user authentication
- Integrate with a real Zomato API
- Add order history tracking

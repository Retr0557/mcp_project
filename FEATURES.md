# Zomato MCP Client - Features Overview

## 🎯 Project Overview

This project demonstrates a complete implementation of the Model Context Protocol (MCP) by building a Zomato food ordering assistant. It showcases how MCP can be used to create AI-powered applications that interact with external systems through a standardized protocol.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              React.js Chat Interface                      │  │
│  │  - Message display with chat bubbles                      │  │
│  │  - Input field with send button                           │  │
│  │  - Reset conversation button                              │  │
│  │  - Loading indicators                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │ HTTP/REST
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  API Endpoints:                                           │  │
│  │  - POST /chat        (Send messages)                      │  │
│  │  - GET /tools        (List available tools)               │  │
│  │  - POST /reset       (Reset conversation)                 │  │
│  │  - GET /             (Health check)                       │  │
│  └───────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     MCP Client                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  - Manages MCP session with Zomato server                 │  │
│  │  - Maintains conversation history                         │  │
│  │  - Coordinates between Claude and MCP tools               │  │
│  └───────────────────────────────────────────────────────────┘  │
└──────────┬────────────────────────────────────────┬─────────────┘
           │                                        │
           │ MCP Protocol (stdio)                   │ API Calls
           ▼                                        ▼
┌──────────────────────────┐         ┌──────────────────────────┐
│   Zomato MCP Server      │         │   Anthropic Claude API   │
│                          │         │                          │
│  Tools:                  │         │  - Natural language      │
│  - search_restaurants    │         │    understanding         │
│  - get_restaurant_menu   │         │  - Tool use capability   │
│  - place_order           │         │  - Context maintenance   │
│  - get_order_status      │         │                          │
│                          │         │  Model: Claude 3.5       │
│  Data:                   │         │         Sonnet           │
│  - Restaurant database   │         │                          │
│  - Order storage         │         └──────────────────────────┘
└──────────────────────────┘
```

## ✨ Key Features

### 1. Natural Language Restaurant Search
- Search by cuisine type (Italian, Japanese, Indian, American)
- Search by restaurant name
- Fuzzy matching for flexible queries
- Returns ratings, delivery time, and cuisine info

**Example:**
```
User: "Show me Italian restaurants"
AI: Lists Pizza Palace with rating 4.5 and 30-40 mins delivery
```

### 2. Interactive Menu Browsing
- View complete menu for any restaurant
- See prices in Indian Rupees (₹)
- Get detailed item information

**Example:**
```
User: "What's on the menu at Pizza Palace?"
AI: Displays Margherita (₹299), Pepperoni (₹399), Veggie Supreme (₹349)
```

### 3. Smart Order Placement
- Natural language order specification
- Automatic item matching
- Quantity support
- Address collection
- COD payment enforcement
- Order confirmation with ID

**Example:**
```
User: "I want to order 2 Pepperoni Pizzas from Pizza Palace"
AI: "I'll need a delivery address..."
User: "123 Main Street"
AI: Confirms order with total ₹798, Order ID: ORD1001
```

### 4. Order Status Tracking
- Check order status by ID
- View order details
- See estimated delivery time

**Example:**
```
User: "What's the status of order ORD1001?"
AI: Shows complete order details and current status
```

### 5. AI-Powered Intelligence
- Understands context and intent
- Handles incomplete information gracefully
- Asks clarifying questions
- Makes recommendations
- Maintains conversation flow

**Example:**
```
User: "I'm hungry"
AI: "I can help! What type of cuisine are you in the mood for?"
User: "Something spicy"
AI: Recommends Curry Corner with spicy Indian dishes
```

## 🛠️ Technical Highlights

### Backend Implementation

#### MCP Server (Zomato)
- **Protocol:** Standard MCP over stdio
- **Tools:** 4 tools (search, menu, order, status)
- **Data:** In-memory restaurant and order databases
- **Thread-Safety:** Lock-protected order operations
- **Error Handling:** Comprehensive error messages

#### MCP Client
- **Session Management:** Persistent MCP session
- **Tool Discovery:** Dynamic tool listing
- **Conversation:** History maintenance
- **Integration:** Seamless Claude API integration

#### FastAPI Backend
- **Async Operations:** Full async/await support
- **CORS:** Configured for frontend access
- **Error Handling:** HTTP status codes and messages
- **Health Checks:** Status endpoint

### Frontend Implementation

#### React Components
- **App.jsx:** Main application container
- **ChatMessage.jsx:** Individual message display
- **ChatInput.jsx:** User input component

#### Styling
- **Responsive Design:** Mobile, tablet, desktop
- **Modern UI:** Gradient backgrounds, animations
- **Accessibility:** Keyboard navigation, screen reader support

#### State Management
- **Messages:** Array of conversation history
- **Loading:** Boolean for API call states
- **Sessions:** Support for multiple conversations

## 🔒 Security Features

### 1. API Key Protection
- Environment variable storage
- Not committed to repository
- Validated at startup

### 2. Input Validation
- Payment method verification (COD only)
- Restaurant ID validation
- Item ID validation
- Address requirement

### 3. Thread Safety
- Lock-protected order storage
- Race condition prevention
- Concurrent request handling

### 4. Dependency Security
- All packages scanned for vulnerabilities
- FastAPI updated to 0.109.1+ (ReDoS fix)
- Vite updated to 6.0.0+ (esbuild fix)
- Zero vulnerabilities in final build

### 5. CORS Configuration
- Restricted to localhost origins
- Credential support enabled
- Method whitelisting

## 📊 Data Models

### Restaurant
```javascript
{
  id: string,
  name: string,
  cuisine: string,
  rating: number,
  delivery_time: string,
  menu: MenuItem[]
}
```

### MenuItem
```javascript
{
  id: string,
  name: string,
  price: number
}
```

### Order
```javascript
{
  order_id: string,
  restaurant: string,
  items: OrderItem[],
  total: number,
  delivery_address: string,
  payment_method: "Cash on Delivery",
  status: string,
  estimated_delivery: string
}
```

### OrderItem
```javascript
{
  name: string,
  quantity: number,
  price: number
}
```

## 🎨 UI/UX Features

### Visual Design
- **Color Scheme:** Purple gradient theme
- **Typography:** Modern sans-serif fonts
- **Icons:** Emoji for personality (🍕, 🤖, 👤)
- **Shadows:** Depth and elevation

### Interactions
- **Smooth Animations:** Message fade-in
- **Loading States:** Typing indicator with animated dots
- **Hover Effects:** Button transformations
- **Responsive Layout:** Adapts to screen size

### User Feedback
- **Loading Indicators:** Shows when processing
- **Error Messages:** Clear, helpful error text
- **Confirmations:** Order details displayed
- **Status Updates:** Real-time status information

## 📈 Performance Characteristics

### Response Times
- Restaurant search: < 2 seconds
- Menu display: < 2 seconds
- Order placement: < 3 seconds
- Order status: < 1 second

### Scalability
- Single server instance
- Memory-based storage
- Stdio protocol (single process)
- Suitable for: Demo, development, small deployments

### Limitations
- No database persistence
- Single server instance only
- In-memory order storage
- Not suitable for production scale

## 🚀 Deployment Options

### Development
```bash
# Backend
cd backend && python api.py

# Frontend
cd frontend && npm run dev
```

### Production Build
```bash
# Frontend build
cd frontend && npm run build

# Serve with production server
# Backend with multiple workers
uvicorn api:app --workers 4 --host 0.0.0.0 --port 8000
```

## 🔮 Future Enhancements

### Possible Improvements
1. **Database Integration:** PostgreSQL for persistence
2. **Authentication:** User accounts and login
3. **Real Zomato API:** Connect to actual Zomato
4. **Payment Gateway:** Real payment processing
5. **Order History:** User order tracking
6. **Ratings & Reviews:** Customer feedback
7. **Real-time Updates:** WebSocket for live status
8. **Mobile App:** React Native version
9. **Admin Panel:** Restaurant management
10. **Analytics:** Usage statistics and insights

## 📝 Code Quality

### Best Practices
- ✅ Type hints in Python
- ✅ Async/await patterns
- ✅ Error handling
- ✅ Code documentation
- ✅ Component modularity
- ✅ Separation of concerns

### Testing
- Unit tests can be added for MCP tools
- Integration tests for API endpoints
- E2E tests for complete flows
- Manual testing guide provided

## 🎓 Learning Resources

This project demonstrates:
- MCP protocol implementation
- Claude AI integration
- FastAPI development
- React.js application structure
- Async Python programming
- RESTful API design
- Modern frontend development

## 📄 License

MIT License - Free to use, modify, and distribute

## 🤝 Contributing

Contributions welcome! Areas for contribution:
- Additional restaurant data
- New MCP tools
- UI improvements
- Test coverage
- Documentation
- Bug fixes

# Testing and Demo Guide

## Overview
This guide helps you test the MCP client application without needing to manually type commands.

## Testing Scenarios

### Scenario 1: Restaurant Discovery
**Objective:** Test restaurant search functionality

**Test Steps:**
1. Start the application
2. Send: "Show me all Italian restaurants"
3. **Expected Result:** Should display Pizza Palace with details
4. Send: "What about Japanese food?"
5. **Expected Result:** Should display Sushi Station

### Scenario 2: Menu Exploration
**Objective:** Test menu viewing functionality

**Test Steps:**
1. Send: "Show me the menu at Pizza Palace"
2. **Expected Result:** Should display all pizza items with prices
3. Send: "What items does Burger Barn have?"
4. **Expected Result:** Should display burger menu items

### Scenario 3: Order Placement
**Objective:** Test end-to-end order placement with COD

**Test Steps:**
1. Send: "I want to order a Margherita Pizza from Pizza Palace"
2. AI will ask for delivery address
3. Send: "Deliver to 123 Main Street, Apartment 4B"
4. **Expected Result:** Order confirmation with order ID, total, and COD payment
5. Note the order ID (e.g., ORD1001)

### Scenario 4: Multiple Items Order
**Objective:** Test ordering multiple items

**Test Steps:**
1. Send: "I want to order 2 Pepperoni Pizzas and 1 Veggie Supreme from Pizza Palace with cash on delivery"
2. Provide address: "456 Oak Avenue"
3. **Expected Result:** Order with multiple items, correct total calculation

### Scenario 5: Order Tracking
**Objective:** Test order status checking

**Test Steps:**
1. After placing an order, note the order ID
2. Send: "What's the status of order ORD1001?"
3. **Expected Result:** Order details with current status

### Scenario 6: Complex Queries
**Objective:** Test AI's understanding of complex requests

**Test Steps:**
1. Send: "I'm in the mood for something spicy. What do you recommend?"
2. **Expected Result:** AI suggests restaurants with spicy options
3. Send: "I have ₹300 budget. What can I order?"
4. **Expected Result:** AI recommends items within budget

## Automated Test Commands

For quick testing, you can copy-paste these commands:

```
# Test 1: Search
Show me Italian restaurants

# Test 2: Menu
What's on the menu at Pizza Palace?

# Test 3: Simple Order
I want to order a Margherita Pizza from Pizza Palace, deliver to 123 Main St

# Test 4: Complex Order
Place an order for 2 Chicken Tikka Masala from Curry Corner with cash on delivery to 456 Oak Avenue, Apt 5C

# Test 5: Status Check
Check the status of order ORD1001
```

## Expected Behavior

### Restaurant Search
- AI should parse the cuisine/name from query
- Display matching restaurants with ratings and delivery time
- Handle partial matches and typos gracefully

### Menu Display
- Show all items with names and prices
- Format prices in INR (₹)
- Include restaurant information

### Order Placement
- Accept orders in natural language
- Request missing information (address, items)
- Confirm COD payment method
- Return order ID and estimated delivery time
- Calculate correct totals

### Order Status
- Retrieve order by ID
- Display all order details
- Show current status

## Testing Checklist

- [ ] Can search restaurants by cuisine
- [ ] Can search restaurants by name
- [ ] Can view restaurant menus
- [ ] Can place single item orders
- [ ] Can place multiple item orders
- [ ] Orders use Cash on Delivery
- [ ] Order totals calculate correctly
- [ ] Receive order confirmation with ID
- [ ] Can check order status
- [ ] AI handles incomplete information gracefully
- [ ] UI is responsive and user-friendly
- [ ] Error messages are clear and helpful

## Performance Testing

### Response Time
- Restaurant search: < 2 seconds
- Menu display: < 2 seconds
- Order placement: < 3 seconds
- Order status: < 1 second

### Concurrent Users
The application should handle multiple simultaneous conversations.

## Known Limitations

1. **Simulated Data:** This is a demo with simulated restaurant data
2. **No Real Payment:** COD is the only payment method (simulated)
3. **No Real Delivery:** Orders are stored in memory only
4. **Session Storage:** Conversation history is not persisted
5. **Single Instance:** Multiple users share the same order database

## Debugging Tips

### Enable Verbose Logging
Check the backend terminal for detailed logs of:
- MCP tool calls
- Claude API requests
- Order processing

### Common Issues

**Issue:** AI doesn't understand the request
- **Solution:** Rephrase more explicitly (e.g., "Search for restaurants" instead of "restaurants")

**Issue:** Order total is incorrect
- **Solution:** Check the menu prices in `zomato_server/server.py`

**Issue:** Can't find order by ID
- **Solution:** Verify the order was placed successfully and use the exact order ID

## API Testing

You can test the backend API directly using curl:

### Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me Italian restaurants", "session_id": "test"}'
```

### List Available Tools
```bash
curl http://localhost:8000/tools
```

### Reset Conversation
```bash
curl -X POST http://localhost:8000/reset
```

## Frontend Testing

### Browser Compatibility
Test in:
- Chrome/Edge (Chromium)
- Firefox
- Safari

### Responsive Design
Test on:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

### Accessibility
- Keyboard navigation should work
- Screen readers should be able to read messages
- Sufficient color contrast

## Security Testing

1. **API Key Protection:** Verify `.env` file is not exposed
2. **Input Validation:** Try sending malicious input
3. **CORS:** Verify only localhost can access API
4. **XSS:** Try injecting scripts in messages

## Next Steps After Testing

1. Document any bugs found
2. Note performance bottlenecks
3. Gather user feedback
4. Identify missing features
5. Plan improvements

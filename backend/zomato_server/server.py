"""
Zomato MCP Server
A simulated MCP server that provides Zomato restaurant data and order placement functionality.
"""

import asyncio
import json
from typing import Any, Sequence
from mcp.server import Server
from mcp.types import Tool, TextContent, Resource, EmbeddedResource
from mcp.server.stdio import stdio_server


# Simulated restaurant database
RESTAURANTS = [
    {
        "id": "1",
        "name": "Pizza Palace",
        "cuisine": "Italian",
        "rating": 4.5,
        "delivery_time": "30-40 mins",
        "menu": [
            {"id": "101", "name": "Margherita Pizza", "price": 299},
            {"id": "102", "name": "Pepperoni Pizza", "price": 399},
            {"id": "103", "name": "Veggie Supreme", "price": 349},
        ]
    },
    {
        "id": "2",
        "name": "Burger Barn",
        "cuisine": "American",
        "rating": 4.2,
        "delivery_time": "25-35 mins",
        "menu": [
            {"id": "201", "name": "Classic Burger", "price": 199},
            {"id": "202", "name": "Cheese Burger", "price": 249},
            {"id": "203", "name": "Veggie Burger", "price": 179},
        ]
    },
    {
        "id": "3",
        "name": "Sushi Station",
        "cuisine": "Japanese",
        "rating": 4.7,
        "delivery_time": "40-50 mins",
        "menu": [
            {"id": "301", "name": "California Roll", "price": 449},
            {"id": "302", "name": "Salmon Nigiri", "price": 399},
            {"id": "303", "name": "Vegetable Tempura", "price": 299},
        ]
    },
    {
        "id": "4",
        "name": "Curry Corner",
        "cuisine": "Indian",
        "rating": 4.4,
        "delivery_time": "35-45 mins",
        "menu": [
            {"id": "401", "name": "Chicken Tikka Masala", "price": 349},
            {"id": "402", "name": "Paneer Butter Masala", "price": 299},
            {"id": "403", "name": "Biryani", "price": 279},
        ]
    }
]

# Order storage
orders = []


app = Server("zomato-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for the Zomato MCP server."""
    return [
        Tool(
            name="search_restaurants",
            description="Search for restaurants by cuisine type or name",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (cuisine or restaurant name)"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_restaurant_menu",
            description="Get the menu for a specific restaurant",
            inputSchema={
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "string",
                        "description": "The ID of the restaurant"
                    }
                },
                "required": ["restaurant_id"]
            }
        ),
        Tool(
            name="place_order",
            description="Place an order with cash on delivery payment",
            inputSchema={
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "string",
                        "description": "The ID of the restaurant"
                    },
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "item_id": {"type": "string"},
                                "quantity": {"type": "integer"}
                            }
                        },
                        "description": "List of items to order"
                    },
                    "delivery_address": {
                        "type": "string",
                        "description": "Delivery address"
                    },
                    "payment_method": {
                        "type": "string",
                        "description": "Payment method (must be 'cod' for cash on delivery)"
                    }
                },
                "required": ["restaurant_id", "items", "delivery_address", "payment_method"]
            }
        ),
        Tool(
            name="get_order_status",
            description="Get the status of a placed order",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The ID of the order"
                    }
                },
                "required": ["order_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls for the Zomato MCP server."""
    
    if name == "search_restaurants":
        query = arguments.get("query", "").lower()
        results = [
            r for r in RESTAURANTS
            if query in r["name"].lower() or query in r["cuisine"].lower()
        ]
        return [TextContent(
            type="text",
            text=json.dumps(results, indent=2)
        )]
    
    elif name == "get_restaurant_menu":
        restaurant_id = arguments.get("restaurant_id")
        restaurant = next((r for r in RESTAURANTS if r["id"] == restaurant_id), None)
        if restaurant:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "restaurant": restaurant["name"],
                    "menu": restaurant["menu"]
                }, indent=2)
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Restaurant not found"})
            )]
    
    elif name == "place_order":
        restaurant_id = arguments.get("restaurant_id")
        items = arguments.get("items", [])
        delivery_address = arguments.get("delivery_address")
        payment_method = arguments.get("payment_method")
        
        if payment_method.lower() != "cod":
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Only Cash on Delivery (COD) is supported"})
            )]
        
        restaurant = next((r for r in RESTAURANTS if r["id"] == restaurant_id), None)
        if not restaurant:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Restaurant not found"})
            )]
        
        # Calculate total
        total = 0
        order_items = []
        for item in items:
            menu_item = next((m for m in restaurant["menu"] if m["id"] == item["item_id"]), None)
            if menu_item:
                quantity = item.get("quantity", 1)
                total += menu_item["price"] * quantity
                order_items.append({
                    "name": menu_item["name"],
                    "quantity": quantity,
                    "price": menu_item["price"]
                })
        
        # Create order
        order_id = f"ORD{len(orders) + 1001}"
        order = {
            "order_id": order_id,
            "restaurant": restaurant["name"],
            "items": order_items,
            "total": total,
            "delivery_address": delivery_address,
            "payment_method": "Cash on Delivery",
            "status": "Order Placed",
            "estimated_delivery": restaurant["delivery_time"]
        }
        orders.append(order)
        
        return [TextContent(
            type="text",
            text=json.dumps(order, indent=2)
        )]
    
    elif name == "get_order_status":
        order_id = arguments.get("order_id")
        order = next((o for o in orders if o["order_id"] == order_id), None)
        if order:
            return [TextContent(
                type="text",
                text=json.dumps(order, indent=2)
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": "Order not found"})
            )]
    
    return [TextContent(
        type="text",
        text=json.dumps({"error": f"Unknown tool: {name}"})
    )]


async def main():
    """Run the Zomato MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())

"""
Example script demonstrating how to use the Zomato MCP Client programmatically.
This script runs a series of automated tests without user interaction.
"""

import asyncio
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_client.client import ZomatoMCPClient


async def run_demo():
    """Run a complete demo of the MCP client capabilities."""
    
    # Initialize client
    client = ZomatoMCPClient()
    
    print("=" * 70)
    print("ZOMATO MCP CLIENT - AUTOMATED DEMO")
    print("=" * 70)
    print()
    
    try:
        # Connect to server
        print("🔌 Connecting to Zomato MCP Server...")
        await client.connect_to_server()
        print("✅ Connected successfully!\n")
        
        # Demo scenarios
        scenarios = [
            {
                "name": "Restaurant Search - Italian Cuisine",
                "message": "Show me Italian restaurants"
            },
            {
                "name": "View Menu",
                "message": "What's on the menu at Pizza Palace?"
            },
            {
                "name": "Place Simple Order",
                "message": "I want to order a Margherita Pizza from Pizza Palace, deliver to 123 Main Street"
            },
            {
                "name": "Search Different Cuisine",
                "message": "Show me Japanese restaurants"
            },
            {
                "name": "Complex Order",
                "message": "I want to order 2 Pepperoni Pizzas and 1 Veggie Supreme from Pizza Palace with cash on delivery to 456 Oak Avenue, Apartment 4B"
            },
            {
                "name": "Check Order Status",
                "message": "What's the status of order ORD1001?"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{'=' * 70}")
            print(f"SCENARIO {i}: {scenario['name']}")
            print(f"{'=' * 70}")
            print(f"User: {scenario['message']}\n")
            
            try:
                response = await client.process_user_request(scenario['message'])
                print(f"Assistant: {response}\n")
                
                # Wait a bit between requests
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"❌ Error in scenario {i}: {str(e)}\n")
        
        print("\n" + "=" * 70)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")
        return False
    
    finally:
        await client.close()
        print("\n🔌 Disconnected from server.")
    
    return True


async def run_single_query(query: str):
    """Run a single query against the MCP client."""
    client = ZomatoMCPClient()
    
    try:
        print("Connecting to server...")
        await client.connect_to_server()
        print("Connected!\n")
        
        print(f"User: {query}\n")
        response = await client.process_user_request(query)
        print(f"Assistant: {response}\n")
        
    finally:
        await client.close()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Zomato MCP Client Demo Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run full automated demo
  python demo.py
  
  # Run a single query
  python demo.py --query "Show me Italian restaurants"
  
  # Interactive mode
  python demo.py --interactive
        """
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Run a single query'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode'
    )
    
    args = parser.parse_args()
    
    if args.query:
        # Single query mode
        asyncio.run(run_single_query(args.query))
    elif args.interactive:
        # Import and run the interactive client
        from mcp_client.client import main as interactive_main
        asyncio.run(interactive_main())
    else:
        # Run full demo
        asyncio.run(run_demo())


if __name__ == "__main__":
    main()

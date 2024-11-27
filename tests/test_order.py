import asyncio
from datetime import datetime
from decimal import Decimal

from api.controllers.order_controller import update_order
from client.order_client import OrderClient


async def test_menu_operations():
    client = OrderClient("http://127.0.0.1:8000")

    # Get all items
    all_items = client.get_all_orders()
    print(f"All items: {all_items}")

    # Create a menu item
    new_order = \
    {
      "order_number": "000003",
      "items": [
        {
          "item": {
            "item_id": "item1",
            "name": "Margherita Pizza",
            "price": 12.99,
            "description": "Classic tomato and mozzarella pizza",
            "category": "Pizza"
          },
          "quantity": 1
        }
      ],
      "subtotal": 0.0,
      "discount_pct": 0.9,
      "total": 0.0,
      "order_date": ""
    }


    created_order = client.create_order(new_order)
    print(f"Created item: {created_order}")

    # Update the order
    update_data = {
        "order_number": "new_order_num",
        "items": [
            {
                "item": {
                    "item_id": "item1",
                    "name": "Deluxe Margherita Pizza",
                    "price": 70.00,
                    "description": "Classic tomato and mozzarella pizza. Made with love, so double the price.",
                    "category": "Pizza"
                },
                "quantity": 1
            }
        ],
        "subtotal": 0.0,
        "discount_pct": 0.3,
        "total": 0.0,
        "order_date": ""
    }

    updated_order = client.update_order(created_order['order_id'], update_data)
    print(f"Updated item: {updated_order}")

    # updated_order = client.patch_order(created_order['order_id'], update_data)
    # print(f"Updated item: {updated_order}")

    # Delete the item
    client.delete_order(created_order['order_id'])
    print("Item deleted successfully")


if __name__ == "__main__":
    asyncio.run(test_menu_operations())
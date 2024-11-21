import asyncio
from client.restaurant_client import RestaurantClient


async def test_menu_operations():
    client = RestaurantClient("http://127.0.0.1:8000")

    # Get all items
    all_items = client.get_all_menu_items()
    print(f"All items: {all_items}")

    # Create a menu item
    new_item = {
        "name": "Margherita Pizza",
        "price": "12.99",
        "description": "Classic Italian pizza with tomato and mozzarella",
        "category": "Pizza"
    }

    created_item = client.create_menu_item(new_item)
    print(f"Created item: {created_item}")

    # Update the item
    updated_data = {
        "name": "Super Margherita Pizza",
        "price": "14.99"
    }
    updated_item = client.patch_menu_item(created_item['item_id'], updated_data)
    print(f"Updated item: {updated_item}")

    # Delete the item
    client.delete_menu_item(created_item['item_id'])
    print("Item deleted successfully")


if __name__ == "__main__":
    asyncio.run(test_menu_operations())
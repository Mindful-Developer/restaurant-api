import requests
from typing import Dict, List, Optional

class RestaurantClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        self.headers = {
            "Content-Type": "application/json",
            **({"X-API-Key": api_key} if api_key else {})
        }

    def get_all_menu_items(self) -> List[Dict]:
        """Get all menu items"""
        response = requests.get(f"{self.base_url}/menu/", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_menu_item(self, item_id: str) -> Dict:
        """Get a specific menu item"""
        response = requests.get(f"{self.base_url}/menu/{item_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_menu_item(self, item_data: Dict) -> Dict:
        """Create a new menu item"""
        response = requests.post(
            f"{self.base_url}/menu/",
            json=item_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def update_menu_item(self, item_id: str, item_data: Dict) -> Dict:
        """Update an entire menu item"""
        response = requests.put(
            f"{self.base_url}/menu/{item_id}",
            json=item_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def patch_menu_item(self, item_id: str, item_data: Dict) -> Dict:
        """Partially update a menu item"""
        response = requests.patch(
            f"{self.base_url}/menu/{item_id}",
            json=item_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def delete_menu_item(self, item_id: str) -> None:
        """Delete a menu item"""
        response = requests.delete(
            f"{self.base_url}/menu/{item_id}",
            headers=self.headers
        )
        response.raise_for_status()
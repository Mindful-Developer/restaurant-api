import requests
from typing import Dict, List, Optional

class OrderClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')  # Remove trailing slash if present
        self.headers = {
            "Content-Type": "application/json",
            **({"X-API-Key": api_key} if api_key else {})
        }

    def get_all_orders(self) -> List[Dict]:
        """Get all orders"""
        response = requests.get(f"{self.base_url}/orders/", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_order(self, order_id: str) -> Dict:
        """Get a specific order"""
        response = requests.get(f"{self.base_url}/orders/{order_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_order(self, order_data: Dict) -> Dict:
        """Create a new order"""
        response = requests.post(
            f"{self.base_url}/orders/",
            json=order_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def update_order(self, order_id: str, order_data: Dict) -> Dict:
        """Update an entire order"""
        response = requests.put(
            f"{self.base_url}/orders/{order_id}",
            json=order_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def patch_order(self, order_id: str, order_data: Dict) -> Dict:
        """Partially update a order"""
        response = requests.patch(
            f"{self.base_url}/orders/{order_id}",
            json=order_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def delete_order(self, order_id: str) -> None:
        """Delete a order"""
        response = requests.delete(
            f"{self.base_url}/orders/{order_id}",
            headers=self.headers
        )
        response.raise_for_status()
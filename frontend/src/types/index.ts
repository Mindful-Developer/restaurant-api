export interface MenuItem {
  item_id: string;
  name: string;
  price: string;
  description?: string;
  category: string;
  created_at: string;
}

export interface OrderItem {
  item: MenuItem;
  quantity: number;
}

export interface Order {
  order_id: string;
  order_number: string;
  items: OrderItem[];
  subtotal: string;
  total: string;
  discount_pct: string;
  order_date: string;
}
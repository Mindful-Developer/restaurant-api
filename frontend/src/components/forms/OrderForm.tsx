import React, { useState, useEffect } from 'react';
import { MenuItem, Order, OrderItem } from '../../types';
import { menuApi } from '../../services/api';
import { Plus, Minus, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';

const generateOrderNumber = () => {
  return Math.floor(100000 + Math.random() * 900000).toString();
};

interface OrderFormProps {
  initialData?: Order;
  onSubmit: (data: Partial<Order>) => void;
  onCancel: () => void;
}

export const OrderForm: React.FC<OrderFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
}) => {
  const [menuItems, setMenuItems] = useState<MenuItem[]>([]);
  const [selectedItems, setSelectedItems] = useState<OrderItem[]>(
    initialData?.items || []
  );
  const [loading, setLoading] = useState(true);
  const [discountPct, setDiscountPct] = useState(
    initialData ? Number(initialData.discount_pct) * 100 : 0
  );

  useEffect(() => {
    loadMenuItems();
  }, []);

  const loadMenuItems = async () => {
    try {
      const response = await menuApi.getAll();
      setMenuItems(response.data);
    } catch (error) {
      toast.error('Failed to load menu items');
    } finally {
      setLoading(false);
    }
  };

  const addItem = (menuItem: MenuItem) => {
    const existingItem = selectedItems.find(
      (item) => item.item.item_id === menuItem.item_id
    );

    if (existingItem) {
      setSelectedItems(
        selectedItems.map((item) =>
          item.item.item_id === menuItem.item_id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      );
    } else {
      setSelectedItems([...selectedItems, { item: menuItem, quantity: 1 }]);
    }
  };

  const updateQuantity = (itemId: string, delta: number) => {
    setSelectedItems(
      selectedItems
        .map((item) => {
          if (item.item.item_id === itemId) {
            const newQuantity = item.quantity + delta;
            return newQuantity > 0 ? { ...item, quantity: newQuantity } : null;
          }
          return item;
        })
        .filter((item): item is OrderItem => item !== null)
    );
  };

  const calculateTotals = () => {
    const subtotal = selectedItems.reduce(
      (sum, item) => sum + Number(item.item.price) * item.quantity,
      0
    );
    const discount = subtotal * (Number(discountPct) / 100);
    const total = subtotal - discount;
    return { subtotal, total };
  };

  const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault();
      const { subtotal, total } = calculateTotals();
      const discountDecimal = Math.min(Math.max(discountPct / 100, 0), 1);

      const orderData = {
          order_number: initialData?.order_number || generateOrderNumber(),
          items: selectedItems.map((item) => ({
              item: item.item,
              quantity: item.quantity,
          })),
          subtotal: subtotal.toFixed(2),
          total: total.toFixed(2),
          discount_pct: discountDecimal.toFixed(2), // Ensure 2 decimal places
          order_date: Math.floor(Date.now() / 1000).toString()
      };

      onSubmit(orderData);
  };

  if (loading) {
    return <div>Loading menu items...</div>;
  }

  const { subtotal, total } = calculateTotals();

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Add Items
        </label>
        <select
          onChange={(e) => {
            const item = menuItems.find((i) => i.item_id === e.target.value);
            if (item) addItem(item);
          }}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value=""
        >
          <option value="">Select an item</option>
          {menuItems.map((item) => (
            <option key={item.item_id} value={item.item_id}>
              {item.name} - ${Number(item.price).toFixed(2)}
            </option>
          ))}
        </select>
      </div>

      <div className="space-y-2">
        {selectedItems.map((item) => (
          <div
            key={item.item.item_id}
            className="flex items-center justify-between bg-gray-50 p-2 rounded"
          >
            <span>{item.item.name}</span>
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => updateQuantity(item.item.item_id, -1)}
                className="p-1 text-gray-500 hover:text-gray-700"
              >
                <Minus className="w-4 h-4" />
              </button>
              <span className="w-8 text-center">{item.quantity}</span>
              <button
                type="button"
                onClick={() => updateQuantity(item.item.item_id, 1)}
                className="p-1 text-gray-500 hover:text-gray-700"
              >
                <Plus className="w-4 h-4" />
              </button>
              <button
                type="button"
                onClick={() => updateQuantity(item.item.item_id, -item.quantity)}
                className="p-1 text-red-500 hover:text-red-700"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Discount (%)
        </label>
        <input
          type="number"
          min="0"
          max="100"
          value={discountPct}
          onChange={(e) => setDiscountPct(Number(e.target.value))}
          className="p-1 mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
        />
      </div>

      <div className="space-y-1">
        <p className="text-sm text-gray-600">
          Subtotal: ${subtotal.toFixed(2)}
        </p>
        <p className="text-sm text-gray-600">
          Discount: ${(subtotal * (Number(discountPct) / 100)).toFixed(2)}
        </p>
        <p className="text-lg font-semibold">Total: ${total.toFixed(2)}</p>
      </div>

      <div className="flex justify-end space-x-3 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
          disabled={selectedItems.length === 0}
        >
          {initialData ? 'Update' : 'Create'}
        </button>
      </div>
    </form>
  );
};
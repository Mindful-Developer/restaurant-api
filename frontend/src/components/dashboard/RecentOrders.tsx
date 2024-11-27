import React from 'react';
import { Order } from '../../types';
import { format } from 'date-fns';

interface RecentOrdersProps {
  orders: Order[];
}

export const RecentOrders: React.FC<RecentOrdersProps> = ({ orders }) => {
  return (
    <div className="space-y-4">
      {orders.map((order) => (
        <div
          key={order.order_number}
          className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
        >
          <div>
            <p className="font-medium">Order #{order.order_number}</p>
            <p className="text-sm text-gray-500">
              {format(new Date(Number(order.order_date) * 1000), 'MMM d, yyyy h:mm a')}
            </p>
            <p className="text-sm text-gray-500">{order.items.length} items</p>
          </div>
          <div className="text-right">
            <p className="font-medium">${Number(order.total).toFixed(2)}</p>
            {Number(order.discount_pct) > 0 && (
              <p className="text-sm text-green-600">
                {Number(order.discount_pct) * 100}% discount
              </p>
            )}
          </div>
        </div>
      ))}
      {orders.length === 0 && (
        <p className="text-gray-500 text-center py-4">No recent orders</p>
      )}
    </div>
  );
};
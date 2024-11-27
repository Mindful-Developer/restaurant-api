import React from 'react';
import { MenuItem } from '../../types';

interface PopularItemsProps {
  items: Array<{
    item: MenuItem;
    totalOrdered: number;
    revenue: number;
  }>;
}

export const PopularItems: React.FC<PopularItemsProps> = ({ items }) => {
  return (
    <div className="space-y-4">
      {items.map(({ item, totalOrdered, revenue }, i) => (
        <div
          key={i}
          className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
        >
          <div>
            <p className="font-medium">{item.name}</p>
            <p className="text-sm text-gray-500">{item.category}</p>
            <p className="text-sm text-gray-500">
              Ordered {totalOrdered} times
            </p>
          </div>
          <div className="text-right">
            <p className="font-medium">${revenue.toFixed(2)}</p>
            <p className="text-sm text-gray-500">
              ${Number(item.price).toFixed(2)} each
            </p>
          </div>
        </div>
      ))}
      {items.length === 0 && (
        <p className="text-gray-500 text-center py-4">No popular items yet</p>
      )}
    </div>
  );
};
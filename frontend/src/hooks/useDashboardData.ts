import { useState, useEffect } from 'react';
import { menuApi, orderApi } from '../services/api';
import { MenuItem, Order } from '../types';
import { subDays } from 'date-fns';

interface DashboardStats {
  totalRevenue: number;
  totalOrders: number;
  menuItemsCount: number;
  averageOrderAmount: number;
  recentOrders: Order[];
  popularItems: Array<{
    item: MenuItem;
    totalOrdered: number;
    revenue: number;
  }>;
  isLoading: boolean;
}

export const useDashboardData = (): DashboardStats => {
  const [stats, setStats] = useState<DashboardStats>({
    totalRevenue: 0,
    totalOrders: 0,
    menuItemsCount: 0,
    averageOrderAmount: 0,
    recentOrders: [],
    popularItems: [],
    isLoading: true,
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ordersResponse, menuResponse] = await Promise.all([
          orderApi.getAll(),
          menuApi.getAll(),
        ]);

        const orders = ordersResponse.data;
        const menuItems = menuResponse.data;

        // Calculate total revenue and average order amount
        const totalRevenue = orders.reduce((sum, order) => sum + Number(order.total), 0);
        const averageOrderAmount = orders.length > 0 ? Number(totalRevenue) / orders.length : 0;

        // Get recent orders (last 30 days)
        const thirtyDaysAgo = subDays(new Date(), 30);
        const recentOrders = orders
          .filter(order => new Date(Number(order.order_date) * 1000) >= thirtyDaysAgo)
          .sort((a, b) => new Date(Number(b.order_date) * 1000).getTime() - new Date(Number(a.order_date) * 1000).getTime())
          .slice(0, 5);

        // Calculate popular items
        const itemStats = new Map<string, { totalOrdered: number; revenue: number; item: MenuItem }>();
        
        orders.forEach(order => {
          order.items.forEach(orderItem => {
            const stats = itemStats.get(orderItem.item.item_id) || {
              totalOrdered: 0,
              revenue: 0,
              item: orderItem.item,
            };
            stats.totalOrdered += orderItem.quantity;
            stats.revenue += Number(orderItem.item.price) * orderItem.quantity;
            itemStats.set(orderItem.item.item_id, stats);
          });
        });

        const popularItems = Array.from(itemStats.values())
          .sort((a, b) => b.totalOrdered - a.totalOrdered)
          .slice(0, 5);

        setStats({
          totalRevenue,
          totalOrders: orders.length,
          menuItemsCount: menuItems.length,
          averageOrderAmount,
          recentOrders,
          popularItems,
          isLoading: false,
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setStats(prev => ({ ...prev, isLoading: false }));
      }
    };

    fetchData();
  }, []);

  return stats;
};
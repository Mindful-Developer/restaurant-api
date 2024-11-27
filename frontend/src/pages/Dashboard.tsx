import React from 'react';
import { DollarSign, ShoppingBag, Utensils, TrendingUp } from 'lucide-react';
import { useDashboardData } from '../hooks/useDashboardData';
import { RecentOrders } from '../components/dashboard/RecentOrders';
import { PopularItems } from '../components/dashboard/PopularItems';

interface StatCardProps {
  title: string;
  value: string;
  icon: React.ElementType;
  color: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon: Icon, color }) => (
  <div className="bg-white rounded-lg shadow p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-gray-500 text-sm">{title}</p>
        <h3 className="text-2xl font-bold mt-1">{value}</h3>
      </div>
      <div className={`p-3 rounded-full ${color}`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
    </div>
  </div>
);

const Dashboard = () => {
  const {
    totalRevenue,
    totalOrders,
    menuItemsCount,
    averageOrderAmount,
    recentOrders,
    popularItems,
    isLoading,
  } = useDashboardData();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p className="text-gray-500">Loading dashboard data...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Revenue"
          value={`$${Number(totalRevenue).toFixed(2)}`}
          icon={DollarSign}
          color="bg-green-500"
        />
        <StatCard
          title="Total Orders"
          value={totalOrders.toString()}
          icon={ShoppingBag}
          color="bg-blue-500"
        />
        <StatCard
          title="Menu Items"
          value={menuItemsCount.toString()}
          icon={Utensils}
          color="bg-purple-500"
        />
        <StatCard
          title="Avg. Order Amount"
          value={`$${averageOrderAmount.toFixed(2)}`}
          icon={TrendingUp}
          color="bg-yellow-500"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Recent Orders</h2>
          <RecentOrders orders={recentOrders} />
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Popular Items</h2>
          <PopularItems items={popularItems} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
import { useEffect, useState } from 'react';
import { orderApi } from '../services/api';
import { Order } from '../types';
import { Eye, Trash2, Plus } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';
import Modal from './ui/Modal';
import { OrderForm } from './forms/OrderForm';

const OrderList = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingOrder, setEditingOrder] = useState<Order | undefined>();

  useEffect(() => {
    loadOrders();
  }, []);

  const loadOrders = async () => {
    try {
      const response = await orderApi.getAll();
      setOrders(response.data);
    } catch (error) {
      toast.error('Failed to load orders');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this order?')) {
      try {
        await orderApi.delete(id);
        toast.success('Order deleted successfully');
        loadOrders();
      } catch (error) {
        toast.error('Failed to delete order');
      }
    }
  };

  const handleSubmit = async (data: Partial<Order>) => {
      try {
          if (editingOrder) {
              await orderApi.update(editingOrder.order_id, data);
              toast.success('Order updated successfully');
          } else {
              await orderApi.create(data);
              toast.success('Order created successfully');
          }
          setIsModalOpen(false);
          setEditingOrder(undefined);
          await loadOrders();
      } catch (error) {
          toast.error(editingOrder ? 'Failed to update order' : 'Failed to create order');
          console.error('Error:', error);
      }
  };

  const handleView = (order: Order) => {
    setEditingOrder(order);
    setIsModalOpen(true);
  };

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading...</div>;
  }

  return (
    <>
      <div className="bg-white rounded-lg shadow">
        <div className="p-4 border-b border-gray-200 flex justify-between items-center">
          <h2 className="text-xl font-semibold">Orders</h2>
          <button
            onClick={() => {
              setEditingOrder(undefined);
              setIsModalOpen(true);
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
          >
            <Plus className="w-4 h-4" />
            New Order
          </button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Order #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Items</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {orders.map((order) => (
                <tr key={order.order_number} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap font-medium">{order.order_number}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {format(new Date(Number(order.order_date) * 1000), 'MMM d, yyyy h:mm a')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">{order.items.length} items</td>
                  <td className="px-6 py-4 whitespace-nowrap">${Number(order.total).toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleView(order)}
                      className="text-blue-600 hover:text-blue-900 mr-4"
                    >
                      <Eye className="w-5 h-5" />
                    </button>
                    <button 
                      className="text-red-600 hover:text-red-900"
                      onClick={() => handleDelete(order.order_number)}
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          setEditingOrder(undefined);
        }}
        title={editingOrder ? 'View/Edit Order' : 'New Order'}
      >
        <OrderForm
          initialData={editingOrder}
          onSubmit={handleSubmit}
          onCancel={() => {
            setIsModalOpen(false);
            setEditingOrder(undefined);
          }}
        />
      </Modal>
    </>
  );
};

export default OrderList;
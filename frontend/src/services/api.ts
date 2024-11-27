import axios from 'axios';
import {MenuItem, Order} from '../types';

const API_URL = 'http://localhost:8000';

// Menu API
export const menuApi = {
  getAll: () => axios.get<MenuItem[]>(`${API_URL}/menu/`),
  getOne: (id: string) => axios.get<MenuItem>(`${API_URL}/menu/${id}/`),
  create: (item: Partial<MenuItem>) =>
    axios.post<MenuItem>(`${API_URL}/menu/`, item),
  update: (id: string, item: Partial<MenuItem>) => 
    axios.put<MenuItem>(`${API_URL}/menu/${id}/`, item),
  patch: (id: string, item: Partial<MenuItem>) => 
    axios.patch<MenuItem>(`${API_URL}/menu/${id}/`, item),
  delete: (id: string) => axios.delete(`${API_URL}/menu/${id}/`)
};

// Orders API
export const orderApi = {
  getAll: () => axios.get<Order[]>(`${API_URL}/orders/`),
  getOne: (id: string) => axios.get<Order>(`${API_URL}/orders/${id}/`),
  create: (order: Partial<Order>) =>
    axios.post<Order>(`${API_URL}/orders/`, order),
  update: (id: string, order: Partial<Order>) =>
    axios.put<Order>(`${API_URL}/orders/${id}/`, order),
  patch: (id: string, order: Partial<Order>) => 
    axios.patch<Order>(`${API_URL}/orders/${id}/`, order),
  delete: (id: string) => axios.delete(`${API_URL}/orders/${id}/`)
};
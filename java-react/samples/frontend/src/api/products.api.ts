import { apiClient } from './client';
import type { Product, ProductPage } from '@/types/product';

interface ProductFilters {
  category?: string;
  page?: number;
  size?: number;
}

export const getProducts = (filters: ProductFilters = {}): Promise<ProductPage> =>
  apiClient.get('/products', { params: filters }).then(r => r.data);

export const getProduct = (uid: string): Promise<Product> =>
  apiClient.get(`/products/${uid}`).then(r => r.data);

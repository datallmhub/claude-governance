import { useQuery } from '@tanstack/react-query';
import { getProducts, getProduct } from '@/api/products.api';
import type { ApiError } from '@/types/api';
import type { ProductPage, Product } from '@/types/product';

export function useProducts(category?: string, page = 0) {
  return useQuery<ProductPage, ApiError>({
    queryKey: ['products', { category, page }],
    queryFn: () => getProducts({ category, page, size: 20 }),
  });
}

export function useProduct(uid: string) {
  return useQuery<Product, ApiError>({
    queryKey: ['products', uid],
    queryFn: () => getProduct(uid),
    enabled: !!uid,
  });
}

import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useProducts } from '@/hooks/useProducts';
import { useCartStore } from '@/store/cartStore';
import { ProductCard } from '@/components/ProductCard';
import { Spinner } from '@/components/ui/spinner';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';

const CATEGORIES = ['All', 'Electronics', 'Clothing', 'Books', 'Home'];

export function ProductListPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [page, setPage] = useState(0);
  const category = searchParams.get('category') ?? undefined;

  const { data, isLoading, isError } = useProducts(category, page);
  const addToCart = useCartStore(s => s.addItem);

  if (isLoading) return <Spinner />;
  if (isError) return (
    <Alert variant="destructive">
      <AlertDescription>Failed to load products. Please try again.</AlertDescription>
    </Alert>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex gap-2 mb-6">
        {CATEGORIES.map(cat => (
          <Button
            key={cat}
            variant={category === cat || (cat === 'All' && !category) ? 'default' : 'outline'}
            size="sm"
            onClick={() => {
              setPage(0);
              setSearchParams(cat === 'All' ? {} : { category: cat });
            }}
          >
            {cat}
          </Button>
        ))}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {data?.content.map(product => (
          <ProductCard
            key={product.uid}
            product={product}
            onAddToCart={addToCart}
          />
        ))}
      </div>

      {data && data.totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-8">
          <Button variant="outline" disabled={page === 0} onClick={() => setPage(p => p - 1)}>
            Previous
          </Button>
          <span className="self-center text-sm text-muted-foreground">
            Page {page + 1} of {data.totalPages}
          </span>
          <Button variant="outline" disabled={page >= data.totalPages - 1} onClick={() => setPage(p => p + 1)}>
            Next
          </Button>
        </div>
      )}
    </div>
  );
}

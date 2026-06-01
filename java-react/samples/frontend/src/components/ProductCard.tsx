import { Link } from 'react-router-dom';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import type { Product } from '@/types/product';

interface Props {
  product: Product;
  onAddToCart: (uid: string) => void;
}

export function ProductCard({ product, onAddToCart }: Props) {
  return (
    <Card className="flex flex-col">
      <CardContent className="flex-1 p-4">
        {product.imageUrl && (
          <img
            src={product.imageUrl}
            alt={product.name}
            className="w-full h-48 object-cover rounded-md mb-3"
          />
        )}
        <Badge variant="secondary" className="mb-2">{product.category}</Badge>
        <Link to={`/products/${product.uid}`} className="block font-semibold hover:underline">
          {product.name}
        </Link>
        <p className="text-sm text-muted-foreground mt-1 line-clamp-2">{product.description}</p>
        <p className="text-lg font-bold mt-2">${product.price.toFixed(2)}</p>
      </CardContent>
      <CardFooter className="p-4 pt-0">
        <Button
          className="w-full"
          disabled={!product.inStock}
          onClick={() => onAddToCart(product.uid)}
          aria-label={`Add ${product.name} to cart`}
        >
          {product.inStock ? 'Add to cart' : 'Out of stock'}
        </Button>
      </CardFooter>
    </Card>
  );
}

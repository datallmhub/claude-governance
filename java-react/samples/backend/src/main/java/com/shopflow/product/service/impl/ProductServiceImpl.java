package com.shopflow.product.service.impl;

import com.shopflow.exception.ProductNotFoundException;
import com.shopflow.product.domain.ProductEntity;
import com.shopflow.product.dto.CreateProductRequest;
import com.shopflow.product.dto.ProductResponse;
import com.shopflow.product.repository.ProductRepository;
import com.shopflow.product.service.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.StringUtils;

import java.util.UUID;

@Service
@Transactional
@RequiredArgsConstructor
public class ProductServiceImpl implements ProductService {

    private final ProductRepository productRepository;

    @Override
    @Transactional(readOnly = true)
    public Page<ProductResponse> findAll(String category, Pageable pageable) {
        Page<ProductEntity> page = StringUtils.hasText(category)
            ? productRepository.findByCategoryAndActiveTrue(category, pageable)
            : productRepository.findByActiveTrue(pageable);
        return page.map(this::toResponse);
    }

    @Override
    @Transactional(readOnly = true)
    public ProductResponse findByPublicId(UUID publicId) {
        return productRepository.findByPublicIdAndActiveTrue(publicId)
            .map(this::toResponse)
            .orElseThrow(() -> new ProductNotFoundException(publicId));
    }

    @Override
    public ProductResponse create(CreateProductRequest request) {
        ProductEntity entity = new ProductEntity();
        entity.setName(request.name());
        entity.setDescription(request.description());
        entity.setPrice(request.price());
        entity.setStock(request.stock());
        entity.setCategory(request.category());
        entity.setImageUrl(request.imageUrl());
        return toResponse(productRepository.save(entity));
    }

    @Override
    public void deactivate(UUID publicId) {
        ProductEntity entity = productRepository.findByPublicIdAndActiveTrue(publicId)
            .orElseThrow(() -> new ProductNotFoundException(publicId));
        entity.setActive(false);
    }

    private ProductResponse toResponse(ProductEntity e) {
        return new ProductResponse(
            e.getPublicId(),
            e.getName(),
            e.getDescription(),
            e.getPrice(),
            e.getStock(),
            e.getCategory(),
            e.getImageUrl(),
            e.getStock() > 0
        );
    }
}

package com.shopflow.product.service;

import com.shopflow.product.dto.CreateProductRequest;
import com.shopflow.product.dto.ProductResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.UUID;

public interface ProductService {

    Page<ProductResponse> findAll(String category, Pageable pageable);

    ProductResponse findByPublicId(UUID publicId);

    ProductResponse create(CreateProductRequest request);

    void deactivate(UUID publicId);
}

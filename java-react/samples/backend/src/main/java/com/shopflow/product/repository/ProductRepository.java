package com.shopflow.product.repository;

import com.shopflow.product.domain.ProductEntity;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface ProductRepository extends JpaRepository<ProductEntity, Long> {

    Optional<ProductEntity> findByPublicIdAndActiveTrue(UUID publicId);

    Page<ProductEntity> findByCategoryAndActiveTrue(String category, Pageable pageable);

    Page<ProductEntity> findByActiveTrue(Pageable pageable);
}

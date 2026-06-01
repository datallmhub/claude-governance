package com.shopflow.product.dto;

import java.math.BigDecimal;
import java.util.UUID;

public record ProductResponse(
    UUID uid,
    String name,
    String description,
    BigDecimal price,
    int stock,
    String category,
    String imageUrl,
    boolean inStock
) {}

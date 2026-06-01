package com.shopflow.product.dto;

import jakarta.validation.constraints.*;
import java.math.BigDecimal;

public record CreateProductRequest(
    @NotBlank @Size(max = 255)
    String name,

    String description,

    @NotNull @DecimalMin("0.01")
    BigDecimal price,

    @Min(0)
    int stock,

    @NotBlank @Size(max = 100)
    String category,

    @Size(max = 500)
    String imageUrl
) {}

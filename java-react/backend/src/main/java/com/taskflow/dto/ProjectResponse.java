package com.taskflow.dto;

import java.util.UUID;

public record ProjectResponse(
        UUID publicId,
        String name,
        String description
) {}

package com.taskflow.dto;

import com.taskflow.domain.Priority;

import java.time.LocalDate;
import java.util.UUID;

public record TaskResponse(
        UUID publicId,
        String title,
        String status,
        LocalDate dueDate,
        Priority priority
) {}

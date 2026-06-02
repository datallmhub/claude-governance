package com.taskflow.exception;

import java.util.UUID;

public class TaskNotFoundException extends TaskFlowException {

    public TaskNotFoundException(UUID publicId) {
        super("Task not found: " + publicId);
    }
}

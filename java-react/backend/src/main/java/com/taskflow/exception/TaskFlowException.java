package com.taskflow.exception;

public class TaskFlowException extends RuntimeException {

    public TaskFlowException(String message) {
        super(message);
    }

    public TaskFlowException(String message, Throwable cause) {
        super(message, cause);
    }
}

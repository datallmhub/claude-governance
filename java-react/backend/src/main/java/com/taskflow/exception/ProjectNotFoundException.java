package com.taskflow.exception;

import java.util.UUID;

public class ProjectNotFoundException extends TaskFlowException {

    public ProjectNotFoundException(UUID publicId) {
        super("Project not found: " + publicId);
    }
}

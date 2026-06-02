package com.taskflow.service;

import com.taskflow.domain.Task;
import com.taskflow.dto.TaskResponse;
import com.taskflow.exception.ProjectNotFoundException;
import com.taskflow.exception.TaskNotFoundException;
import com.taskflow.repository.ProjectRepository;
import com.taskflow.repository.TaskRepository;
import com.taskflow.security.TenantContext;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class TaskService {

    private final TaskRepository taskRepository;
    private final ProjectRepository projectRepository;

    @Transactional(readOnly = true)
    public TaskResponse getByPublicId(UUID publicId) {
        Task task = taskRepository.findByPublicId(publicId)
                .orElseThrow(() -> new TaskNotFoundException(publicId));
        return new TaskResponse(task.getPublicId(), task.getTitle(), task.getStatus(), task.getDueDate(), task.getPriority());
    }

    @Transactional(readOnly = true)
    public Page<TaskResponse> getTasksByProject(UUID projectPublicId, Pageable pageable) {
        // @Filter on TenantAwareEntity ensures findByPublicId only returns a project
        // belonging to the current organization — a cross-tenant publicId yields empty.
        projectRepository.findByPublicId(projectPublicId)
                .orElseThrow(() -> new ProjectNotFoundException(projectPublicId));
        return taskRepository.findByProject_PublicId(projectPublicId, pageable)
                .map(t -> new TaskResponse(t.getPublicId(), t.getTitle(), t.getStatus(), t.getDueDate(), t.getPriority()));
    }

    @Transactional
    public void delete(UUID publicId) {
        Long organizationId = TenantContext.getRequiredOrganizationId();
        Task task = taskRepository.findByPublicIdAndOrganizationId(publicId, organizationId)
                .orElseThrow(() -> new TaskNotFoundException(publicId));
        taskRepository.delete(task);
    }
}

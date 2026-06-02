package com.taskflow.service;

import com.taskflow.domain.Project;
import com.taskflow.dto.CreateProjectRequest;
import com.taskflow.dto.ProjectResponse;
import com.taskflow.repository.ProjectRepository;
import com.taskflow.security.TenantContext;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
public class ProjectService {

    private final ProjectRepository projectRepository;

    @Transactional
    public ProjectResponse create(CreateProjectRequest request) {
        Long organizationId = TenantContext.getRequiredOrganizationId();

        Project project = Project.builder()
                .name(request.name())
                .description(request.description())
                .organizationId(organizationId)
                .build();

        Project saved = projectRepository.save(project);

        return new ProjectResponse(
                saved.getPublicId(),
                saved.getName(),
                saved.getDescription()
        );
    }
}

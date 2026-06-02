package com.taskflow.controller;

import com.taskflow.dto.CreateProjectRequest;
import com.taskflow.dto.ProjectResponse;
import com.taskflow.service.ProjectService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/projects")
@RequiredArgsConstructor
public class ProjectController {

    private final ProjectService projectService;

    @PostMapping
    public ResponseEntity<ProjectResponse> create(@Valid @RequestBody CreateProjectRequest request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(projectService.create(request));
    }
}

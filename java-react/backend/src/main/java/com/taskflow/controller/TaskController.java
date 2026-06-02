package com.taskflow.controller;

import com.taskflow.dto.TaskResponse;
import com.taskflow.service.TaskService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/tasks")
@RequiredArgsConstructor
public class TaskController {

    private final TaskService taskService;

    @GetMapping("/{publicId}")
    public ResponseEntity<TaskResponse> getByPublicId(@PathVariable UUID publicId) {
        return ResponseEntity.ok(taskService.getByPublicId(publicId));
    }

    @DeleteMapping("/{publicId}")
    public ResponseEntity<Void> delete(@PathVariable UUID publicId) {
        taskService.delete(publicId);
        return ResponseEntity.noContent().build();
    }
}

package com.taskflow.repository;

import com.taskflow.domain.Project;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface ProjectRepository extends JpaRepository<Project, Long> {

    // Hibernate @Filter on TenantAwareEntity automatically appends
    // "AND organization_id = :organizationId" — no manual parameter needed.
    Optional<Project> findByPublicId(UUID publicId);
}

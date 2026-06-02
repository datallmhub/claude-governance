package com.taskflow.repository;

import com.taskflow.domain.Task;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {

    // Hibernate @Filter on TenantAwareEntity automatically appends
    // "AND organization_id = :organizationId" to every query in this repository.
    Optional<Task> findByPublicId(UUID publicId);

    Optional<Task> findByPublicIdAndOrganizationId(UUID publicId, Long organizationId);

    Page<Task> findByProject_PublicId(UUID projectPublicId, Pageable pageable);

    @Query("SELECT t FROM Task t WHERE LOWER(t.title) LIKE LOWER(CONCAT('%', :keyword, '%')) AND t.status = :status")
    Page<Task> searchByTitleKeywordAndStatus(@Param("keyword") String keyword,
                                             @Param("status") String status,
                                             Pageable pageable);
}

package com.taskflow.security;

import com.taskflow.domain.Project;
import com.taskflow.domain.Task;
import com.taskflow.domain.TenantAwareEntity;
import com.taskflow.repository.ProjectRepository;
import com.taskflow.repository.TaskRepository;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.hibernate.Session;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Verifies that the Hibernate tenant filter enforces organization isolation:
 * a record inserted for org A must not be visible when the filter is bound to org B.
 *
 * Uses @DataJpaTest (H2 in-memory) so no Docker/Testcontainers is needed here.
 * Full Testcontainers coverage lives in the integration profile (mvn verify -Pintegration).
 */
@DataJpaTest
@ActiveProfiles("test")
@Transactional
class TenantFilterIsolationTest {

    private static final Long ORG_A = 1L;
    private static final Long ORG_B = 2L;

    @Autowired
    private TaskRepository taskRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @PersistenceContext
    private EntityManager entityManager;

    private Task taskForOrgA;
    private Project projectForOrgA;

    @BeforeEach
    void setUp() {
        // Insert directly without filter to seed cross-tenant data
        TenantContext.setOrganizationId(ORG_A);

        projectForOrgA = new Project();
        projectForOrgA.setOrganizationId(ORG_A);
        projectForOrgA.setName("Org A project");
        projectRepository.saveAndFlush(projectForOrgA);

        taskForOrgA = new Task();
        taskForOrgA.setOrganizationId(ORG_A);
        taskForOrgA.setTitle("Org A task");
        taskForOrgA.setStatus("OPEN");
        taskRepository.saveAndFlush(taskForOrgA);

        TenantContext.clear();
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    void taskIsVisibleWhenFilterBoundToSameOrg() {
        enableFilter(ORG_A);

        Optional<Task> result = taskRepository.findByPublicId(taskForOrgA.getPublicId());

        assertThat(result).isPresent();
    }

    @Test
    void taskIsHiddenWhenFilterBoundToDifferentOrg() {
        enableFilter(ORG_B);

        Optional<Task> result = taskRepository.findByPublicId(taskForOrgA.getPublicId());

        assertThat(result).isEmpty();
    }

    @Test
    void findAllReturnsOnlyCurrentTenantRecords() {
        // Seed a second task for org B
        Task taskForOrgB = new Task();
        taskForOrgB.setOrganizationId(ORG_B);
        taskForOrgB.setTitle("Org B task");
        taskForOrgB.setStatus("OPEN");
        taskRepository.saveAndFlush(taskForOrgB);

        enableFilter(ORG_A);

        assertThat(taskRepository.findAll())
                .allMatch(t -> ORG_A.equals(t.getOrganizationId()))
                .hasSize(1);
    }

    @Test
    void projectIsHiddenWhenFilterBoundToDifferentOrg() {
        // Verifies that ProjectRepository.findByPublicId() — which no longer takes an
        // explicit organizationId — is still protected by the @Filter alone.
        enableFilter(ORG_B);

        Optional<Project> result = projectRepository.findByPublicId(projectForOrgA.getPublicId());

        assertThat(result).isEmpty();
    }

    @Test
    void projectIsVisibleWhenFilterBoundToSameOrg() {
        enableFilter(ORG_A);

        Optional<Project> result = projectRepository.findByPublicId(projectForOrgA.getPublicId());

        assertThat(result).isPresent();
    }

    private void enableFilter(Long organizationId) {
        entityManager.unwrap(Session.class)
                .enableFilter(TenantAwareEntity.TENANT_FILTER_NAME)
                .setParameter("organizationId", organizationId);
    }
}

package com.taskflow.config;

import com.taskflow.domain.TenantAwareEntity;
import com.taskflow.security.TenantContext;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.hibernate.Session;
import org.springframework.stereotype.Component;

/**
 * Activates the Hibernate tenant filter on the current transactional session
 * before any service method executes. Targeting the service layer (rather than
 * repositories) guarantees the @Transactional session is already open when
 * EntityManager.unwrap(Session.class) is called.
 *
 * @PersistenceContext is required — constructor injection via @RequiredArgsConstructor
 * would inject the shared proxy, which cannot be unwrapped to a Session outside a
 * transaction. The @PersistenceContext proxy delegates to the active transaction's
 * Session at the point of the call.
 */
@Aspect
@Component
public class TenantFilterAspect {

    @PersistenceContext
    private EntityManager entityManager;

    @Around("execution(* com.taskflow.service.*Service.*(..))")
    public Object enableTenantFilter(ProceedingJoinPoint joinPoint) throws Throwable {
        Long organizationId = TenantContext.getOrganizationId();
        if (organizationId != null) {
            Session session = entityManager.unwrap(Session.class);
            session.enableFilter(TenantAwareEntity.TENANT_FILTER_NAME)
                   .setParameter("organizationId", organizationId);
        }
        return joinPoint.proceed();
    }
}

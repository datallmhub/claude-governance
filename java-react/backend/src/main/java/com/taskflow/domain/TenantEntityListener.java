package com.taskflow.domain;

import com.taskflow.security.TenantContext;
import jakarta.persistence.PrePersist;

public class TenantEntityListener {

    @PrePersist
    public void setOrganizationId(TenantAwareEntity entity) {
        if (entity.getOrganizationId() == null) {
            entity.setOrganizationId(TenantContext.getRequiredOrganizationId());
        }
    }
}

package com.taskflow.security;

public final class TenantContext {

    private static final ThreadLocal<Long> CURRENT_ORGANIZATION_ID = new ThreadLocal<>();

    private TenantContext() {
    }

    public static void setOrganizationId(Long organizationId) {
        CURRENT_ORGANIZATION_ID.set(organizationId);
    }

    public static Long getOrganizationId() {
        return CURRENT_ORGANIZATION_ID.get();
    }

    public static Long getRequiredOrganizationId() {
        Long orgId = CURRENT_ORGANIZATION_ID.get();
        if (orgId == null) {
            throw new IllegalStateException("No organization ID set in TenantContext");
        }
        return orgId;
    }

    public static void clear() {
        CURRENT_ORGANIZATION_ID.remove();
    }
}

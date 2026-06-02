package com.taskflow.domain;

import jakarta.persistence.Column;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.MappedSuperclass;
import jakarta.persistence.PrePersist;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.SuperBuilder;
import org.hibernate.annotations.Filter;
import org.hibernate.annotations.FilterDef;
import org.hibernate.annotations.ParamDef;

import java.util.UUID;

@MappedSuperclass
@FilterDef(
    name = TenantAwareEntity.TENANT_FILTER_NAME,
    parameters = @ParamDef(name = "organizationId", type = Long.class),
    defaultCondition = "organization_id = :organizationId"
)
@Filter(name = TenantAwareEntity.TENANT_FILTER_NAME)
@EntityListeners(TenantEntityListener.class)
@Getter
@Setter
@NoArgsConstructor
@SuperBuilder
public abstract class TenantAwareEntity {

    public static final String TENANT_FILTER_NAME = "tenantFilter";

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "public_id", nullable = false, unique = true, updatable = false)
    private UUID publicId;

    @Column(name = "organization_id", nullable = false)
    private Long organizationId;

    @PrePersist
    protected void onCreate() {
        if (publicId == null) {
            publicId = UUID.randomUUID();
        }
    }
}

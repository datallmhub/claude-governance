package com.taskflow.security;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;

public record AuthenticatedUser(
        Long id,
        String email,
        Long organizationId,
        Collection<? extends GrantedAuthority> authorities
) implements UserDetails {

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return authorities != null ? authorities : List.of();
    }

    @Override
    public String getPassword() {
        return null;
    }

    @Override
    public String getUsername() {
        return email;
    }

    public Long getOrganizationId() {
        return organizationId;
    }
}

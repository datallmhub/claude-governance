package com.taskflow.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

/**
 * Populates TenantContext from the authenticated principal so the Hibernate
 * @Filter can scope all queries to the current organization without manual
 * organizationId threading through service/repository signatures.
 *
 * Must run after the JWT authentication filter that populates SecurityContext.
 */
@Component
public class TenantContextFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        try {
            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
            if (authentication != null && authentication.getPrincipal() instanceof AuthenticatedUser user) {
                TenantContext.setOrganizationId(user.organizationId());
            }
            filterChain.doFilter(request, response);
        } finally {
            // Always clear to prevent thread-local leaks in thread-pool environments
            TenantContext.clear();
        }
    }
}

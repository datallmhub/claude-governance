package com.taskflow.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.time.Duration;
import java.util.Date;
import java.util.List;

@Service
public class JwtService {

    private static final String ISSUER   = "taskflow-api";
    private static final String AUDIENCE = "taskflow-web";

    private final Key signingKey;
    private final Duration accessTokenTtl;

    public JwtService(
            @Value("${security.jwt.secret}") String secret,
            @Value("${security.jwt.access-token-ttl:PT15M}") Duration accessTokenTtl) {

        byte[] keyBytes = secret.getBytes(StandardCharsets.UTF_8);
        if (keyBytes.length < 32) {
            throw new IllegalArgumentException("JWT secret must be at least 256 bits (32 bytes)");
        }
        this.signingKey    = Keys.hmacShaKeyFor(keyBytes);
        this.accessTokenTtl = accessTokenTtl;
    }

    public String generateToken(Long userId, Long organizationId, List<String> roles) {
        Date now    = new Date();
        Date expiry = new Date(now.getTime() + accessTokenTtl.toMillis());

        return Jwts.builder()
                .setSubject(String.valueOf(userId))
                .setIssuer(ISSUER)
                .setAudience(AUDIENCE)
                .setIssuedAt(now)
                .setExpiration(expiry)
                .claim("orgId", organizationId)
                .claim("roles", roles)
                .signWith(signingKey, SignatureAlgorithm.HS256)
                .compact();
    }

    /**
     * Validates signature, expiry, issuer and audience, then returns the claims.
     *
     * @throws JwtException if the token is invalid or expired
     */
    public Claims validateAndExtract(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(signingKey)
                .requireIssuer(ISSUER)
                .requireAudience(AUDIENCE)
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    public Long extractUserId(Claims claims) {
        return Long.valueOf(claims.getSubject());
    }

    public Long extractOrganizationId(Claims claims) {
        return claims.get("orgId", Long.class);
    }

    @SuppressWarnings("unchecked")
    public List<String> extractRoles(Claims claims) {
        return claims.get("roles", List.class);
    }
}

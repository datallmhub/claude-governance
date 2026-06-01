# Architecture — Next.js Full-Stack Overview

## System Diagram

```
┌──────────────────────────────────────────────────────┐
│                    BROWSER                            │
│         React Client Components (selective)          │
│         TanStack Query (client state cache)          │
│         Zustand (UI state)                           │
└─────────────────────────┬────────────────────────────┘
                          │ HTTP / RSC Payload
┌─────────────────────────▼────────────────────────────┐
│                 NEXT.JS SERVER                        │
│                                                      │
│  ┌──────────────┐   ┌─────────────────────────────┐  │
│  │ App Router   │   │       Server Actions         │  │
│  │ (RSC pages)  │   │ (mutations, form handling)   │  │
│  └──────┬───────┘   └──────────────┬──────────────┘  │
│         │                          │                 │
│  ┌──────▼──────────────────────────▼──────────────┐  │
│  │              Prisma ORM                        │  │
│  └────────────────────┬───────────────────────────┘  │
│                       │                              │
│  ┌────────────────────▼───────────────────────────┐  │
│  │          PostgreSQL (Vercel / Neon)             │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  API Routes: webhooks, OAuth callbacks only    │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

## Key Decisions

### 1. Server Components by default
All components are Server Components unless explicitly marked `'use client'`.
**Impact**: less JavaScript shipped to the browser, data fetching co-located with rendering.

### 2. Server Actions for all mutations
Form submissions and data mutations use Server Actions, not API routes.
**Impact**: built-in CSRF protection, progressive enhancement, type-safe end-to-end.

### 3. API Routes only for external integrations
API routes (`app/api/`) are reserved for webhooks (Stripe, GitHub), OAuth callbacks, and third-party integrations.
**Impact**: no internal RPC over HTTP — Server Actions handle all internal mutations.

### 4. Prisma with internal/public ID separation
Every model has an internal `id` (auto-increment) and a `publicId` (UUID). Only `publicId` appears in URLs and responses.
**Impact**: no IDOR vulnerability, no enumeration attacks on sequential IDs.

## Authentication Flow (NextAuth v5)

```
Browser                Next.js Server           DB
  │── POST /auth/signin ──►│                     │
  │                        │── verify credentials►│
  │◄── Set-Cookie session ─│◄── user record ──────│
  │                        │                     │
  │── Page request ────────►│                     │
  │                        │── auth() ───────────►│ (session lookup)
  │◄── RSC payload ─────────│◄── session ──────────│
```

# Multi-Tenancy

A multi-tenant system serves many customers from shared infrastructure. The design question is how much to share, how to keep tenants from seeing or starving each other, and how to bill and scale per tenant.

---

## 13.1 Learning Outcomes

After reading this chapter, you'll be able to:

1. Choose between shared, pooled and dedicated tenancy models.
2. Isolate tenants at the data layer (row-level security, schemas, databases) and at the request layer.
3. Contain noisy neighbours with quotas, rate limits and per-tenant limits.
4. Test for cross-tenant leaks.

---

## 13.2 Multi-Tenancy

Tenant isolation models (pool, bridge, silo), data isolation, and tenant-aware routing/security.

**In one sentence:** a multi-tenant SaaS serves many customer organizations (tenants) from one system, and the core design choice is how much they share — everything (pool), a shared app with separate databases or schemas (bridge), or fully separate stacks (silo) — traded off against cost, isolation, and operational effort.

**Mental model — housing.** Pool is a hostel: one big room, cheapest, and everyone relies on the staff to keep belongings apart. Bridge is an apartment building: shared walls and elevators, but each unit has its own lock. Silo is a street of detached houses: expensive, but nobody's plumbing problem floods the neighbors.

**The three models**

| | Pool (shared everything) | Bridge (shared app, separate schema or DB) | Silo (dedicated stack) |
|-|-------------------------|-------------------------------------------|------------------------|
| Data | one DB, a `tenant_id` column on every row | schema-per-tenant or DB-per-tenant | separate DB, app, and often account/VPC |
| Isolation | logical (code + RLS) | stronger (separate objects) | strongest (physical) |
| Cost per tenant | lowest | medium | highest |
| Number of tenants | 100,000s | 100s–1,000s (schema) / 100s (DB) | tens to hundreds |
| Noisy neighbors | a real risk | reduced (DB-level) | none |
| Per-tenant backup / restore / delete | hard (row-level) | easy | easy |
| Migrations | one run | N runs (automate!) | N stacks to upgrade |
| Customization | little | some | a lot (versions, regions, keys) |
| Typical tier | free / self-serve | business | enterprise, regulated, "bring your own key" |

Real SaaS usually mixes them: pool for the long tail, silo for the biggest or most regulated tenants (a *tiered* model).

**Preventing tenant data leaks — defense in depth**

| Layer | Control |
|-------|---------|
| Identity | every request carries an authenticated tenant ID (from the token, never from a URL parameter alone) |
| Application | a tenant context set once per request; repository methods *require* the tenant; no "unscoped" queries |
| Database | **Row-Level Security (RLS)** policies filter by `current_setting('app.tenant_id')`; unique constraints include `tenant_id` |
| Caches, queues, search | the tenant ID is part of every cache key, message, index filter, and object-storage prefix |
| Keys | per-tenant encryption keys (envelope encryption) for silo/bridge tiers |
| Testing | automated **cross-tenant tests**: tenant A's token must never read tenant B's IDs, across every endpoint |
| Observability | the tenant ID in logs, metrics, and traces (and per-tenant usage metering) |

**Noisy neighbors** — per-tenant rate limits and quotas (Ch 8), fair queuing for background jobs, statement timeouts, moving heavy tenants to their own shard or silo, and metering usage so it can also be billed.

**Tenant-aware routing** — resolve the tenant from the subdomain (`acme.app.com`), a header, or the token, then look up its placement (`tenant → shard / region / stack`) in a small, cached **tenant catalog**, and route there.

---

## 13.3 Key Takeaways

- Isolation is a spectrum; cost falls and risk rises as sharing increases.
- Put the tenant id on every request, row and cache key, and enforce it below the application code.
- Plan for noisy neighbours before the first large customer arrives.

## 13.4 Sample Interview Questions

- Compare row-level security with a database per tenant.
- How do you stop one tenant exhausting a shared connection pool?
- How would you migrate a tenant between shards?
- What is a tenant catalog and why keep one?

## 13.5 Further Reading

- Microsoft Azure Architecture Center, *Multitenant solution architecture*
- AWS SaaS Lens, Well-Architected Framework

---

**Next Up:** [Chapter 14 — Cloud Architecture & Cost →](./14%20-%20Cloud%20Architecture%20%26%20Cost.md)

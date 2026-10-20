# Chapter 35 — Library Ch 13 — Multi-Tenancy

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 34 — Library Ch 12 — Cloud Design Patterns](ch34-library-12-cloud-design-patterns.md) · Next → [Chapter 36 — Library Ch 14 — Cloud Architecture & Cost](ch36-library-14-cloud-architecture-cost.md)

---

## Concept

Isolation models, tenant-aware routing, noisy neighbours and cross-tenant safety for SaaS.

**In one sentence:** A multi-tenant system serves many customers from shared infrastructure.

A multi-tenant system serves many customers from shared infrastructure. The design question is how much to share, how to keep tenants from seeing or starving each other, and how to bill and scale per tenant.

---

### Learning Outcomes

After reading this chapter, you'll be able to:

1. Choose between shared, pooled and dedicated tenancy models.
2. Isolate tenants at the data layer (row-level security, schemas, databases) and at the request layer.
3. Contain noisy neighbours with quotas, rate limits and per-tenant limits.
4. Test for cross-tenant leaks.


### Multi-Tenancy

*This section is in [Chapter 15 — Multi-Tenancy](ch15-multi-tenancy.md), next to that chapter's practice material, so it is not repeated here.*

### Key Takeaways

- Isolation is a spectrum; cost falls and risk rises as sharing increases.
- Put the tenant id on every request, row and cache key, and enforce it below the application code.
- Plan for noisy neighbours before the first large customer arrives.

### Sample Interview Questions

- Compare row-level security with a database per tenant.
- How do you stop one tenant exhausting a shared connection pool?
- How would you migrate a tenant between shards?
- What is a tenant catalog and why keep one?

### Further Reading

- Microsoft Azure Architecture Center, *Multitenant solution architecture*
- AWS SaaS Lens, Well-Architected Framework


**Next Up:** Chapter 14 — Cloud Architecture & Cost →


*(From AI Library chapter 13.)*


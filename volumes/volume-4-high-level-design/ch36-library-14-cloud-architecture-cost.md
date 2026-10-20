# Chapter 36 — Library Ch 14 — Cloud Architecture & Cost

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 35 — Library Ch 13 — Multi-Tenancy](ch35-library-13-multi-tenancy.md) · Next → [Chapter 37 — Library Ch 15 — The System Design Blueprint](ch37-library-15-the-system-design-blueprint.md)

---

## Concept

Choosing managed services, serverless vs containers vs VMs, and designing with unit economics in mind.

**In one sentence:** Every architectural choice has a price.

Every architectural choice has a price. This chapter covers the cloud choices that shape a design (managed vs self-run, serverless vs containers vs VMs) and how to reason about cost per request, per tenant and per customer.

---

### Learning Outcomes

After reading this chapter, you'll be able to:

1. Apply the cloud well-architected pillars to a design.
2. Choose between serverless, containers and virtual machines with a break-even sketch.
3. Reason about cost per request, per active customer and per tenant.
4. Right-size continuously instead of once.


### Cloud Architecture Choices

*This section is in [Chapter 20 — Cloud Architecture](ch20-cloud-architecture.md), next to that chapter's practice material, so it is not repeated here.*

### Cost and Capacity Economics

*This section is in [Chapter 21 — Cost & Capacity Economics](ch21-cost-and-capacity-economics.md), next to that chapter's practice material, so it is not repeated here.*

### Key Takeaways

- Managed services trade money for operational load; use them unless a constraint says otherwise.
- Cost is a design-time property: estimate unit economics before you build.
- Lock-in is a cost to weigh, not a sin to avoid.

### Sample Interview Questions

- When is serverless cheaper than containers, and when is it not?
- How would you estimate cost per active customer?
- What does right-sizing mean in practice?
- How do you weigh lock-in against managed-service convenience?

### Further Reading

- AWS Well-Architected Framework, Cost Optimization pillar
- J.R. Storment and Mike Fuller, *Cloud FinOps*


**Next Up:** Chapter 15 — The System Design Blueprint →


*(From AI Library chapter 14.)*


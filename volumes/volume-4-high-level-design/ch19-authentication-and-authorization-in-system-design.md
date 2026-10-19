# Chapter 19 — Authentication & Authorization in System Design

> **Volume 4 — High-Level Design** · [Contents](index.md) · ← [Chapter 18 — Security at the System Level](ch18-security-at-the-system-level.md) · Next → [Chapter 20 — Cloud Architecture](ch20-cloud-architecture.md)

---

## Concept

Where identity is checked in a large system, how it travels between services, how tokens are issued, verified, rotated, and revoked at scale, how services trust each other, how permissions are decided, and how all of it survives failure.

**In one sentence:** in a distributed system, authentication happens once at the edge and becomes a signed identity that every hop can verify cheaply, while authorization is decided by the service that owns the data, using a policy it can check in microseconds and a design that keeps working when the identity service is down.

**Read the full explanation in the AI Library** (it is explained there once, so this chapter does not repeat it):

* [Chapter 5 — Authentication Primer: Proving Who You Are](https://charikshith.github.io/AI_Library/notes/system-design/chapters/5%20-%20Web%20Concepts%20in%20System%20Design%20%28System%20Design%20Fundamentals%29.html#53-authentication-primer-proving-who-you-are)
* [Chapter 10 — Authentication & Authorization
](https://charikshith.github.io/AI_Library/notes/system-design/chapters/10%20-%20Security%20in%20System%20Design%20%E2%80%93%20Principles%2C%20Practices%20%26%20Protocols.html#108-authentication--authorization)
* [Chapter 10 — Authentication and Authorization at Scale](https://charikshith.github.io/AI_Library/notes/system-design/chapters/10%20-%20Security%20in%20System%20Design%20%E2%80%93%20Principles%2C%20Practices%20%26%20Protocols.html#10812-authentication-and-authorization-at-scale)
* [Chapter 10 — Refresh Tokens: Rotation and Storage](https://charikshith.github.io/AI_Library/notes/system-design/chapters/10%20-%20Security%20in%20System%20Design%20%E2%80%93%20Principles%2C%20Practices%20%26%20Protocols.html#1087-refresh-tokens-rotation-and-storage)

This chapter is the **practice layer**: the diagram, worked example, exercises, mini-project, design prompt, open-source reading, interview questions and checklist below.

---

## Prereqs

* [Vol 2 Ch 12 — Authentication & Authorization](../volume-2-software-engineering/ch12-authentication-and-authorization.md)
* [Vol 2 Ch 11 — Security & Threat Modeling](../volume-2-software-engineering/ch11-security-and-threat-modeling.md)
* [Ch 5 — Proxies, Gateways, Web Servers & Storage Types](ch05-proxies-gateways-web-servers-and-storage-types.md)
* [Ch 10 — Service Mesh & Service Discovery](ch10-service-mesh-and-service-discovery.md)
* [Ch 15 — Multi-Tenancy](ch15-multi-tenancy.md)
* [Ch 18 — Security at the System Level](ch18-security-at-the-system-level.md)

---

## Diagram

**Edge authentication, token exchange, and service-to-service trust**

```mermaid
flowchart LR
    C["client<br/>(opaque token)"] --> GW["API gateway<br/>verify / introspect<br/>rate limit, coarse scopes"]
    GW -- "swap for short-lived<br/>internal JWT" --> O["orders service<br/>verify JWT locally<br/>object-level authz"]
    IDP["identity service (IdP)<br/>login, MFA, token issue"] -. "JWKS (cached)" .-> GW
    IDP -. "JWKS (cached)" .-> O
    GW -. "introspect (cached)" .-> IDP
    O -- "mTLS + token exchange<br/>(on behalf of user)" --> P["payments service<br/>allow: orders → POST /charges"]
    O --> PDP["policy sidecar (OPA)<br/>decision in &lt; 5 ms"]
```

**Login and token lifecycle, with revocation**

```mermaid
sequenceDiagram
    participant U as User
    participant GW as Gateway
    participant A as Auth service
    participant R as Redis
    participant S as Orders service
    U->>A: login (password + MFA)
    A->>A: Argon2id verify, rate limits
    A->>U: access JWT (10 min) + refresh token
    U->>GW: request + access JWT
    GW->>GW: verify signature, aud, exp (local)
    GW->>R: deny-list / user-version check
    GW->>S: forward with verified identity
    S->>S: authorize this user on this object
    Note over U,A: access token expires
    U->>A: refresh token
    A->>R: mark old refresh used, store new
    A->>U: new access + new refresh
    Note over A,R: password change or theft: bump user version, revoke refresh family
```

**Which revocation approach?**

```mermaid
flowchart TD
    Q{"how fast must a revoked<br/>token stop working?"} -- "minutes are fine" --> T["short TTL only"]
    Q -- "seconds" --> D{"many tokens per user?"}
    D -- yes --> V["per-user 'valid since' version in Redis"]
    D -- no --> L["deny-list of jti until exp"]
    Q -- "immediately" --> I["opaque tokens + introspection<br/>(cache for a few seconds)"]
```

---

## Example

```yaml
# Envoy: verify JWTs at the edge (jwt_authn filter)
http_filters:
- name: envoy.filters.http.jwt_authn
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.jwt_authn.v3.JwtAuthentication
    providers:
      corp_idp:
        issuer: https://auth.example.com
        audiences: ["orders-api"]
        remote_jwks:
          http_uri:
            uri: https://auth.example.com/.well-known/jwks.json
            cluster: idp
            timeout: 2s
          cache_duration: 600s          # keep working if the IdP is briefly down
        forward: false                  # do not pass the raw client token inward
        payload_in_metadata: jwt_payload
    rules:
    - match: { prefix: /api/ }
      requires: { provider_name: corp_idp }
- name: envoy.filters.http.router
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
```

```yaml
# Istio: only the orders workload may call POST /charges on payments (default deny otherwise)
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata: { name: payments-allow-orders, namespace: prod }
spec:
  selector:
    matchLabels: { app: payments }
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/prod/sa/orders"]   # the caller's mTLS identity
    to:
    - operation:
        methods: ["POST"]
        paths: ["/charges"]
```

```rego
# OPA policy: scope + same-tenant check. Anything not allowed is denied.
package orders.authz
import rego.v1

default allow := false

scopes := split(input.claims.scope, " ")

allow if {
    input.method == "GET"
    "orders:read" in scopes
    input.claims.tenant_id == input.resource.tenant_id
}

allow if {
    input.method == "POST"
    "orders:write" in scopes
    input.claims.tenant_id == input.resource.tenant_id
    input.claims.role in {"admin", "editor"}
}
```

```python
# Revocation check at the gateway: deny-list plus per-user "valid since" (Redis).
def is_revoked(claims: dict, redis) -> bool:
    if redis.exists(f"revoked:jti:{claims['jti']}"):              # one token revoked
        return True
    valid_since = redis.get(f"user:{claims['sub']}:valid_since")  # all tokens before this time
    return valid_since is not None and claims["iat"] < int(valid_since)

def revoke_user(redis, user_id: str, now: int):
    redis.set(f"user:{user_id}:valid_since", now)                 # logout everywhere / password change
```

---

## Exercises

1. Why must inner services verify identity again if the gateway already did?

   <details><summary>Solution</summary>Zero trust: the gateway can be bypassed (a misrouted call, a compromised pod, an internal tool), and only the service that owns the data can decide object-level access. A second local verification costs microseconds, so the safety is cheap. The gateway still does coarse checks and rate limiting; services do the fine ones.</details>

2. A service reads the user from an <code>X-User-Id</code> header. What goes wrong and how do you fix it?

   <details><summary>Solution</summary>Anything that can reach the service can set that header and become any user. Accept identity only from a signed token or an mTLS-authenticated gateway, make the gateway strip client-supplied copies, and have the service verify the signature itself.</details>

3. Revocation must take effect within 10 seconds for 5 million active users, with 20,000 requests per second. Pick an approach.

   <details><summary>Solution</summary>Short access tokens (5–10 minutes) plus a per-user "valid since" value in a replicated Redis. Each request costs one cache read (about 20,000 reads/s is small for Redis; add a local cache of 1–5 seconds if needed). One write revokes every token of a user. Deny-list by <code>jti</code> works too, but needs one entry per token. Opaque tokens give instant revocation but put the IdP or an introspection cache on every request.</details>

4. The identity service goes down for 20 minutes. What still works and what fails?

   <details><summary>Solution</summary>Requests with valid, unexpired access tokens keep working (local verification with cached JWKS). New logins and token refreshes fail; clients with expiring tokens will start failing within the token lifetime. Mitigations: cache JWKS, multi-zone IdP, a refresh grace window, and client backoff with jitter. Security decisions still fail closed.</details>

5. A customer wants to log in with their own company SSO. What do you build?

   <details><summary>Solution</summary>Per-tenant IdP configuration (OIDC or SAML), a tenant lookup at login (by email domain or tenant URL), mapping of the IdP user to a tenant membership and role, SCIM for provisioning and deprovisioning, and <code>tenant_id</code> in the token, checked on every resource access. Keep a break-glass admin path in case their IdP is down.</details>

---

## Mini project

**A gateway, an auth service, and two services with token exchange and service-level allow rules.**

```mermaid
flowchart LR
    U["curl / test client"] --> GW["gateway<br/>(Envoy or Traefik)"]
    GW --> AUTH["auth service<br/>login, JWT, JWKS, refresh"]
    GW --> ORD["orders service"]
    ORD -- "mTLS + exchanged token" --> PAY["payments service"]
    ORD --> OPA["OPA sidecar"]
    GW --> RED[("Redis<br/>deny-list, user version")]
```

**Steps**

1. Run an auth service that issues 10-minute RS256 JWTs (with `iss`, `aud`, `sub`, `tenant_id`, `scope`) and serves a JWKS endpoint.
2. Put a gateway in front that verifies the JWT locally (cached JWKS), strips client-supplied identity headers, and checks Redis for revocation.
3. Give `orders` a policy sidecar (OPA) that enforces scope and same-tenant access.
4. Make `orders` call `payments` over mTLS using a token exchanged for audience `payments`; allow only that caller and path.
5. Add rotation: publish a second signing key, switch signing, and keep serving both keys until old tokens expire.
6. Chaos tests: stop the auth service and show existing tokens still work; revoke one user and show requests fail within the target time; call `payments` directly without a certificate and show it is refused; send a token for tenant A to tenant B's resource and show it is denied.

**Done when:** all four chaos tests pass, key rotation causes zero failed requests, and every denial appears in a decision log with a reason.

---

## Design

**Design 1 — Authentication for a multi-tenant B2B SaaS with enterprise SSO.**

* **Requirements:** 5,000 tenants, 2M users, some tenants require SAML or OIDC SSO and SCIM, others use email + password with MFA; sensitive data separated per tenant; an admin console.
* **Shape:** a hosted or self-run IdP fronts logins; per-tenant IdP federation; the gateway verifies JWTs; each service enforces `tenant_id` plus roles; SCIM endpoint for user lifecycle; audit log for every login and permission change.
* **Decisions to justify:** build vs buy the IdP; how a login finds its tenant; how roles are stored and cached; how a tenant's IdP outage is handled (break-glass admin); whether each tenant gets its own signing key; how support impersonation is audited.

**Design 2 — Identity for a public API platform.**

* **Requirements:** third-party developers, 50,000 API clients, 20,000 requests per second at peak, user-granted access (OAuth2) and server-to-server keys, per-client limits and billing, instant disable of an abused key.
* **Shape:** developer portal issues clients and keys; Authorization Code + PKCE for user access and Client Credentials for server access; API keys stored as hashes with a prefix, scopes, and an owner; the gateway checks keys/tokens (cached) and applies per-client rate limits; usage events go to a queue for billing; webhooks are HMAC-signed.
* **Decisions to justify:** opaque keys with cached lookup versus JWT access tokens; how fast a disabled key must stop working and how you ensure it; how keys are rotated without downtime; what you log without logging secrets.

**Design 3 — Login and sessions for a consumer app with 100M users.**

* **Requirements:** 10M daily active users, peak 2,000 logins per second, mobile and web, social sign-in (OIDC), passkeys, strong defence against credential stuffing, revocation within 10 seconds on password change.
* **Shape:** a dedicated auth service (autoscaled for password hashing) behind its own rate limits and bot checks; short-lived access JWT plus rotating refresh tokens in HttpOnly cookies (web) or secure storage (mobile); Redis for refresh families and the user "valid since" version; passkeys as the preferred factor; multi-region with a primary for writes or a globally replicated store.
* **Decisions to justify:** sessions versus tokens for web; how many cores the login path needs and where hashing runs; how to rate-limit by IP and by account without locking out real users; whether login is multi-region active-active, and how to avoid a password change taking effect only in one region.

---

## Open source

* [`keycloak/keycloak`](https://github.com/keycloak/keycloak) and [`ory/hydra`](https://github.com/ory/hydra) — identity providers and OAuth2/OIDC servers.
* [`spiffe/spire`](https://github.com/spiffe/spire) — workload identity (SPIFFE IDs and short-lived certificates).
* [`envoyproxy/envoy`](https://github.com/envoyproxy/envoy) — the `jwt_authn` and external authorization filters; [`oauth2-proxy/oauth2-proxy`](https://github.com/oauth2-proxy/oauth2-proxy) — put OIDC login in front of an app.
* [`open-policy-agent/opa`](https://github.com/open-policy-agent/opa) and [`authzed/spicedb`](https://github.com/authzed/spicedb) — policy engine and Zanzibar-style relationship-based authorization.
* [`hashicorp/vault`](https://github.com/hashicorp/vault) — dynamic credentials and a transit/signing engine.

---

## Interview

1. **"Where would you authenticate in a microservices system?"**
   <details><summary>Answer</summary>At the edge (API gateway) first: verify the token, apply rate limits and coarse scope checks. Then inside each service verify the signed identity again (local JWT verification or mTLS) and do object-level authorization, because only the service owns the data and the gateway can be bypassed. The identity service issues tokens; it is not called on every request.</details>

2. **"How do services call each other securely?"**
   <details><summary>Answer</summary>Give each workload a short-lived identity (mTLS certificates via a mesh or SPIRE, or client-credentials tokens), verify it on both sides, and add default-deny allow rules per caller and path. When acting for a user, exchange the user's token for one scoped to the next service so identity propagates without replay or confused-deputy problems.</details>

3. **"JWT revocation at scale: how?"**
   <details><summary>Answer</summary>Keep access tokens short (minutes) so revocation is bounded. For faster cut-off, store a per-user "valid since" version (or a <code>jti</code> deny-list) in a replicated cache that the gateway checks — a single cheap read — and revoke refresh tokens. If immediate revocation is required, use opaque tokens with a cached introspection call.</details>

4. **"What happens to your system if the auth service is down?"**
   <details><summary>Answer</summary>Valid tokens keep working because verification is local with cached public keys. New logins and refreshes fail, so tokens expire into errors within their lifetime. Reduce the impact with a multi-zone or multi-region IdP, JWKS caching, a refresh grace window, client backoff, and fail-closed security decisions with clear alerting.</details>

5. **"How would you design enterprise SSO for a multi-tenant SaaS?"**
   <details><summary>Answer</summary>Per-tenant OIDC/SAML federation to the customer's IdP, tenant resolution at login (domain or tenant URL), tenant memberships and roles in your database, SCIM for provisioning, <code>tenant_id</code> in tokens checked on every resource access, per-tenant audit logs, and a break-glass admin path for IdP outages.</details>

6. **"Centralized policy service or library per service?"**
   <details><summary>Answer</summary>A library or sidecar gives low latency and no new network dependency, but risks version drift. A central decision service gives one place to change rules and supports relationship graphs, but adds a hop and a critical dependency, so cache decisions and set tight timeouts. Many systems use a shared policy language (OPA/Cedar) with sidecar evaluation and central policy distribution.</details>

7. **"How do you protect the login endpoint from credential stuffing?"**
   <details><summary>Answer</summary>Rate-limit per IP and per account, check passwords against breach lists, add bot detection and CAPTCHA on suspicious patterns, require MFA or passkeys, return identical errors for unknown user and wrong password, and alert on spikes in failures. Run password hashing in its own scalable service so attacks cannot starve other traffic.</details>

---

## Checklist

- [ ] authenticate at the edge and verify again inside services
- [ ] never trust identity headers that did not come from a verified source
- [ ] give every workload an identity and default-deny service-to-service calls
- [ ] rotate signing keys with overlap; cache JWKS
- [ ] choose a revocation approach that matches the risk
- [ ] keep the identity service off the per-request path
- [ ] enforce tenant and object checks in the owning service
- [ ] log every authorization decision

---

> [Contents](index.md) · ← [Chapter 18 — Security at the System Level](ch18-security-at-the-system-level.md) · Next → [Chapter 20 — Cloud Architecture](ch20-cloud-architecture.md)

# Chapter 25 — Configuration & Secrets Management

> **Volume 1 — Computer Science Foundations** · [Contents](index.md) · ← [Chapter 24 — Logging](ch24-logging.md) · Next → [Chapter 26 — Testing: Unit, Integration, Mocking & Coverage](ch26-testing-unit-integration-mocking-and-coverage.md)

---

## Concept

Environment variables, dotenv, YAML/TOML/JSON config, and keeping secrets out of code.

**In one sentence:** configuration is everything that changes between environments (dev, staging, prod), so it belongs outside the code; secrets are the dangerous subset of configuration that must never be committed, printed, or shared in plain text.

**Mental model — a hotel room.** The building (your code) is identical everywhere. Each guest's room settings — temperature, wake-up call (config) — are set at check-in. The room safe's code (a secret) is never written on the door, never photocopied, and changed when a guest leaves.

**Where config comes from, lowest to highest precedence**

| Layer | Example | Good for |
|-------|---------|----------|
| 1. Defaults in code | `port: int = 8080` | sensible fallbacks |
| 2. Config file | `config.toml`, `settings.yaml` | structured, versioned, non-secret settings |
| 3. Environment variables | `APP_PORT=9000` | per-deployment values (12-factor) |
| 4. CLI flags | `--port 9001` | one-off overrides |
| Secrets store | Vault, AWS Secrets Manager, K8s Secrets, 1Password | passwords, keys, tokens |

Later layers override earlier ones. **Make the precedence explicit and document it.**

**Config file vs env var**

| | Config file | Environment variable |
|-|-------------|----------------------|
| Structure | nested, typed, commented | flat strings |
| Versioned | yes (non-secret files) | no |
| Changes per deploy? | rarely | often |
| Visible to | anyone with the repo | the process (and its children, `/proc/<pid>/environ`, crash dumps) |

**Secrets rules**

1. Never in git — not even in "private" repos. History is forever; rotate if leaked.
2. Commit a `.env.example` with fake values; add `.env` to `.gitignore`.
3. Prefer short-lived, automatically rotated credentials (IAM roles, workload identity, Vault dynamic secrets) over long-lived keys.
4. Scan: pre-commit hooks and CI secret scanners (`gitleaks`, GitHub push protection).
5. Least privilege: each service gets only the secrets it needs.
6. Keep secrets out of logs, error messages, and URLs.

**Fail fast** — validate all config at startup: required keys present, types right, values in range. A service that starts with a broken config fails later, at the worst moment.

---

## Prereqs

* [Chapter 8 — Data Formats (Text): JSON, CSV, XML, YAML, TOML](ch08-data-formats-text-json-csv-xml-yaml.md)
* [Chapter 24 — Logging](ch24-logging.md)

---

## Diagram

**A 12-factor config flow**

```mermaid
flowchart LR
    D["defaults<br/>(in code)"] --> M["merge<br/>(precedence)"]
    F["config.toml"] --> M
    E["env vars<br/>APP_*"] --> M
    C["CLI flags"] --> M
    V[("Vault /<br/>Secrets Manager")] -->|"fetched at startup<br/>via workload identity"| M
    M --> VAL{"validate<br/>types, ranges,<br/>required keys"}
    VAL -- invalid --> X["exit 2 with a clear error"]
    VAL -- valid --> CFG["typed, immutable Config object"] --> APP[application]
```

**Precedence as layers**

```
  CLI flags        --port 9001            ▲ wins
  env vars         APP_PORT=9000          │
  config file      port = 8081            │
  defaults         port = 8080            │ loses
  ───────────────────────────────────────
  effective:       port = 9001
```

**Secret rotation**

```mermaid
sequenceDiagram
    participant App
    participant Vault
    participant DB
    App->>Vault: auth (Kubernetes service account)
    Vault->>DB: CREATE ROLE app_7f3 VALID UNTIL +1h
    Vault-->>App: user=app_7f3, password=…, lease 1h
    App->>DB: connect
    Note over Vault,DB: lease expires → Vault drops the role automatically
```

---

## Example

```python
# config.py — typed, layered, validated at startup (pydantic-settings)
from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env")
    # (a TOML file layer needs TomlConfigSettingsSource via settings_customise_sources)

    port: int = Field(8080, ge=1, le=65535)
    debug: bool = False
    database_url: PostgresDsn                  # required: startup fails if missing
    stripe_api_key: SecretStr                  # prints as '**********'

settings = Settings()                          # raises ValidationError with every problem listed
print(settings.stripe_api_key)                 # **********
key = settings.stripe_api_key.get_secret_value()   # only where actually needed
```

```bash
# .env.example — committed, fake values
APP_DATABASE_URL=postgres://user:pass@localhost:5432/app
APP_STRIPE_API_KEY=sk_test_replace_me

# .gitignore
.env
```

```python
import os
db_url = os.getenv("DB_URL")                   # None if missing — check it!
if not db_url:
    raise SystemExit("DB_URL is required (see .env.example)")
```

---

## Exercises

1. Load config with layered precedence (defaults < file < env).

   <details><summary>Solution</summary>

   ```python
   import os, tomllib
   DEFAULTS = {"port": 8080, "debug": False}
   def load(path="config.toml"):
       cfg = dict(DEFAULTS)
       if os.path.exists(path):
           with open(path, "rb") as f:
               cfg |= tomllib.load(f).get("server", {})
       if "APP_PORT" in os.environ:
           cfg["port"] = int(os.environ["APP_PORT"])
       if "APP_DEBUG" in os.environ:
           cfg["debug"] = os.environ["APP_DEBUG"].lower() in ("1", "true", "yes")
       return cfg
   ```
   Note that env vars are strings and must be parsed.
   </details>

2. Move a hardcoded API key into a secret store.

   <details><summary>Solution</summary>(1) Rotate the key first — it's in git history. (2) Store the new key in the secret manager. (3) Grant only this service's identity read access. (4) Read it at startup into a <code>SecretStr</code>. (5) Remove it from code and add a secret scanner to CI. Deleting the line is not enough; the old value must be revoked.</details>

3. Why is `https://api.example.com?api_key=…` a bad pattern?

   <details><summary>Solution</summary>URLs end up in access logs, proxy logs, browser history, and <code>Referer</code> headers. Send credentials in an <code>Authorization</code> header instead.</details>

---

## Mini project

**A config loader supporting file + env + CLI overrides, failing fast on missing keys.**

```mermaid
flowchart TD
    A["argv"] --> P["argparse: --config, --port, --set key=value"]
    P --> L["load TOML"]
    L --> E["overlay APP_* env vars<br/>(APP_DB__HOST → db.host)"]
    E --> C["overlay CLI --set"]
    C --> S["validate against schema"]
    S -- errors --> R["print ALL errors, exit 2"]
    S -- ok --> O["frozen dataclass Config"]
    O --> SHOW["--print-config shows effective values<br/>with secrets masked and the source of each"]
```

**Steps**

1. Schema as a frozen dataclass or pydantic model with types, defaults, and required fields.
2. Merge layers; `__` in env var names maps to nesting (`APP_DB__HOST`).
3. `--print-config` shows each effective value *and where it came from* (default / file / env / cli), masking secrets.
4. Collect every validation error before exiting.
5. Tests for precedence, type coercion, missing required keys, and masking.

**Done when:** a missing `database_url` stops startup with one clear line, and `--print-config` never shows a secret.

---

## Open source

* [`theskumar/python-dotenv`](https://github.com/theskumar/python-dotenv) — loads `.env` files into the environment for local development.
* [`hashicorp/vault`](https://github.com/hashicorp/vault) — secrets engines, dynamic database credentials, leases, and audit logs.

---

## Interview

1. **"Why never commit secrets?"**
   <details><summary>Answer</summary>Git history is permanent and widely copied: forks, clones, CI caches, laptops. Bots scan public repos for keys within minutes. Even private repos leak through compromised accounts or later open-sourcing. A committed secret must be treated as compromised and rotated.</details>

2. **"Config file vs env var — when each?"**
   <details><summary>Answer</summary>Files for structured, mostly-static, non-secret settings that benefit from versioning and comments (feature settings, timeouts). Env vars for values that differ per deployment (URLs, ports, flags) and for injecting secrets from a secret manager at runtime. Many apps use both, with env overriding file.</details>

---

## Checklist

- [ ] precedence is explicit
- [ ] secrets never in git
- [ ] validate config at startup

---

> [Contents](index.md) · ← [Chapter 24 — Logging](ch24-logging.md) · Next → [Chapter 26 — Testing: Unit, Integration, Mocking & Coverage](ch26-testing-unit-integration-mocking-and-coverage.md)

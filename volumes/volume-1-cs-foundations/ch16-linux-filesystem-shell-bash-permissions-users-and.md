# Chapter 16 — Linux: Filesystem, Shell, Bash, Permissions, Users & Groups

> **Volume 1 — Computer Science Foundations** · [Contents](index.md) · ← [Chapter 15 — Correctness Traps](ch15-correctness-traps.md) · Next → [Chapter 17 — Linux: Processes, Signals, Services, systemd, SSH, Cron & Networking](ch17-linux-processes-signals-services-systemd-ssh-cron.md)

---

## Concept

The Unix filesystem tree, shell basics, Bash scripting, file permissions, users and groups.

**In one sentence:** in Linux everything hangs off one tree starting at `/`, you drive it by typing commands into a shell, and every file says which user, which group, and everyone else may read, write, or run it.

**Mental model — an office building.** `/` is the lobby. Each folder is a room. Your *user* is your badge; *groups* are departments. Each door (file) has a sign with three rows: what the owner may do, what the owner's department may do, and what anyone else may do.

**The filesystem tree**

| Path | Holds |
|------|-------|
| `/` | the root of everything |
| `/home/alice` | Alice's files (`~` is a shortcut) |
| `/root` | the superuser's home |
| `/etc` | system configuration (`/etc/passwd`, `/etc/ssh/sshd_config`) |
| `/bin`, `/usr/bin` | programs (`ls`, `grep`) |
| `/var/log` | logs |
| `/tmp` | temporary files, often cleared on reboot |
| `/dev` | devices as files (`/dev/null`, `/dev/sda`) |
| `/proc`, `/sys` | live kernel and process info as virtual files |
| `/opt`, `/srv` | add-on software, served data |

**Permissions**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 700 240" role="img" aria-label="Reading ls -l output: type, owner, group and others permission triplets" style="width:100%;max-width:700px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><text x="30" y="40" font-size="17" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--text)" xml:space="preserve">-rwxr-x---  1  alice  devs  4096  script.sh</text><text x="149.4" y="62" font-size="1" text-anchor="middle" fill="var(--text)"></text><line x1="35.2" y1="48" x2="35.2" y2="80" stroke="var(--text-muted)" stroke-width="1.4"/><line x1="35.2" y1="80" x2="330" y2="80" stroke="var(--text-muted)" stroke-width="1.4"/><text x="338" y="84" font-size="12.5" text-anchor="start" fill="var(--text)">type: - file, d directory, l symlink</text><line x1="56.0" y1="48" x2="56.0" y2="108" stroke="var(--primary)" stroke-width="1.4"/><line x1="56.0" y1="108" x2="330" y2="108" stroke="var(--primary)" stroke-width="1.4"/><text x="338" y="112" font-size="12.5" text-anchor="start" fill="var(--text)">owner:  rwx  = 4+2+1 = 7</text><line x1="87.2" y1="48" x2="87.2" y2="136" stroke="var(--success)" stroke-width="1.4"/><line x1="87.2" y1="136" x2="330" y2="136" stroke="var(--success)" stroke-width="1.4"/><text x="338" y="140" font-size="12.5" text-anchor="start" fill="var(--text)">group:  r-x  = 4+0+1 = 5</text><line x1="118.4" y1="48" x2="118.4" y2="164" stroke="var(--danger)" stroke-width="1.4"/><line x1="118.4" y1="164" x2="330" y2="164" stroke="var(--danger)" stroke-width="1.4"/><text x="338" y="168" font-size="12.5" text-anchor="start" fill="var(--text)">others: ---  = 0</text><text x="206.8" y="62" font-size="11.5" text-anchor="start" fill="var(--text-muted)">owner</text><text x="279.6" y="62" font-size="11.5" text-anchor="start" fill="var(--text-muted)">group</text></svg>
</div>

| Bit | Value | On a file | On a directory |
|-----|:-:|-----------|----------------|
| `r` | 4 | read contents | list names (`ls`) |
| `w` | 2 | modify contents | create / delete / rename entries inside |
| `x` | 1 | run as a program | enter it (`cd`) and reach files inside |

Common modes: `644` (files: owner writes, all read), `755` (programs and dirs), `600` (secrets: owner only), `700` (private dirs). Special bits: **setuid** (runs as the file's owner — how `passwd` works), **setgid**, and the **sticky bit** on `/tmp` (only the owner can delete their own files).

**Shell essentials**

| Concept | Syntax |
|---------|--------|
| Pipe output into another command | `cmd1 \| cmd2` |
| Redirect stdout / stderr / both | `> out.txt`, `2> err.txt`, `&> all.txt`, `>>` appends |
| Variables | `name="x"; echo "$name"` — **always quote** |
| Command substitution | `today=$(date +%F)` |
| Exit status | `$?`; 0 = success; `&&` runs next on success, `\|\|` on failure |
| Globs | `*.txt`, `file?.log`, `{a,b}.conf` |

**Safe Bash header:** `set -euo pipefail` — exit on errors (`-e`), fail on unset variables (`-u`), and fail a pipeline if any part fails (`pipefail`).

---

## Prereqs

None.

---

## Diagram

**Filesystem tree with permission annotations**

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 306" role="img" aria-label="A Linux directory tree with each entry's permissions, owner and group" style="width:100%;max-width:900px;height:auto;font-family:inherit"><defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs><text x="14" y="20" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--primary)" font-weight="600">📁 /</text><text x="250" y="20" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← drwxr-xr-x  root  root</text><line x1="24" y1="32" x2="24" y2="44" stroke="var(--border)" stroke-width="1.4"/><line x1="24" y1="44" x2="34" y2="44" stroke="var(--border)" stroke-width="1.4"/><text x="38" y="46" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--primary)" font-weight="600">📁 etc/</text><text x="250" y="46" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← drwxr-xr-x  root  root</text><line x1="48" y1="58" x2="48" y2="70" stroke="var(--border)" stroke-width="1.4"/><line x1="48" y1="70" x2="58" y2="70" stroke="var(--border)" stroke-width="1.4"/><text x="62" y="72" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--text)" font-weight="400">📄 passwd</text><text x="250" y="72" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← -rw-r--r--  root  root    (everyone may read)</text><line x1="48" y1="84" x2="48" y2="96" stroke="var(--border)" stroke-width="1.4"/><line x1="48" y1="96" x2="58" y2="96" stroke="var(--border)" stroke-width="1.4"/><text x="62" y="98" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--text)" font-weight="400">📄 shadow</text><text x="250" y="98" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← -rw-r-----  root  shadow  (password hashes: locked)</text><line x1="24" y1="110" x2="24" y2="122" stroke="var(--border)" stroke-width="1.4"/><line x1="24" y1="122" x2="34" y2="122" stroke="var(--border)" stroke-width="1.4"/><text x="38" y="124" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--primary)" font-weight="600">📁 home/</text><line x1="48" y1="136" x2="48" y2="148" stroke="var(--border)" stroke-width="1.4"/><line x1="48" y1="148" x2="58" y2="148" stroke="var(--border)" stroke-width="1.4"/><text x="62" y="150" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--primary)" font-weight="600">📁 alice/</text><text x="250" y="150" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← drwx------  alice  alice   (private)</text><line x1="72" y1="162" x2="72" y2="174" stroke="var(--border)" stroke-width="1.4"/><line x1="72" y1="174" x2="82" y2="174" stroke="var(--border)" stroke-width="1.4"/><text x="86" y="176" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--text)" font-weight="400">📄 notes.txt</text><text x="250" y="176" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← -rw-r--r--  alice  alice</text><line x1="72" y1="188" x2="72" y2="200" stroke="var(--border)" stroke-width="1.4"/><line x1="72" y1="200" x2="82" y2="200" stroke="var(--border)" stroke-width="1.4"/><text x="86" y="202" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--text)" font-weight="400">📄 deploy.sh</text><text x="250" y="202" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← -rwxr-x---  alice  devs    (750)</text><line x1="24" y1="214" x2="24" y2="226" stroke="var(--border)" stroke-width="1.4"/><line x1="24" y1="226" x2="34" y2="226" stroke="var(--border)" stroke-width="1.4"/><text x="38" y="228" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--primary)" font-weight="600">📁 tmp/</text><text x="250" y="228" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← drwxrwxrwt  root  root    (t = sticky bit)</text><line x1="24" y1="240" x2="24" y2="252" stroke="var(--border)" stroke-width="1.4"/><line x1="24" y1="252" x2="34" y2="252" stroke="var(--border)" stroke-width="1.4"/><text x="38" y="254" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--text)" font-weight="400">📄 usr/bin/passwd</text><text x="250" y="254" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← -rwsr-xr-x  root  root    (s = setuid)</text><line x1="24" y1="266" x2="24" y2="278" stroke="var(--border)" stroke-width="1.4"/><line x1="24" y1="278" x2="34" y2="278" stroke="var(--border)" stroke-width="1.4"/><text x="38" y="280" font-size="13" font-family="ui-monospace,Menlo,Consolas,monospace" fill="var(--primary)" font-weight="600">📁 var/log/</text><text x="250" y="280" font-size="12.5" text-anchor="start" fill="var(--text-muted)">← drwxr-xr-x  root  root</text></svg>
</div>

**How the kernel checks access**

```mermaid
flowchart TD
    R["alice runs: cat deploy.sh"] --> U{"alice is the owner?"}
    U -- yes --> OB["use owner bits rwx"]
    U -- no --> G{"alice in group 'devs'?"}
    G -- yes --> GB["use group bits r-x"]
    G -- no --> OT["use other bits ---"]
    OB & GB & OT --> D{"bit for this action set?"}
    D -- yes --> ALLOW[allowed]
    D -- no --> DENY["Permission denied"]
```

Only the *first* matching class counts. If you are the owner with `---`, group bits do not rescue you.

---

## Example

```bash
chmod 750 script.sh            # rwx for owner, r-x for group, nothing for others
chmod u+x,g-w file             # symbolic form
chown alice:devs script.sh     # change owner and group
ls -l script.sh
id                             # uid=1000(alice) gid=1000(alice) groups=1000(alice),27(sudo),1001(devs)
sudo usermod -aG devs bob      # add bob to devs (-a: append, don't replace groups)
umask                          # 0022 → new files 644, new dirs 755
```

```bash
#!/usr/bin/env bash
set -euo pipefail

# Count lines in every .txt file (quoted, so spaces in names are safe)
for f in *.txt; do
    [[ -e "$f" ]] || continue            # no matches → the glob stays literal; skip it
    printf '%6d  %s\n' "$(wc -l < "$f")" "$f"
done

# Functions, arguments, and exit codes
backup() {
    local src="$1" dest="$2"
    cp -a -- "$src" "$dest" || { echo "copy failed: $src" >&2; return 1; }
}
backup notes.txt /tmp/notes.bak && echo "ok"
```

---

## Exercises

1. Explain `chmod 750` in words.

   <details><summary>Solution</summary>Owner: read, write, execute (7). Group: read and execute, no write (5). Others: no access (0). Typical for a script shared with your team but hidden from everyone else.</details>

2. Write a Bash script that finds and deletes files older than 30 days.

   <details><summary>Solution</summary>

   ```bash
   #!/usr/bin/env bash
   set -euo pipefail
   dir="${1:?usage: $0 DIR}"
   find "$dir" -type f -mtime +30 -print          # dry run first: look before deleting
   read -rp "Delete these? [y/N] " ok
   [[ "$ok" == "y" ]] && find "$dir" -type f -mtime +30 -delete
   ```
   <code>${1:?…}</code> stops the script if no directory is given, so it never runs <code>find</code> on an empty path.
   </details>

3. Why does `rm -rf $DIR/` with an unset `DIR` destroy a system, and how does `set -u` help?

   <details><summary>Solution</summary>Unset and unquoted, it expands to <code>rm -rf /</code>. <code>set -u</code> makes the script exit on the unset variable before running <code>rm</code>. Also quote it (<code>"$DIR"</code>) and use <code>${DIR:?}</code>.</details>

---

## Mini project

**A Bash backup script with permission handling and a cron entry.**

```mermaid
flowchart LR
    C["cron 02:30 daily"] --> S["backup.sh"] --> L{"lock free?<br/>(flock)"}
    L -- no --> X[exit: already running]
    L -- yes --> T["tar + gzip ~/projects<br/>→ /backups/2024-05-01.tgz"] --> P["chmod 600, chown backup:backup"] --> R["delete archives older than 14 days"] --> LOG["append to /var/log/backup.log"]
```

**Steps**

1. `set -euo pipefail`; take the source and destination as arguments with defaults.
2. Use `flock` so two runs never overlap.
3. Create a dated archive with `tar -czf`; set `umask 077` so archives are private from creation.
4. Keep the last 14 archives; delete older ones with `find -mtime +14 -delete`.
5. Log start, end, size, and exit status; exit non-zero on failure.
6. Install with `crontab -e`: `30 2 * * * /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1`.

**Done when:** archives are mode 600, a second concurrent run exits cleanly, and a restore test gives back identical files (`diff -r`).

---

## Open source

* [`torvalds/linux`](https://github.com/torvalds/linux) (permission model) — `fs/namei.c`, function `generic_permission`, is the owner → group → other check shown in the diagram.
* [`bash`](https://www.gnu.org/software/bash/) — the manual's "Shell Expansions" section explains the order of brace, tilde, parameter, command, arithmetic, word-splitting, and glob expansion — the root of most quoting bugs.

---

## Interview

1. **"What do 4/2/1 mean in permissions?"**
   <details><summary>Answer</summary>Read = 4, write = 2, execute = 1. Add them per class (owner, group, others) to get one octal digit each. So 754 = rwx for owner, r-x for group, r-- for others.</details>

2. **"How do you make a script executable?"**
   <details><summary>Answer</summary>Add a shebang line (<code>#!/usr/bin/env bash</code>), then <code>chmod +x script.sh</code>, and run it with <code>./script.sh</code> (or put it on <code>$PATH</code>). Without the execute bit you can still run it as <code>bash script.sh</code>.</details>

---

## Checklist

- [ ] navigate the tree by heart
- [ ] set permissions correctly
- [ ] write a safe Bash script

---

> [Contents](index.md) · ← [Chapter 15 — Correctness Traps](ch15-correctness-traps.md) · Next → [Chapter 17 — Linux: Processes, Signals, Services, systemd, SSH, Cron & Networking](ch17-linux-processes-signals-services-systemd-ssh-cron.md)

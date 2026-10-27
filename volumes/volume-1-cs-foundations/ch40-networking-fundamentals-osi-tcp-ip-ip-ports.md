# Chapter 40 — Networking Fundamentals: OSI, TCP/IP, IP, Ports, DNS & NAT

> **Volume 1 — Computer Science Foundations** · [Contents](index.md) · ← [Chapter 39 — OS: Memory Management, File Systems, System Calls & IPC](ch39-os-memory-management-file-systems-system-calls.md) · Next → [Chapter 41 — Transport & Security: TCP, UDP, QUIC, TLS & HTTPS](ch41-transport-and-security-tcp-udp-quic-tls.md)

---

## Concept

Layered models, IP addressing/subnets, ports, DNS resolution, and NAT.

**In one sentence:** networks are built in layers — each layer wraps the one above it in its own envelope — IP addresses find the machine, ports find the program on it, DNS turns names into addresses, and NAT lets a whole house share one public address.

### Mental model — sending a letter

Your letter (data) goes in an envelope addressed to an apartment number (the port) in a building (the IP address). The post office (routers) reads only the building address and forwards it hop by hop. The phone book (DNS) turns "Alice's Bakery" into a street address. Your building's front desk (NAT) sends all residents' mail out under the building's single address and routes replies back to the right apartment.

### OSI vs TCP/IP

| OSI # | OSI layer | TCP/IP layer | Unit | Examples | Job |
|:-:|-----------|--------------|------|----------|-----|
| 7 | Application | Application | message | HTTP, DNS, SSH, SMTP | what the app says |
| 6 | Presentation | ↑ | | TLS, encoding | format, encryption |
| 5 | Session | ↑ | | (TLS sessions, RPC) | dialogue control |
| 4 | Transport | Transport | segment / datagram | TCP, UDP, QUIC | process-to-process, ports, reliability |
| 3 | Network | Internet | packet | IP, ICMP | host-to-host across networks (routing) |
| 2 | Data link | Link | frame | Ethernet, Wi-Fi, ARP | to the next hop on the local network (MAC addresses) |
| 1 | Physical | ↓ | bits | copper, fiber, radio | signals |

"L4 load balancer" and "L7 firewall" refer to these OSI numbers.

### IP addressing

| Concept | Example | Meaning |
|---------|---------|---------|
| IPv4 | `192.168.1.10` | 32 bits, ~4.3 billion addresses |
| IPv6 | `2001:db8::1` | 128 bits; `::` collapses runs of zeros |
| CIDR | `192.168.1.0/24` | the first 24 bits are the network; 8 bits for hosts |
| Hosts in a /24 | 256 − 2 = 254 | minus the network address (.0) and broadcast (.255) |
| Private ranges (RFC 1918) | `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | not routed on the internet |
| Loopback | `127.0.0.1`, `::1` | this machine |
| Socket | `192.168.1.10:443` | IP + port = one endpoint |

### Ports

16-bit numbers (0–65535). Well-known: 22 SSH, 53 DNS, 80 HTTP, 443 HTTPS, 5432 Postgres, 6379 Redis. Clients use *ephemeral* ports (Linux default 32768–60999). A TCP connection is identified by the **4-tuple** (src IP, src port, dst IP, dst port).

### Port exhaustion

One client IP talking to one server IP:port has only ~28k ephemeral ports. Short-lived connections sit in `TIME_WAIT` for up to 60 s, so a busy proxy can run out and fail to connect. Fixes: connection pooling / keep-alive, more source IPs, widen `ip_local_port_range`, reuse `TIME_WAIT` sockets safely.

### DNS record types

| Type | Maps | Example |
|------|------|---------|
| A / AAAA | name → IPv4 / IPv6 | `example.com → 93.184.215.14` |
| CNAME | alias → canonical name | `www → example.com` |
| MX | domain → mail server | |
| TXT | free text | SPF, domain verification |
| NS | zone → authoritative servers | |
| TTL | how long resolvers may cache it | 300 s |

### DNS as a dependency — and a single point of failure

- **Choosing a TTL is a trade-off.** Long TTLs mean fewer lookups and less load on name servers, but a changed record (a failover, a migration) takes that long to reach everyone. Short TTLs make changes fast but add lookup latency and load — and the shorter the TTL, the more clients break immediately if your name servers go down.
- **Not every client respects the TTL.** Some resolvers and long-running clients cache longer, so expect a trickle of traffic to old addresses well after a change; keep old endpoints alive for a while.
- **If DNS fails, nothing else matters.** Clients that can't resolve your name can't reach you, however healthy your servers are. Real outages have come from expired domain registrations, a provider's name servers being DDoSed (Dyn, 2016), and whole top-level domains having trouble. Use more than one DNS provider for critical names, monitor domain and certificate expiry, and keep TTLs sensible.
- **Serve stale rather than fail.** A resolver that can't reach the authoritative servers can keep answering with an *expired* cached record (standardized as "serve-stale", RFC 8767) — the address almost never changed, so a stale answer beats no answer. The general principle — keep working with the last known good data when a dependency is down — is called *static stability*.
- **Privacy.** Classic DNS is plain text over UDP, visible to anyone on the path; **DNS over TLS (DoT)** and **DNS over HTTPS (DoH)** encrypt it.

### NAT

A router rewrites private source addresses and ports to its public address and keeps a table to map replies back. It stretches IPv4 and blocks *unsolicited* inbound connections, but it is **not a firewall**, it breaks peer-to-peer (needing STUN/TURN), and it complicates logs and rate limiting (many users share one IP).

---

## Prereqs

None.

---

## Diagram

### OSI 7 layers next to TCP/IP 4 layers, with encapsulation

<div class="fig">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 612" role="img" aria-label="OSI seven layers next to the TCP/IP four layers, with the headers each layer adds" style="width:100%;max-width:900px;height:auto;font-family:inherit">
<defs><marker id="osiar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="var(--text-muted)"/></marker></defs>
<text x="20" y="40" font-size="15" font-weight="700" fill="var(--text)">OSI model · 7 layers</text>
<line x1="20" y1="50" x2="270" y2="50" stroke="var(--border)" stroke-width="2"/>
<text x="290" y="40" font-size="15" font-weight="700" fill="var(--text)">TCP/IP model · 4 layers</text>
<line x1="290" y1="50" x2="480" y2="50" stroke="var(--border)" stroke-width="2"/>
<text x="500" y="40" font-size="15" font-weight="700" fill="var(--text)">What each layer adds (sending side)</text>
<line x1="500" y1="50" x2="860" y2="50" stroke="var(--border)" stroke-width="2"/>
<rect x="20" y="78" width="250" height="54" rx="10" fill="var(--primary)" fill-opacity=".14" stroke="var(--primary)" stroke-width="1.6"/>
<text x="36" y="102" font-size="14" font-weight="700" fill="var(--text)">7  Application</text>
<text x="36" y="120" font-size="12" fill="var(--text-muted)">HTTP, DNS, SMTP, SSH</text>
<rect x="20" y="136" width="250" height="54" rx="10" fill="var(--primary)" fill-opacity=".14" stroke="var(--primary)" stroke-width="1.6"/>
<text x="36" y="160" font-size="14" font-weight="700" fill="var(--text)">6  Presentation</text>
<text x="36" y="178" font-size="12" fill="var(--text-muted)">TLS, encoding, compression</text>
<rect x="20" y="194" width="250" height="54" rx="10" fill="var(--primary)" fill-opacity=".14" stroke="var(--primary)" stroke-width="1.6"/>
<text x="36" y="218" font-size="14" font-weight="700" fill="var(--text)">5  Session</text>
<text x="36" y="236" font-size="12" fill="var(--text-muted)">sessions, sockets, RPC</text>
<rect x="20" y="252" width="250" height="54" rx="10" fill="var(--success)" fill-opacity=".14" stroke="var(--success)" stroke-width="1.6"/>
<text x="36" y="276" font-size="14" font-weight="700" fill="var(--text)">4  Transport</text>
<text x="36" y="294" font-size="12" fill="var(--text-muted)">TCP, UDP, QUIC</text>
<rect x="20" y="310" width="250" height="54" rx="10" fill="var(--accent)" fill-opacity=".14" stroke="var(--accent)" stroke-width="1.6"/>
<text x="36" y="334" font-size="14" font-weight="700" fill="var(--text)">3  Network</text>
<text x="36" y="352" font-size="12" fill="var(--text-muted)">IP, ICMP, routing</text>
<rect x="20" y="368" width="250" height="54" rx="10" fill="#8b5cf6" fill-opacity=".14" stroke="#8b5cf6" stroke-width="1.6"/>
<text x="36" y="392" font-size="14" font-weight="700" fill="var(--text)">2  Data link</text>
<text x="36" y="410" font-size="12" fill="var(--text-muted)">Ethernet, Wi-Fi, ARP</text>
<rect x="20" y="426" width="250" height="54" rx="10" fill="#8b5cf6" fill-opacity=".14" stroke="#8b5cf6" stroke-width="1.6"/>
<text x="36" y="450" font-size="14" font-weight="700" fill="var(--text)">1  Physical</text>
<text x="36" y="468" font-size="12" fill="var(--text-muted)">cable, fibre, radio, bits</text>
<rect x="290" y="78" width="190" height="170" rx="10" fill="var(--primary)" fill-opacity=".22" stroke="var(--primary)" stroke-width="2"/>
<text x="385" y="159.0" font-size="15" font-weight="700" text-anchor="middle" fill="var(--text)">Application</text>
<text x="385" y="177.0" font-size="11.5" text-anchor="middle" fill="var(--text-muted)">data / message</text>
<line x1="270" y1="163.0" x2="290" y2="163.0" stroke="var(--primary)" stroke-width="2"/>
<rect x="290" y="252" width="190" height="54" rx="10" fill="var(--success)" fill-opacity=".22" stroke="var(--success)" stroke-width="2"/>
<text x="385" y="275.0" font-size="15" font-weight="700" text-anchor="middle" fill="var(--text)">Transport</text>
<text x="385" y="293.0" font-size="11.5" text-anchor="middle" fill="var(--text-muted)">segment (TCP) · datagram (UDP)</text>
<line x1="270" y1="279.0" x2="290" y2="279.0" stroke="var(--success)" stroke-width="2"/>
<rect x="290" y="310" width="190" height="54" rx="10" fill="var(--accent)" fill-opacity=".22" stroke="var(--accent)" stroke-width="2"/>
<text x="385" y="333.0" font-size="15" font-weight="700" text-anchor="middle" fill="var(--text)">Internet</text>
<text x="385" y="351.0" font-size="11.5" text-anchor="middle" fill="var(--text-muted)">packet</text>
<line x1="270" y1="337.0" x2="290" y2="337.0" stroke="var(--accent)" stroke-width="2"/>
<rect x="290" y="368" width="190" height="112" rx="10" fill="#8b5cf6" fill-opacity=".22" stroke="#8b5cf6" stroke-width="2"/>
<text x="385" y="420.0" font-size="15" font-weight="700" text-anchor="middle" fill="var(--text)">Link</text>
<text x="385" y="438.0" font-size="11.5" text-anchor="middle" fill="var(--text-muted)">frame → bits</text>
<line x1="270" y1="424.0" x2="290" y2="424.0" stroke="#8b5cf6" stroke-width="2"/>
<rect x="500" y="86" width="360" height="154" rx="6" fill="var(--primary)" fill-opacity=".16" stroke="var(--primary)" stroke-width="1.6"/>
<text x="680.0" y="167.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">HTTP data (request or response)</text>
<rect x="500" y="260" width="70" height="38" rx="6" fill="var(--success)" fill-opacity=".55" stroke="var(--success)" stroke-width="1.6"/>
<text x="535.0" y="283.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">TCP hdr</text>
<rect x="570" y="260" width="290" height="38" rx="6" fill="var(--primary)" fill-opacity=".16" stroke="var(--primary)" stroke-width="1.6"/>
<text x="715.0" y="283.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">HTTP data</text>
<rect x="500" y="318" width="62" height="38" rx="6" fill="var(--accent)" fill-opacity=".55" stroke="var(--accent)" stroke-width="1.6"/>
<text x="531.0" y="341.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">IP hdr</text>
<rect x="562" y="318" width="70" height="38" rx="6" fill="var(--success)" fill-opacity=".55" stroke="var(--success)" stroke-width="1.6"/>
<text x="597.0" y="341.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">TCP hdr</text>
<rect x="632" y="318" width="228" height="38" rx="6" fill="var(--primary)" fill-opacity=".16" stroke="var(--primary)" stroke-width="1.6"/>
<text x="746.0" y="341.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">HTTP data</text>
<rect x="500" y="376" width="58" height="96" rx="6" fill="#8b5cf6" fill-opacity=".55" stroke="#8b5cf6" stroke-width="1.6"/>
<text x="529.0" y="428.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">Eth hdr</text>
<rect x="558" y="376" width="52" height="96" rx="6" fill="var(--accent)" fill-opacity=".55" stroke="var(--accent)" stroke-width="1.6"/>
<text x="584.0" y="428.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">IP hdr</text>
<rect x="610" y="376" width="60" height="96" rx="6" fill="var(--success)" fill-opacity=".55" stroke="var(--success)" stroke-width="1.6"/>
<text x="640.0" y="428.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">TCP hdr</text>
<rect x="670" y="376" width="130" height="96" rx="6" fill="var(--primary)" fill-opacity=".16" stroke="var(--primary)" stroke-width="1.6"/>
<text x="735.0" y="428.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">HTTP data</text>
<rect x="800" y="376" width="60" height="96" rx="6" fill="#8b5cf6" fill-opacity=".55" stroke="#8b5cf6" stroke-width="1.6"/>
<text x="830.0" y="428.5" font-size="12" font-weight="600" text-anchor="middle" fill="var(--text)">FCS</text>
<text x="500" y="478" font-size="11.5" fill="var(--text-muted)"> </text>
<line x1="874" y1="78" x2="874" y2="480" stroke="var(--text-muted)" stroke-width="1.6" marker-end="url(#osiar)"/>
<text transform="translate(892 279.0) rotate(-90)" font-size="11.5" text-anchor="middle" fill="var(--text-muted)">sending: each layer wraps the data below it</text>
<text x="20" y="514" font-size="13" font-weight="700" fill="var(--text)">How each layer finds its target</text>
<rect x="20" y="524" width="205" height="44" rx="10" fill="var(--primary)" fill-opacity=".14" stroke="var(--primary)" stroke-width="1.6"/>
<text x="122.5" y="543" font-size="12.5" font-weight="700" text-anchor="middle" fill="var(--text)">Application</text>
<text x="122.5" y="559" font-size="12" text-anchor="middle" fill="var(--text-muted)">URL, domain name</text>
<rect x="238" y="524" width="205" height="44" rx="10" fill="var(--success)" fill-opacity=".14" stroke="var(--success)" stroke-width="1.6"/>
<text x="340.5" y="543" font-size="12.5" font-weight="700" text-anchor="middle" fill="var(--text)">Transport</text>
<text x="340.5" y="559" font-size="12" text-anchor="middle" fill="var(--text-muted)">port number</text>
<rect x="456" y="524" width="205" height="44" rx="10" fill="var(--accent)" fill-opacity=".14" stroke="var(--accent)" stroke-width="1.6"/>
<text x="558.5" y="543" font-size="12.5" font-weight="700" text-anchor="middle" fill="var(--text)">Internet</text>
<text x="558.5" y="559" font-size="12" text-anchor="middle" fill="var(--text-muted)">IP address</text>
<rect x="674" y="524" width="205" height="44" rx="10" fill="#8b5cf6" fill-opacity=".14" stroke="#8b5cf6" stroke-width="1.6"/>
<text x="776.5" y="543" font-size="12.5" font-weight="700" text-anchor="middle" fill="var(--text)">Link</text>
<text x="776.5" y="559" font-size="12" text-anchor="middle" fill="var(--text-muted)">MAC address</text>
</svg>
</div>

*Reading it left to right: the OSI layers 7–5 collapse into TCP/IP's Application layer and OSI layers 2–1 into its Link layer. On the way down each layer wraps what it receives in its own header (and the link layer adds a trailer); on the way up the receiver strips them in reverse order.*

### A DNS resolution chain for `www.example.com`

```mermaid
sequenceDiagram
    participant B as Browser / OS stub
    participant R as Recursive resolver (ISP / 1.1.1.1)
    participant Root as Root server
    participant TLD as .com TLD server
    participant Auth as example.com authoritative
    B->>R: A? www.example.com
    Note over R: cache miss
    R->>Root: A? www.example.com
    Root-->>R: ask .com servers (NS)
    R->>TLD: A? www.example.com
    TLD-->>R: ask ns1.example.com (NS)
    R->>Auth: A? www.example.com
    Auth-->>R: 93.184.215.14, TTL 300
    R-->>B: 93.184.215.14 (cached for 300 s)
```

### A NAT table mapping private → public

```mermaid
flowchart LR
    subgraph home["home network 192.168.1.0/24"]
        l["laptop<br/>192.168.1.10:51000"]
        p["phone<br/>192.168.1.23:51000"]
    end
    l --> nat["NAT<br/>router public IP 203.0.113.7"]
    p --> nat
    nat --> net(("internet"))
```

### NAT table

| inside | outside | remote |
|---|---|---|
| `192.168.1.10:51000` | `203.0.113.7:40001` | `142.250.1.1:443` |
| `192.168.1.23:51000` | `203.0.113.7:40002` | `142.250.1.1:443` |

---

## Example

```bash
dig example.com A +short                 # 93.184.215.14
dig www.github.com +trace                # walk root → .com → github.com yourself
dig example.com MX
ip addr; ip route                        # your addresses; the default gateway
ss -tn state established                 # live TCP 4-tuples
curl -v https://example.com 2>&1 | head  # DNS → TCP connect → TLS → HTTP in one view
```

```python
import ipaddress
net = ipaddress.ip_network("192.168.1.0/24")
print(net.num_addresses, net.network_address, net.broadcast_address)   # 256 192.168.1.0 192.168.1.255
hosts = list(net.hosts()); print(hosts[0], hosts[-1], len(hosts))      # 192.168.1.1 192.168.1.254 254
for sub in net.subnets(new_prefix=26):                                  # four /26 subnets
    print(sub, "hosts:", sub.num_addresses - 2)
print(ipaddress.ip_address("10.3.4.5").is_private)                      # True

import socket
print(socket.getaddrinfo("example.com", 443, proto=socket.IPPROTO_TCP)[0][4])
```

---

## Exercises

1. Explain what happens between typing a URL and page load (DNS → TCP → TLS → HTTP).

   <details><summary>Solution</summary>(1) The browser parses the URL and checks its caches and HSTS. (2) DNS: browser/OS cache → recursive resolver → root → TLD → authoritative, returning an IP. (3) TCP 3-way handshake to IP:443 (or QUIC over UDP). (4) The TLS handshake verifies the certificate chain and agrees keys. (5) An HTTP request is sent, possibly through a CDN or load balancer. (6) The server responds; the browser parses HTML, discovers CSS/JS/images (more requests, often reusing the connection), builds DOM and CSSOM, lays out, and paints.</details>

2. Subnet a /24 and pick valid hosts.

   <details><summary>Solution</summary><code>10.0.5.0/24</code> into four /26s: <code>.0/26</code> (hosts .1–.62), <code>.64/26</code> (.65–.126), <code>.128/26</code> (.129–.190), <code>.192/26</code> (.193–.254). Each has 62 usable hosts: 64 minus the network and broadcast addresses.</details>

3. Why does `ping` work but `curl` to port 443 time out?

   <details><summary>Solution</summary>ICMP reaches the host, but TCP 443 is blocked (firewall or security group), nothing listens (that would be "connection refused", not a timeout), or a middlebox drops it. Check with <code>nc -vz host 443</code> and <code>ss -tlnp</code> on the server.</details>

---

## Mini project

### A small DNS client that resolves A/AAAA records over UDP

```mermaid
flowchart LR
    Q["build query:<br/>12-byte header (id, flags RD=1, qdcount=1)<br/>+ QNAME 3www7example3com0 + QTYPE + QCLASS"] --> S["UDP sendto 1.1.1.1:53"] --> R["recv ≤ 512 bytes"] --> P["parse header, skip the question,<br/>parse answers (handle name compression 0xC0 pointers)"] --> O["print: name TTL type address"]
```

### Steps

1. Encode the query with `struct.pack("!HHHHHH", id, 0x0100, 1, 0, 0, 0)` plus labels.
2. Send over UDP with a 2-second timeout; retry once.
3. Parse answers: type, class, TTL, rdlength, rdata; decode A (4 bytes) and AAAA (16 bytes) with `ipaddress`.
4. Handle compressed names (pointers starting with bits `11`) and CNAME chains.
5. Compare the output with `dig +short` for 10 domains.

**Done when:** your client matches `dig` for A, AAAA, and CNAME-chained names, and handles a timeout cleanly.

---

## Open source

* [`miekg/dns`](https://github.com/miekg/dns) — a complete DNS library in Go (used by CoreDNS); `msg.go` shows wire-format packing and name compression.
* [`curl/curl`](https://github.com/curl/curl) — `curl -v` and `--trace-time` show each phase of a connection; `lib/connect.c` implements Happy Eyeballs (racing IPv4 and IPv6).

---

## Interview

1. **"Walk me through DNS resolution."**
   <details><summary>Answer</summary>The app asks the OS stub resolver, which checks its cache and <code>/etc/hosts</code>, then asks a recursive resolver. On a miss, the resolver asks a root server (which refers it to the TLD), the TLD server (which refers it to the domain's authoritative servers), and the authoritative server, which returns the record with a TTL. Each layer caches answers for the TTL, which is why DNS changes take time to propagate.</details>

2. **"What does NAT solve (and not solve)?"**
   <details><summary>Answer</summary>It solves IPv4 scarcity: many private hosts share one public IP. As a side effect it hides internal topology and drops unsolicited inbound packets. It does not provide real security (use a firewall), breaks end-to-end connectivity (peer-to-peer and inbound services need port forwarding or STUN/TURN), and makes per-user rate limiting and logging harder. IPv6 removes the need for it.</details>

---

## Checklist

- [ ] name each layer's job
- [ ] resolve DNS by hand
- [ ] explain port exhaustion

---

> [Contents](index.md) · ← [Chapter 39 — OS: Memory Management, File Systems, System Calls & IPC](ch39-os-memory-management-file-systems-system-calls.md) · Next → [Chapter 41 — Transport & Security: TCP, UDP, QUIC, TLS & HTTPS](ch41-transport-and-security-tcp-udp-quic-tls.md)

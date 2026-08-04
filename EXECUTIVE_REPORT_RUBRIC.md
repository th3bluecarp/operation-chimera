# Incident Case: Operation Chimera (NIGHTMARE DIFFICULTY): Executive Report Rubric

## Scenario-specific required conclusions

Validated against the repository artifacts in operation-chimera.

## 1. Initial access

The attacker exploited an SSRF vulnerability in /api/v2/webhook/fetch. The Flask endpoint accepts an arbitrary URL and passes it directly to requests.get() without restricting link-local or metadata addresses.

The attacker requested:

http://169.254.169.254/latest/meta-data/iam/security-credentials/web-ec2-role

This exposed temporary credentials for the instance role arn:aws:iam::111122223333:role/web-ec2-role. The evidence does not include a literal access-key secret; the stolen access was the temporary EC2-role credentials obtained through the metadata service.

## 2. Evasion

Persistence/evasion used /usr/local/lib/libprocesshider.so through /etc/ld.so.preload. That preload library hides processes from normal tools such as ps and netstat.

The hidden C2 process is PID 1460, confirmed by proc_maps_dump.txt showing /memfd:kworker (deleted) and syslog memfd execution events.

## 3. Lateral movement

The attacker used chisel to create a reverse tunnel from the compromised web server to 192.0.2.55:443. The recovered remotes entry R:10.0.5.50:5432 exposed the isolated PostgreSQL service through the attacker-controlled relay.

## 4. Data exfiltration

The attacker did not download database files directly over the internet. They used the stolen web-ec2-role access to assume arn:aws:iam::111122223333:role/db-admin-cross-account, created an EBS snapshot of vol-00001111222233334, then used ModifySnapshotAttribute to grant access to external AWS account 999988887777.

Snapshot ID: snap-0abcd1234efgh5678.

## Timeline

- 08:15:10 — SSRF endpoint tested
- 08:16:22 — EC2 metadata endpoint probed
- 08:17:05 — IAM-role metadata successfully fetched
- 08:18:10 — Cross-account role assumed
- 08:26:01 — Payload persistence executed as www-data
- 08:27:10–08:27:12 — memfd/process-hider activity
- 08:35:00 — EBS snapshot created
- 08:38:15 — Snapshot shared with account 999988887777

## Compact answer key

1. SSRF to EC2 metadata; temporary web-ec2-role credentials.
2. /etc/ld.so.preload plus libprocesshider.so; hidden PID 1460.
3. Reverse chisel tunnel to PostgreSQL 10.0.5.50:5432.
4. Cross-account EBS snapshot exfiltration to account 999988887777.

## False signals and non-primary evidence

- The 08:14:02 GET to /api/v2/status from 10.0.1.20 is a normal Datadog health check, not attacker reconnaissance.
- The 08:15:10 webhook request for https://example.com/hook is a harmless feature probe and does not touch metadata or internal services.
- The 08:16:22 metadata request returns HTTP 500. It is an unsuccessful precursor/probe, not proof that credentials were obtained. The successful credential retrieval is the 08:17:05 request.
- The 08:18:00 Datadog status check is another benign monitoring event.
- The 08:26:05 apt-get update run by www-data is suspicious and part of post-compromise activity, but it is not itself the initial access mechanism or the exfiltration step.
- The AppArmor event says ALLOWED, not DENIED. It is evidence that the memfd payload executed under an unconfined profile, not evidence that AppArmor stopped the attacker.
- Zeek C1 is the initial outbound HTTP callback and C2 is the long-lived TLS connection. The two database connections are not separate initial compromises: they are the tunneled database transfer, with byte direction distinguishing database response traffic from command/query traffic.
- The 08:15 example.com URL and the external relay IP 192.0.2.55 are infrastructure clues. The challenge's decisive cloud evidence is the STS role assumption followed by snapshot creation and sharing.

## Scoring

- 30% accurate, normalized timeline with artifact citations
- 25% complete entry, pivot, persistence, privilege, and impact analysis
- 20% correct clustering of related, unrelated, benign, and false-signal activity
- 15% disciplined confidence labels and treatment of telemetry gaps
- 10% executive-quality remediation, ownership, and sequencing

## Automatic deductions

- Unsupported attribution or invented observables
- Collapsing every suspicious event into a single incident
- Treating attempted access as successful access
- Treating access as exfiltration without transfer or receipt evidence
- Treating missing logs as proof that activity did not occur
- Omitting material contradictory or benign evidence

Every high-impact conclusion should cite two independent artifacts where available and preserve exact identities, hosts, IP addresses, object names, and timestamps.

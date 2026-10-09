# STAGE-04: Linux System Security & Cron Persistence

## Overview
- **Domain:** Linux / System Security[cite: 3]
- **Difficulty:** Moderate
- **Points:** 100
- **Flag Format:** `CTF{[a-z0-9_]+}`[cite: 3]
- **Dependencies:** None (standalone stage)[cite: 3]

## Challenge Description
An internal system monitor flagged anomalous minutely script executions under a low-privilege account on the Nexora staging server.

Participants are granted SSH access as user `player` to investigate scheduled cron tasks, locate a suspicious system backup script, and discover the persistence mechanism and exfiltration endpoint (`exfil.nexora-logistics.lk:8443`).

## Challenge Files
- `SSH Connection`: Port `2222` on target VM `192.168.56.20` (`ssh player@192.168.56.20 -p 2222`)[cite: 1, 3]
- `/usr/local/bin/backup.sh`: Suspect persistence backup script executed via cron.[cite: 3]

## Solution Walkthrough
1. Connect to target container via SSH on port 2222 (`player:player123`).[cite: 3]
2. Inspect scheduled tasks using `crontab -l` or active process trees.[cite: 3]
3. Discover scheduled script executing minutely at `/usr/local/bin/backup.sh`.[cite: 3]
4. Inspect the contents of `/usr/local/bin/backup.sh`.[cite: 3]
5. Identify exfiltration callback endpoint `exfil.nexora-logistics.lk:8443` and Stage 4 flag comment.[cite: 3]
6. Confirm and record flag string.[cite: 3]
7. **Flag:** `CTF{cr0n_j0b_p3rs1st3nc3_d3t3ct3d}`[cite: 3]
   - **SHA-256 Hash of the flag:** `49454b3725994e5bb29158ce6f84f16d2ed14187cda43c4e6e3a088e53fdb186`[cite: 3]
   - **SHA-256 Checksum of the final artifact(s):** N/A (Dynamic Container Service)[cite: 3]

## How It Was Built
1. **Base Component:** Initialized container from `ubuntu:22.04` base image installing `openssh-server` and `cron`.[cite: 3]
2. **Payload / Persistence / Content:** Authored `/usr/local/bin/backup.sh` containing callback domain and flag string.[cite: 3]
3. **Configuration / Embedding:** Configured SSH daemon to listen on port 2222 and created user `player`.[cite: 3]
4. **Integration / Obfuscation:** Installed minutely cron job (`* * * * * /usr/local/bin/backup.sh`) under user `player`.[cite: 3]
5. **Clean up:** Purged apt caching layers and temporary build files from image layers.[cite: 3]
6. **Verify:** Deployed container via `docker compose up -d` and verified automated SSH extraction using `solve_stage4.py`.[cite: 3]

**Why the order matters:** SSH configuration and script placement must occur before defining cron entrypoints in Dockerfile.[cite: 3]

> **Warning:** Restarting container resets runtime `/tmp/backup.log` entries.[cite: 3]

## Hints

| Hint | Cost | Text |
| :--- | :--- | :--- |
| **Hint 1** | Free | "Check crontab listings or inspect binary paths under /usr/local/bin/." |
| **Hint 2** | -5 points | "Examine header comments in /usr/local/bin/backup.sh for callback domain details." |

## Reset / Recovery
Dynamic Docker container. Redeploy or restart using `docker compose restart stage4-linux` on host server.[cite: 3]

## Validation and Anti-Shortcut Checks
- The flag is submitted through the CTFd submission field and validated against server-side SHA-256 matching.[cite: 3]
- System permissions prevent user `player` from modifying `/usr/local/bin/backup.sh` while keeping execution readable.[cite: 3]
- Isolated container environment prevents unauthorized breakout to host VM.[cite: 3]

## Changes From the Assignment 01 Design
- **Port Mapping:** Mapped internal SSH service to port 2222 to avoid host port 22 conflicts.[cite: 3]
- **Script Location:** Standardized script placement to `/usr/local/bin/backup.sh`.[cite: 3]

## Tools and Resources Acknowledged
- Docker & Docker Compose[cite: 3]
- OpenSSH Server & Cron Service[cite: 3]
- Python `paramiko` SSH library[cite: 3]
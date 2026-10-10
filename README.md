# The Insider's Trail: CTF Play Box

**Module:** IE3132 Penetration Testing, SLIIT (Year 3, Semester 1, 2026)
**Group:** Y3.S1.WD.CS.02.01, Group 18

A six-stage Capture The Flag box built around an insider-threat investigation at the fictional company *Nexora Logistics Group*. 
Participants act as DFIR analysts investigating a resigned engineer suspected of data exfiltration and of leaving a backdoor. 
The box runs in an isolated lab network and is hosted on CTFd.

## Team
| Student ID | Member | Role | 
|---|---|---|
| IT24103991 | Siriwardana A.W.T.B. | Member 1: Platform and Architecture |
| IT24103820 | Maldeniya A.T. | Member 2: Challenge Design A (Stages 1, 3, 5) | 
| IT24102560 | Nirmana A.A.H. | Member 3: Challenge Design B (Stages 2, 4, 6) | 
| IT24610817 | Gunasena B.R.S. | Member 4: Integration, Testing and Documentation |

## Challenges
| Stage | Domain | Difficulty |
|---|---|---|
| 1 | Cryptography (Vigenère) | Easy |
| 2 | OSINT | Easy |
| 3 | Steganography | Moderate |
| 4 | Linux / System Security | Moderate |
| 5 | Digital Forensics | Moderate-Hard |
| 6 | Correlation (capstone) | Hard |

Each stage folder has its own README with the description, solution path, build notes, hints and reset notes. 
Stages 1, 2, 3 and 5 are static file challenges served through CTFd. Stage 4 is an SSH-accessible Docker container (port 2222). 
Stage 6 is a Flask correlation service (port 5000) that needs evidence from Stages 1 to 5. Point values are set in CTFd.

## Repository layout
- `Platform/` : Docker Compose project for CTFd and MariaDB, with the platform README
- `Stage1-Cryptography/`, `Stage3-Steganography/`, `Stage5-Digital-Forensics/` : Challenge Design A
- `Stage2-OSINT/`, `Stage4-Linux/`, `Stage6-Correlation/` : Challenge Design B
- `Solver/` : Centralized directory containing each member's LO3 automation, exploit, and verification scripts
  - `Member1_IT24103991/` : Platform health and deployment verification script
  - `Member2_IT24103820/` : Automated solver for Stages 1, 3, and 5
  - `Member3_IT24102560/` : Stage solvers for Stages 2, 4, and 6
  - `Member4_IT24610817/` : End-to-end verification and QA testing suite
- `testing/` : Test matrices, defect logs, and validation evidence

## Architecture
| Machine | Role | Address |
|---|---|---|
| Ubuntu Server 24.04.4 LTS VM | Host for Docker, CTFd, MariaDB and the challenge containers | 192.168.56.20 |
| Kali Linux VM | Participant workstation | 192.168.56.10 |

* Both VMs have a NAT adapter (internet access for installing software) and a **Host-Only** adapter on 192.168.56.0/24 with static addresses.
* CTFd 3.7.5 is published only on the host-only address (`192.168.56.20:8000`), so it is not exposed on the NAT side.
* MariaDB 10.11 sits on an internal-only Docker network, so only CTFd can reach it.
* CTFd runs as a non-root user (UID 1001).
* Secrets live in `.env`, which is never committed (copy `.env.example`).

## Setup
1. Create the Ubuntu Server and Kali VMs in VirtualBox. Give each a NAT adapter (Adapter 1) and a Host-Only adapter (Adapter 2). 
  Set the static host-only addresses above (see the platform README for the netplan and nmcli steps). Check with `ping -c 3 192.168.56.20` from Kali.
2. On the Ubuntu VM, install Docker Engine and the Compose plugin from Docker's apt repository, then add your user to the `docker` group.
3. Clone this repository on the Ubuntu VM and start the platform:
```bash
   cd Platform
   mkdir -p data/uploads data/logs data/ctfd_data data/mysql
   sudo chown -R 1001:1001 data/uploads data/logs data/ctfd_data
   cp .env.example .env        # then replace the placeholder values
   docker compose up -d
   docker compose ps
   curl -I http://192.168.56.20:8000
```
   Both containers should be up (the database healthy), and the `curl` should return a redirect to `/setup`.
4. From the Kali VM, open `http://192.168.56.20:8000/setup`, enter the event name *The Insider's Trail* and create the admin account.
5. In the CTFd admin panel, add each challenge using the values in its stage README (name, category, points, description, hints, files and flag).
6. Start the Stage 4 container and the Stage 6 service as described in their stage READMEs.

## Flags and validation
* Flag format: `CTF{[a-z0-9_]+}` (lowercase snake_case).
* Each flag is configured in CTFd as a static, case-sensitive flag. CTFd compares the submitted text with the stored flag using an exact string comparison.
* SHA-256 hashes of the flags and challenge files are used by the team for verification (see the testing report). 
  They are not used by CTFd to validate submissions.

## Reset and recovery
* **Static stages (1, 2, 3, 5):** no reset is needed. Participants re-download the original files from CTFd, and the checksums in each stage README confirm that the files are unchanged.
* **Stage 4:** recreate the container from its image to discard all changes made during an attempt: `docker compose up -d --force-recreate stage4-linux`.
* **Stage 6:** the service keeps no player state, so restarting it (`docker compose restart stage6-correlation`) restores it.
* **Platform:** `docker compose down` then `docker compose up -d` restarts CTFd and MariaDB. Platform data is kept in `Platform/data/`.

## Changes from the Assignment 01 design
* **Platform:** Ubuntu Server 24.04.4 LTS instead of 22.04, CTFd 3.7.5 instead of 3.8.x, no Redis (CTFd uses its filesystem cache),
  and a 30 GB disk instead of 25 GB.
* **Flag validation:** CTFd uses exact string comparison, not SHA-256 matching as Assignment 01 stated.
* **Stage 3:** the Base64 passphrase string in Assignment 01 was incorrect and was corrected (`TjFHSFRfRFIxVjNfMjAyNg==`). See the Stage 3 README.
* **Stage 5:** 100 KB of padding was added after the hidden ZIP so that `unzip` cannot open `chat_export.txt` directly. See the Stage 5 README.
* **Stage 2, 4 and 6:** see the "Changes" section of each stage README.

## Tools and resources acknowledged
CTFd, Docker and Docker Compose, MariaDB, Flask, VirtualBox, Ubuntu Server, Kali Linux, CyberChef, dcode.fr, ExifTool, Steghide, 
ImageMagick, binwalk, foremost, xxd, zip/unzip, OpenSSH, cron, Python 3.

# STAGE-06: Incident Correlation & Capstone Portal

## Overview
- **Domain:** Multi-Domain Correlation[cite: 3]
- **Difficulty:** Hard
- **Points:** 150
- **Flag Format:** `CTF{[a-z0-9_]+}`[cite: 3]
- **Dependencies:** Requires inputs from Stages 1–5[cite: 3]

## Challenge Description
Security operations have recovered access to the central Nexora Incident Correlation Portal.

To finalize the investigation and unlock the capstone flag, analysts must correlate all Indicators of Compromise (IOCs), passphrases, and artifacts recovered across Stages 1 through 5, submitting them to the Flask validation backend (`app.py`).

## Challenge Files
- `HTTP Web Link`: `http://192.168.56.20:5000` (Flask Web Correlation Portal)[cite: 1, 3]
- `Stage6-Correlation/app.py`: Backend Flask application handling endpoint requests.[cite: 3]

## Solution Walkthrough
1. Access Incident Correlation Portal interface at `http://192.168.56.20:5000`.[cite: 1, 3]
2. Gather evidence tokens from Stages 1–5 (`NIGHTHAWK`, `ghostwire_lk`, `N1GHT_DR1V3_2026`, `exfil.nexora-logistics.lk:8443`, `RevokeAccess2026`).[cite: 3]
3. Construct JSON payload or web form submission with all 5 evidence keys (`clue1` through `clue5`).[cite: 3]
4. Submit request to `/correlate` endpoint.[cite: 3]
5. Receive success JSON response containing the capstone flag.[cite: 3]
6. Confirm and submit capstone flag string.[cite: 3]
7. **Flag:** `CTF{1nc1d3nt_c0rr3l4t10n_m4st3r_2026}`[cite: 3]
   - **SHA-256 Hash of the flag:** `c33fd93ea6373e9b5b8adb61b3c94f9262ca147c8d664c9be62cad107d822038`[cite: 3]
   - **SHA-256 Checksum of the final artifact(s):** N/A (Dynamic Web Service)[cite: 3]

## How It Was Built
1. **Base Component:** Developed Python Flask application (`app.py`) with `render_template` index portal.[cite: 3]
2. **Payload / Persistence / Content:** Configured `CORRECT_EVIDENCE` validation map and defined `CAPSTONE_FLAG`.[cite: 3]
3. **Configuration / Embedding:** Implemented strict token matching and 400 error handling on `/correlate` route.[cite: 3]
4. **Integration / Obfuscation:** Bound Flask app to host `0.0.0.0` on port 5000 for network accessibility.[cite: 3]
5. **Clean up:** Standardized JSON error response messages.[cite: 3]
6. **Verify:** Executed `solve_stage6.py` automated POST request to verify token validation pipeline.[cite: 3]

**Why the order matters:** Evidence tokens must match exact output values from prior stages before capstone deployment.[cite: 3]

> **Warning:** Submitting incomplete or partial evidence payloads will trigger HTTP 400 validation errors.[cite: 3]

## Hints

| Hint | Cost | Text |
| :--- | :--- | :--- |
| **Hint 1** | Free | "Ensure you have gathered tokens from all 5 preceding investigation stages." |
| **Hint 2** | -5 points | "Verify clue4 callback domain from Stage 4 and clue5 password from Stage 5." |

## Reset / Recovery
Dynamic Flask web service. Restart container using `docker compose restart stage6-correlation` on host server.[cite: 3]

## Validation and Anti-Shortcut Checks
- The flag is submitted through the CTFd submission field and validated against server-side SHA-256 matching.[cite: 3]
- Backend validates all 5 evidence keys simultaneously preventing single-token brute-forcing.[cite: 3]
- Input values are sanitized with `.strip()` to prevent accidental formatting failures.[cite: 3]

## Changes From the Assignment 01 Design
- **Validation Rigor:** Added explicit whitespace stripping (`.strip()`) to prevent input formatting mismatches.[cite: 3]
- **Endpoint Handling:** Enhanced error response clarity on incomplete token submissions.[cite: 3]

## Tools and Resources Acknowledged
- Python 3 & Flask Web Framework[cite: 3]
- Docker & Docker Compose[cite: 3]
- Python `requests` library[cite: 3]

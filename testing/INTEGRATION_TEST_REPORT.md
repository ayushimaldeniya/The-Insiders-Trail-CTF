# Integration & End-to-End Testing Report
**Project Name:** The Insider's Trail CTF  
**Assigned Tester / QA Lead:** Member 4 — Gunasena B.R.S. (IT24610817)  
**Assigned Role:** Integration Testing, Defect Resolution, Unintended-Solution Checks & Platform Validation  
**Environment:** Kali Linux VM (`192.168.56.10/24`) -> Target Server (`192.168.56.20/24`)  
**Date of Testing:** October 2026  
**Status:** All 6 Stages Fully Verified & Approved  

---

## 1. Executive Summary
This document provides the formal validation records for **The Insider's Trail CTF** platform. As Member 4, the primary responsibilities are:
1. Validating end-to-end challenge flow across all 6 stages.
2. Building and maintaining the **Flag Verification Matrix** and **Artifact Integrity Checksums**.
3. Documenting defects found during integration and verifying their resolutions.
4. Performing **Unintended-Solution Checks (Shortcut Testing - Requirement 7)** to prevent trivial bypasses.
5. Verifying **State Reset and Recovery Procedures (Requirement 5)** for both static challenges and live containerized environments.

---

## 2. End-to-End Validation & Flag Verification Matrix

### 2.1 Flag Verification Matrix (All 6 Stages)
Every flag extracted from the official solution path was hashed using SHA-256 (with trailing newlines stripped via `echo -n` or raw byte encoding). The calculated hashes were verified against the approved challenge designs.

| Stage ID | Stage Name & Domain | Extracted Flag String | Approved Design SHA-256 Hash | Calculated SHA-256 Hash | Points | Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **STG-01** | **The Farewell Message**<br>*(Cryptography - Vigenère)* | `CTF{v1g3ner3_c1p3r_cr4ck3d}` | `06fc482694c85e8cf6ea5ab7edbc397878cadc14303262c83327cc5d6abe24ae` | `06fc482694c85e8cf6ea5ab7edbc397878cadc14303262c83327cc5d6abe24ae` | 50 | **PASS** |
| **STG-02** | **Tracing the Ghost**<br>*(OSINT / Metadata Recon)* | `CTF{0s1nt_tr4c1ng_th3_gh0st}` | `72f37e7253fa4247b8d59320874f27f339f38913d1ce2b87333207a46182a7c5` | `72f37e7253fa4247b8d59320874f27f339f38913d1ce2b87333207a46182a7c5` | 100 | **PASS** |
| **STG-03** | **Nostalgia**<br>*(Steganography - Steghide)* | `CTF{p1x3ls_h4v3_s3cr3ts}` | `864d140e3e97f74894eb8524da7e511f40685820453d966f11dfd4645fd3f80c` | `864d140e3e97f74894eb8524da7e511f40685820453d966f11dfd4645fd3f80c` | 100 | **PASS** |
| **STG-04** | **Ghost in the Cron**<br>*(Linux Persistence / SSH)* | `CTF{cr0n_j0b_p3rs1st3nc3_d3t3ct3d}` | `49454b3725994e5bb29158ce6f84f16d2ed14187cda43c4e6e3a088e53fdb186` | `49454b3725994e5bb29158ce6f84f16d2ed14187cda43c4e6e3a088e53fdb186` | 150 | **PASS** |
| **STG-05** | **The Appended Archive**<br>*(Digital Forensics / Carving)*| `CTF{f1l3_c4rv1ng_p4st_th3_30f}` | `e5f3a00e0111eb63400dd117a61112204f886991fef0030679819e0d3867ba25` | `e5f3a00e0111eb63400dd117a61112204f886991fef0030679819e0d3867ba25` | 150 | **PASS** |
| **STG-06** | **Incident Correlation Master**<br>*(Capstone Correlation)* | `CTF{1nc1d3nt_c0rr3l4t10n_m4st3r_2026}` | `c33fd93ea6373e9b5b8adb61b3c94f9262ca147c8d664c9be62cad107d822038` | `c33fd93ea6373e9b5b8adb61b3c94f9262ca147c8d664c9be62cad107d822038` | 200 | **PASS** |

---

### 2.2 Artifact Integrity Checksums (In-Transit Validation)
To ensure that challenge files served via the CTFd platform or downloaded by participants do not suffer corruption or alterations during transit:

| File Name | Stage Association | Expected SHA-256 Hash | Verified Status |
| :--- | :--- | :--- | :---: |
| `office_party.jpg` | Stage 3 (Carrier Image) | `a49c10a258e35a4c48eb35d45f268731cc7e894a66456ef41830a3adc5eacc03` | **VERIFIED** |
| `chat_export.txt` | Stage 5 (Forensic Text Carrier) | `286064cfe8b8424e72cd4b6cda4bc8554ddb3cfec9ceb13f992586b461875211` | **VERIFIED** |
| `it_handover_notes.txt` | Stage 5 (Handover Memo) | `bc77d76c24baf82ee56cedfde668204cd7a4342d1016f30b0931706f4d9b3ab9` | **VERIFIED** |

---

## 3. Defect Discovery & Resolution Log

During the integration and review of branches submitted by Members 2 and 3, Member 4 identified critical defects and coordinated with the authors to apply technical resolutions prior to merge:

| Defect ID | Stage | Severity | Defect Description | Root Cause | Technical Resolution & Verification |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DEF-01** | Stage 3 | **High** | The Base64 string in the initial Assignment 01 documentation was given as `TDFHSE1fRFIxdjNfMjAyNg==`. When decoded, this produced `L1GHM_DR1v3_2026`, which failed Steghide authentication. | Transposition typos during manual Base64 generation in initial drafting. | Re-encoded the correct key `N1GHT_DR1V3_2026` to `TjFHSFRfRFIxVjNfMjAyNg==`. Embedded into the EXIF `Comment` header using `exiftool`. Tested extraction on Kali: Steghide now unlocks cleanly. |
| **DEF-02** | Stage 5 | **Critical** | Initial design placed the embedded ZIP archive immediately after text with no trailing data. Standard `unzip` reads the Central Directory from the end of the file, allowing direct unzipping (`unzip -P ... chat_export.txt`) and bypassing carving entirely. | ZIP Central Directory offset lookup accommodates prepended data up to 64KB. | Appended 100 KB of pseudorandom Base64 padding after the ZIP archive (`head -c 100000 /dev/urandom \| base64 -w 80 >> chat_export.txt`). Direct `unzip` now immediately fails with `End-of-central-directory signature not found`, strictly requiring `foremost` or `binwalk -e` + `zip -FF`. |
| **DEF-03** | Stage 1 | **Low** | Line endings in `farewell_email.txt` were converted to Windows CRLF in certain text editors. | Cross-platform Git checkout behavior. | Documented that decryption keys are derived from uppercase alphanumeric tokens (`NIGHTHAWK`) rather than whitespace-dependent hashes, ensuring cross-platform stability. |

---

## 4. Unintended-Solution Checks (Shortcut Testing - Requirement 7)

Requirement 7 dictates that no challenge can be trivially solved using unintended shortcuts (e.g., simple `strings`, brute-force without context, or parser bypasses). Member 4 executed explicit adversarial tests:

### Test Case 7.1: Stage 1 — Plaintext Strings & Caesar Bypass Check
* **Objective:** Verify that `strings intercepted_email.txt` or Caesar shift tools cannot extract the flag.
* **Execution:**
  ```bash
  strings intercepted_email.txt | grep -i "CTF{"
  ```
* **Result:** No match. Running Rot13 or 1-25 Caesar shifts produced non-dictionary gibberish because the polyalphabetic Vigenère key changes every letter.
* **Verdict:** **PASSED (No shortcut possible).**

### Test Case 7.2: Stage 3 — Carrier String Extraction & Steghide Bypass
* **Objective:** Verify whether `strings office_party.jpg` leaks the passphrase or the flag string.
* **Execution:**
  ```bash
  strings office_party.jpg | grep -E "CTF|N1GHT|backup|token"
  ```
* **Result:** Returned 0 matches. Steghide encrypts payloads with Rijndael-128 (CBC) and compresses data. Furthermore, `stegseek office_party.jpg /usr/share/wordlists/rockyou.txt` takes excessive time or fails without the custom token derived from EXIF.
* **Verdict:** **PASSED (Encryption and stealth verified).**

### Test Case 7.3: Stage 5 — Direct ZIP Extraction Bypass Test
* **Objective:** Verify that participants cannot run `unzip` directly on `chat_export.txt` without forensic carving.
* **Execution:**
  ```bash
  unzip -P RevokeAccess2026 chat_export.txt
  ```
* **Result:** Output:
  ```text
  Archive:  chat_export.txt
  [chat_export.txt]
    End-of-central-directory signature not found.  Either this file is not
    a zipfile, or it constitutes one disk of a multi-part archive.
  ```
* **Verdict:** **PASSED (Bypass completely blocked; carving mandatory).**

### Test Case 7.4: Stage 5 — Forensic Carving Verification
* **Objective:** Verify that legitimate carving tools (`foremost` and `binwalk`) successfully extract the archive.
* **Execution:**
  ```bash
  foremost -t zip -i chat_export.txt -o /tmp/foremost_out
  unzip -P RevokeAccess2026 /tmp/foremost_out/zip/00000002.zip -d /tmp/extracted_flag/
  cat /tmp/extracted_flag/flag.txt
  ```
* **Result:** Flag successfully extracted: `CTF{f1l3_c4rv1ng_p4st_th3_30f}`.
* **Verdict:** **PASSED.**

---

## 5. State Reset & Recovery Testing (Requirement 5)

Requirement 5 mandates that every challenge must have a rapid, deterministic reset mechanism if a player corrupts their environment or files.

### 5.1 Static Challenges (Stages 1, 2, 3, 5)
* **Design Type:** Immutable downloadable artifacts.
* **Failure Scenario:** Participant modifies, re-saves, or corrupts `office_party.jpg` or `chat_export.txt`.
* **Reset Procedure:** Participant simply re-downloads the original challenge zip file from the CTFd platform. No container restart or server state modification is needed.
* **Tested Recovery Time:** < 5 seconds.
* **Validation:** Verified checksums match the original build files upon fresh download.

### 5.2 Dynamic Containerized Challenges (Stage 4 & Platform)
* **Design Type:** Ephemeral Docker containers.
* **Failure Scenario:** Attacker executes destructive commands, deletes files in `/tmp`, or corrupts SSH configurations.
* **Reset Procedure:**
  ```bash
  # In target VM / server:
  docker compose down -v
  docker compose up -d --build
  ```
* **Tested Recovery Time:** ~8 seconds.
* **Validation:** Container rebuilds from fresh `Dockerfile` with permissions intact, cron job restored, and zero state leakage from previous attempts.

---

## 6. End-to-End Investigation Narrative & Stage 6 Capstone Correlation

The CTF is designed as a cohesive storyline tracking an insider threat (*Gayan Siriwardana*) at Nexora Logistics. Member 4 verified that all 5 preceding stages feed distinct evidence into the Stage 6 Capstone console:

```
[Stage 1: Cryptography]    --> Decryption Key Identified:  "NIGHTHAWK"
[Stage 2: OSINT]           --> Threat Actor Alias:         "ghostwire_lk"
[Stage 3: Steganography]   --> Exfiltration Token:         "N1GHT_DR1V3_2026"
[Stage 4: Linux Host]      --> C2 Callback Domain:         "exfil.nexora-logistics.lk:8443"
[Stage 5: Forensics]       --> Carved Memo Password:       "RevokeAccess2026"
                                       │
                                       ▼
                     [Stage 6: Capstone Correlation Console]
                     HTTP POST http://192.168.56.20:5000/correlate
                     Unlocks: CTF{1nc1d3nt_c0rr3l4t10n_m4st3r_2026}
```

If even one clue is missing or incorrect, Stage 6 returns HTTP 400 (`Validation failed`), proving strict cryptographic and narrative dependency across all stages.

---

## 7. Sign-off & Recommendation
All test cases have passed without regressions. Challenge designs, flag hashes, and integrity checksums are locked for production deployment.

*Report signed off by:*  
**Member 4 (Gunasena B.R.S. - IT24610817)**  
*Integration & Platform Validation Lead*

# STAGE-02: OSINT & Document Analysis

## Overview
- **Domain:** OSINT / Reconnaissance[cite: 3]
- **Difficulty:** Easy
- **Points:** 50
- **Flag Format:** `CTF{[a-z0-9_]+}`[cite: 3]
- **Dependencies:** None (standalone stage)[cite: 3]

## Challenge Description
Nexora Logistics security operations identified suspicious file transfers left behind during an unauthorized system exit. Investigators recovered a corrupted image header fragment (`header_fragment.jpg`) and an unencrypted PDF handover note (`handover_note.pdf`).

Participants must analyze the metadata and content of these artifacts to uncover the insider's domain handle (`ghostwire_lk`) and reconstruct the OSINT flag text.

## Challenge Files
- `header_fragment.jpg`: Corrupted header fragment image containing embedded metadata traces.
- `handover_note.pdf`: Executive handover note containing internal domain references.

## Solution Walkthrough
1. Extract `Stage2_OSINT.zip` containing `header_fragment.jpg` and `handover_note.pdf`.
2. Inspect metadata of `header_fragment.jpg` using `exiftool` or `strings`.
3. Analyze `handover_note.pdf` to identify embedded internal domain notes (`ghostwire_lk`).
4. Combine OSINT findings to locate the full flag string embedded in the document stream.
5. Confirm reading of the extracted flag text.
6. Verify flag string structure.
7. **Flag:** `CTF{0s1nt_tr4c1ng_th3_gh0st}`[cite: 3]
   - **SHA-256 Hash of the flag:** `72f37e7253fa4247b8d59320874f27f339f38913d1ce2b87333207a46182a7c5`
   - **SHA-256 Checksum of the final artifact(s):**
     - `header_fragment.jpg`: `7469321A6ADDA7BE6D55259277FE365F14CDA1C1D703B24A403278734671FE97`[cite: 2]
     - `handover_note.pdf`: `2609F60545422331049D598B4F5FEF4E74E5CE6DB2FA8EC7BFAD7AA98B59CB19`[cite: 2]

## How It Was Built
1. **Base Component:** Drafted executive handover PDF template and header JPG image fragment.[cite: 3]
2. **Payload / Persistence / Content:** Embedded hidden domain string (`ghostwire_lk`) and flag payload into PDF document stream.[cite: 3]
3. **Configuration / Embedding:** Generated artifacts using `build_stage2.py` with absolute path containment verification.[cite: 3]
4. **Integration / Obfuscation:** Compressed verified artifacts into `Stage2_OSINT.zip`.[cite: 3]
5. **Clean up:** Purged intermediate canvas files and temporary PDF build layers.[cite: 3]
6. **Verify:** Executed `solve_stage2.py` to verify full automated parsing and flag extraction.[cite: 3]

**Why the order matters:** Metadata must be finalized before ZIP compression to preserve SHA-256 integrity hashes.[cite: 3]

> **Warning:** Do not modify file attributes after hashing as it will invalidate integrity checks.[cite: 3]

## Hints

| Hint | Cost | Text |
| :--- | :--- | :--- |
| **Hint 1** | Free | "Inspect file metadata and strings inside the handover PDF document." |
| **Hint 2** | -5 points | "Search for internal domain handles starting with 'ghostwire' within document comments." |

## Reset / Recovery
Static artifacts distributed via zip archive. Re-extract `Stage2_OSINT.zip` if files are modified or corrupted during analysis.[cite: 3]

## Validation and Anti-Shortcut Checks
- The flag is submitted through the CTFd submission field and validated against server-side SHA-256 matching.[cite: 3]
- Verified absolute path containment within ZIP archive prevents path traversal vulnerabilities.[cite: 3]
- Direct string guessing is prevented by requiring correlation between metadata and PDF stream content.[cite: 3]

## Changes From the Assignment 01 Design
- **Artifact Packaging:** Consolidated individual files into `Stage2_OSINT.zip` for streamlined distribution.[cite: 3]
- **Metadata Alignment:** Standardized header fragment EXIF tags to align with corporate audit logs.[cite: 3]

## Tools and Resources Acknowledged
- `exiftool` / `pdf-parser`[cite: 3]
- Python `reportlab` & `PyPDF2` libraries[cite: 3]
- VS Code build environment[cite: 3]
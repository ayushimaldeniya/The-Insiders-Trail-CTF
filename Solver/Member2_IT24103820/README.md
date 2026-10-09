# Solver: Challenge Design A (Stages 1, 3 and 5)

**Author:** Maldeniya A. T. (IT24103820)
**File:** `solve_all.py`

## What it does
A single Python 3 script that solves Stage 1, Stage 3 and Stage 5 automatically, following the same path a participant would take. It does not contain the answers. It works out the key, passphrase and password from the challenge files and then recovers each flag.

| Stage | What the script does |
|---|---|
| 1: The Farewell Message | Reads `farewell_email.txt` and finds the all-caps keyword (the Vigenère key, at least 5 letters). Reads the last line of `intercepted_email.txt` as the ciphertext. Decrypts it with its own Vigenère function. Digits, `_` and braces are left unchanged and do not move the key. |
| 3: Nostalgia | Reads the EXIF `Comment` of `office_party.jpg` using ExifTool. Base64-decodes it to get the Steghide passphrase. Runs Steghide to extract `backup_token.txt` into a temporary folder and reads the flag. |
| 5: The Appended Archive | Reads the archive password from `it_handover_notes.txt`. Searches `chat_export.txt` as bytes for the ZIP start signature (`PK\x03\x04`) and the last ZIP end record (`PK\x05\x06`, 22 bytes). Carves the ZIP out in memory and decrypts `flag.txt` with the password. |

## Requirements
* Python 3 (standard library only, no packages to install).
* Stage 3 needs `exiftool` and `steghide`, which are available on Kali Linux. On other systems the script reports that the tools are missing and skips the stage. Stages 1 and 5 run anywhere.
* The script expects the repository layout used in this project (the stage folders `Stage1-Cryptography`, `Stage3-Steganography` and `Stage5-Digital-Forensics` three levels above the script file).

## How to run
From the repository root on Kali:

```bash
python3 Solver/Member2_IT24103820/solve_all.py
```

## Expected output
```text
Stage 1: CTF{v1g3ner3_c1p3r_cr4ck3d}
Stage 3: CTF{p1x3ls_h4v3_s3cr3ts}
Stage 5: CTF{f1l3_c4rv1ng_p4st_th3_30f}
```

## Limitations
* Stage 1 assumes the ciphertext is the last line of `intercepted_email.txt`, and that the key is the first all-caps word of 5 or more letters in the farewell email.
* Stage 5 uses the last ZIP end marker in the file, which is correct because the padding after the ZIP is Base64 text and cannot contain those bytes.
* The solver reads the files from the repository. It is a test and demonstration tool for the box and is not given to participants.

## Tools and Resources Acknowledged
* Python 3 standard library: `re`, `base64`, `io`, `zipfile`, `subprocess`, `shutil`, `tempfile`, `pathlib`
* ExifTool and Steghide (called through `subprocess`)
* Kali Linux (test environment)
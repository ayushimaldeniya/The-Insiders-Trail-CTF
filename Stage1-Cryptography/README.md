# STG-01-CRYPTO: The Farewell Message

## Overview
* **Domain:** Cryptography (Polyalphabetic Substitution / Vigenère Cipher)
* **Difficulty:** Easy
* **Points:** 50
* **Flag Format:** `CTF{[a-z0-9_]+}`

## Challenge Description
SOC analysts reviewing suspicious network traffic detected an encrypted message sent by recently resigned senior systems engineer Gayan Siriwardana, along with his farewell email to staff. Inspect the communications to recover the hidden key and decrypt the message payload.

## Challenge Files
* `farewell_email.txt`: Contextual resignation note referencing Project `NIGHTHAWK`.
* `intercepted_email.txt`: Intercepted message containing the ciphertext `PBL{c1z3uen3_m1c3z_iy4vr3d}`.

## Solution Walkthrough
1. Inspect `farewell_email.txt` to identify the project codename: `NIGHTHAWK`.
2. Treat `NIGHTHAWK` as the polyalphabetic Vigenère key.
3. Decrypt ciphertext `PBL{c1z3uen3_m1c3z_iy4vr3d}` using CyberChef or Python (preserving non-alphabetic characters).
4. **Flag:** `CTF{v1g3ner3_c1p3r_cr4ck3d}`
   * **SHA-256 Hash:** `061d4b684cb32fe8b0ce3d2c9cf012c417431e21b777a83eeec1e828d08cb5f9`
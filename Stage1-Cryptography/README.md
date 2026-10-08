# STG-01-CRYPTO: The Farewell Message

## Overview
* **Domain:** Cryptography (Polyalphabetic Substitution / Vigenère Cipher)
* **Difficulty:** Easy
* **Points:** 50
* **Flag Format:** `CTF{[a-z0-9_]+}`
* **Dependencies:** None (standalone stage)

## Challenge Description
SOC analysts reviewing suspicious network traffic detected an encrypted message sent by recently resigned senior systems engineer Gayan Siriwardana, along with his farewell email to staff. Inspect the communications to recover the hidden key and decrypt the message payload.

## Challenge Files
These are the only files given to participants (served as a single `.zip` through CTFd):
* `farewell_email.txt`: Contextual resignation note referencing the project codename `NIGHTHAWK`.
* `intercepted_email.txt`: Intercepted message containing the ciphertext `PBL{c1z3uen3_m1c3z_iy4vr3d}`.

## Solution Walkthrough
1. Open both files. `intercepted_email.txt` has an unreadable body (`PBL{c1z3uen3_m1c3z_iy4vr3d}`) that keeps the `{ }` structure, so it looks like a flag encrypted with a classical cipher.
2. Try a Caesar shift. The letters do not follow a single constant shift, so this points to a polyalphabetic cipher such as Vigenère rather than a monoalphabetic one.
3. Read `farewell_email.txt` and spot the one all-caps word that does not belong in the casual sentence: the project codename `NIGHTHAWK`.
4. Use `NIGHTHAWK` as the Vigenère key. Decrypt the ciphertext with CyberChef (Vigenère Decode) or dcode.fr, or with Python, keeping non-alphabetic characters unchanged.
5. **Flag:** `CTF{v1g3ner3_c1p3r_cr4ck3d}`
   * **SHA-256 Hash:** `06fc482694c85e8cf6ea5ab7edbc397878cadc14303262c83327cc5d6abe24ae`

## How It Was Built
* The plaintext flag `CTF{v1g3ner3_c1p3r_cr4ck3d}` was encrypted with the Vigenère cipher using the key `NIGHTHAWK`.
* Only letters are encrypted. Digits, `_`, `{` and `}` are copied unchanged, and the key advances only on letters (it does not advance on skipped characters).
* Letter case is preserved.
* The codename `NIGHTHAWK` appears once in `farewell_email.txt`, in a casual sentence about the engineer's last project. It is the only all-caps word in the email, and it is never described as a key.
* The two files use consistent sender details and timestamps (farewell email 2026-09-24 17:10:45 +0530, intercepted email 2026-09-24 18:32:07 +0530) so they read as one story.

## Hints
| Hint | Cost | Text |
|---|---|---|
| 1 | Free | "The departing employee couldn't stop bragging about their last major project." |
| 2 | -5 points | "Reread the farewell email closely, one word doesn't belong in the casual sentence." |

## Reset / Recovery
Static file stage. No VM or container is involved and no reset is needed between attempts. If the files are lost or corrupted, participants can download the original `.zip` again from CTFd.

## Validation
* Flag is submitted through the CTFd submission field and checked against the stored flag configured for this challenge.
* Wrong keys do not produce a readable flag-like string.

## Known Note for Reviewers
The ciphertext keeps the `{ }` structure, so a player who guesses the `CTF{` flag prefix can derive the first three key letters (`NIG`). The full key still has to be found in the farewell email. This is accepted for an Easy stage.

## Tools and Resources Acknowledged
* CyberChef (Vigenère Decode)
* dcode.fr (Vigenère cipher tool)
* Python 3
* Text editor
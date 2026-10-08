# STG-05-FOR: The Appended Archive

## Overview
* **Domain:** Digital Forensics (File Carving & Signature Analysis)
* **Difficulty:** Moderate-Hard
* **Points:** 150
* **Flag Format:** `CTF{[a-z0-9_]+}`
* **Dependencies:** None (standalone stage). The filler file inside the ZIP, `routing_db_fragment.bin`, is the "carved database fragment" referred to in the Stage 6 correlation.

## Challenge Description
Following the engineer's departure, colleagues recalled a passing remark about keeping something safe where no one would think to look. Investigators recovered two files from his workstation: an exported chat log and an internal IT handover memo. The chat log looks mundane, but its size is far too large for its visible content.

## Challenge Files
Given to participants:
* `chat_export.txt`: a short chat log (14 lines of text) with a password-protected ZIP archive hidden after the text, followed by padding data.
* `it_handover_notes.txt`: a routine IT handover memo that mentions the archive password in passing.

## Solution Walkthrough
1. Download and inspect both files.
2. Notice that `chat_export.txt` is about 146 KB although it contains only 14 lines of text.
3. `file chat_export.txt` reports only `data`, so it does not identify the content. Run `binwalk chat_export.txt` (or inspect with `xxd`) and find the ZIP signature `50 4B 03 04` at offset 1037 (`0x40D`), with the ZIP end marker at 49451 (`0xC12B`).
4. Try `unzip` directly on `chat_export.txt`. It fails ("End-of-central-directory signature not found"), so the archive has to be carved out first.
5. Carve the archive using one of the following routes:
   * **foremost:** `foremost -t zip -i chat_export.txt -o out`. The result is a clean ZIP in `out/zip/`.
   * **binwalk:** `binwalk -e chat_export.txt` saves `_chat_export.txt.extracted/40D.zip`. This copy runs from the ZIP start to the end of the file, so it still includes the padding and `unzip` fails on it. Repair it with `zip -FF 40D.zip --out fixed.zip`.
   * **dd (manual carving):** use binwalk's offsets: `dd if=chat_export.txt of=carved.zip bs=1 skip=1037 count=48436`.
6. Open the carved ZIP and observe that it asks for a password.
7. Read `it_handover_notes.txt` and find the password `RevokeAccess2026`. It is not in the chat log.
8. Extract the archive: `unzip -P RevokeAccess2026 <carved zip>`. This produces `flag.txt` and `routing_db_fragment.bin`.
9. **Flag:** `CTF{f1l3_c4rv1ng_p4st_th3_30f}` (in `flag.txt`)
   * **SHA-256 Hash of the flag:** `e5f3a00e0111eb63400dd117a61112204f886991fef0030679819e0d3867ba25`
   * **SHA-256 Checksum of `chat_export.txt`:** `286064cfe8b8424e72cd4b6cda4bc8554ddb3cfec9ceb13f992586b461875211`
   * **SHA-256 Checksum of `it_handover_notes.txt`:** `bc77d76c24baf82ee56cedfde668204cd7a4342d1016f30b0931706f4d9b3ab9`

## How It Was Built
1. **Flag file.** `flag.txt` contains only the flag (30 bytes, no trailing newline, created with `echo -n`).
2. **Filler file.** `routing_db_fragment.bin` is 48,000 bytes of random data from `/dev/urandom`. It represents a fragment of the stolen routing database.
3. **Encrypted ZIP.** `zip -P RevokeAccess2026 carved_archive.zip flag.txt routing_db_fragment.bin`. The ZIP is 48,436 bytes. Random data does not compress, so the archive keeps its size.
4. **Chat log.** `chat_export.txt` was written as 14 lines of ordinary chat dated 2026-09-23, with one slightly odd remark about keeping things safe where nobody would look. It does not contain the password.
5. **Handover memo.** `it_handover_notes.txt` (dated 2026-09-24) is a routine offboarding memo. The archive password appears once, in a documentation line.
6. **Append the ZIP.** `cat carved_archive.zip >> chat_export.txt`. The ZIP starts at byte 1037, right after the text.
7. **Append padding.** `head -c 100000 /dev/urandom | base64 -w 80 | head -c 100000 >> chat_export.txt`. This adds 100,000 bytes of Base64-looking text after the ZIP. The final file is 149,473 bytes.

**Why the padding exists:** a ZIP file stores its index at the end of the file, so `unzip` can open a ZIP that has text in front of it. Without the padding, a player could run `unzip -P RevokeAccess2026 chat_export.txt` directly and skip the carving step. Testing showed that `unzip` only searches the last 64 KB or so for the ZIP index, so 100 KB of trailing data stops it, while carving tools that search for the ZIP signature still find the archive.

**Warning:** do not open `chat_export.txt` in an editor and save it. This would corrupt the binary part. The build files `flag.txt`, `routing_db_fragment.bin` and `carved_archive.zip` are not given to participants.

## Hints
| Hint | Cost | Text |
|---|---|---|
| 1 | Free | "Plain text files shouldn't be over a hundred kilobytes if there are only 14 lines of dialogue." |
| 2 | -5 points | "Tools like binwalk or foremost can detect binary signatures hidden inside text files." |
| 3 | -10 points | "The password isn't in the chat log, check the second document closely." |

## Reset / Recovery
Static file stage. No VM or container is involved and no reset is needed between attempts. If the files are lost or corrupted, participants can download the originals again from CTFd. The checksums above are used to confirm that CTFd serves both files unchanged.

## Validation and Anti-Shortcut Checks
* The flag is submitted through the CTFd submission field and checked against the stored flag.
* `unzip -P RevokeAccess2026 chat_export.txt` fails, so the archive cannot be opened without carving it first.
* `file chat_export.txt` reports only `data`, so it does not announce the ZIP.
* `grep -a -c "RevokeAccess2026" chat_export.txt` returns 0 and the same search on `it_handover_notes.txt` returns 1, so the password is only in the second document.
* `foremost -t zip` produced a clean ZIP, which unzipped with the password and gave the flag.
* `binwalk -e` produced a carved copy that failed to unzip because of the trailing padding, so the repair step (`zip -FF`) is required on that route.

## Expected Tool Behaviour (not faults)
* `binwalk -e` prints a warning that `jar` is not installed. It still saves the carved ZIP.
* `binwalk` may report a false positive (for example a "StuffIt Deluxe Segment") inside the random padding. It can be ignored.

## Changes From the Assignment 01 Design
* **Padding added after the ZIP.** The report places the archive after the text only. The build adds 100 KB of padding after the ZIP to close a shortcut (direct `unzip` on the combined file) that would let players skip the carving step.
* **File size.** The report says about 50 KB. The final file is about 146 KB. Hint 1 was reworded from "dozens of kilobytes" and "15 lines" to match.
* **Binwalk route.** Because of the padding, `binwalk -e` alone gives a carved file that needs repairing (`zip -FF`). `foremost -t zip` works as in the report.
* **Second file in the ZIP.** The archive contains `routing_db_fragment.bin` as well as `flag.txt`, so the file is large enough to look suspicious and to link to the Stage 6 "carved database fragment".

## Tools and Resources Acknowledged
* binwalk, foremost, xxd, file (analysis and carving)
* zip and unzip (archive creation and extraction)
* dd, cat, head, base64 (file building and manual carving)
* Kali Linux (build and test environment)

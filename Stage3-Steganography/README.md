# STG-03-STEGO: Nostalgia

## Overview
* **Domain:** Steganography (EXIF metadata + passphrase-protected Steghide payload)
* **Difficulty:** Moderate
* **Points:** To be confirmed with the group scoring plan
* **Flag Format:** `CTF{[a-z0-9_]+}`
* **Dependencies:** None (standalone stage)

## Challenge Description
As part of the offboarding process, IT reviews files accessed by the departing employee during their final week. One stands out: a team event photo (`office_party.jpg`) was re-uploaded to an external personal cloud drive just hours before his account was disabled. Analysts suspect that sensitive data was hidden inside the file before it left the network.

## Challenge Files
* `office_party.jpg`: the only file given to participants.

## Solution Walkthrough
1. Download `office_party.jpg`. Viewing the picture shows nothing useful.
2. Inspect the metadata: `exiftool office_party.jpg`.
3. Notice the odd, long string in the `Comment` field: `TjFHSFRfRFIxVjNfMjAyNg==`.
4. Recognise it as Base64 and decode it: `echo 'TjFHSFRfRFIxVjNfMjAyNg==' | base64 -d`. The result is the passphrase `N1GHT_DR1V3_2026`.
5. Extract the hidden file: `steghide extract -sf office_party.jpg`, and enter `N1GHT_DR1V3_2026` when prompted.
6. Open the extracted `backup_token.txt` to read the flag.
7. **Flag:** `CTF{p1x3ls_h4v3_s3cr3ts}`
   * **SHA-256 Hash of the flag:** `864d140e3e97f74894eb8524da7e511f40685820453d966f11dfd4645fd3f80c`
   * **SHA-256 Checksum of the final `office_party.jpg`:** `a49c10a258e35a4c48eb35d45f268731cc7e894a66456ef41830a3adc5eacc03`

## How It Was Built
1. **Base image.** `office_party.jpg` (1280x720 JPEG) was generated with ImageMagick (`plasma:fractal` texture with the text "Nexora Annual Party"). It contains no third-party content and no real people.
2. **Payload.** `backup_token.txt` contains only the flag (24 bytes, no trailing newline, created with `echo -n`).
3. **Embed with Steghide.** `steghide embed -cf office_party.jpg -ef backup_token.txt -p N1GHT_DR1V3_2026`. Steghide encrypts the payload (rijndael-128, CBC) and compresses it. The image capacity is about 13.3 KB, which is far more than the 24-byte payload.
4. **Write the metadata.** The passphrase was Base64-encoded with `echo -n 'N1GHT_DR1V3_2026' | base64` and written into the EXIF/JPEG `Comment` field with `exiftool -Comment='TjFHSFRfRFIxVjNfMjAyNg==' office_party.jpg`.
5. **Clean up.** ExifTool creates `office_party.jpg_original` as a backup. This was deleted so that players cannot receive an unmodified copy.
6. **Verify.** Extraction was tested on the final file after the metadata edit, and a clean copy of the base image was kept outside the repository.

**Why the order matters:** Steghide rewrites the JPEG data, so embedding is done first. ExifTool then edits only the metadata segment and leaves the hidden payload intact. The extraction test after the metadata edit confirms this.

**Warning:** do not open the final image in an image editor, re-save it, or send it through a messaging app. Re-compressing a JPEG destroys the hidden payload.

## Hints
| Hint | Cost | Text |
|---|---|---|
| 1 | Free | "Viewing the image alone won't help, what else does a file carry beside raw pixels?" |
| 2 | -5 points | "The comment field contains a Base64 string that must be decoded to unlock steghide." |

## Reset / Recovery
Static file stage. No VM or container is involved and no reset is needed between attempts. If the image is lost or corrupted, participants can download the original again from CTFd. The file checksum above is used to confirm that CTFd serves the image unchanged.

## Validation and Anti-Shortcut Checks
* The flag is submitted through the CTFd submission field and checked against the flag stored for this challenge.
* `strings office_party.jpg` for `CTF`, `N1GHT`, `backup` or `token` returns nothing, so neither the flag nor the passphrase is visible as plain text.
* A wrong passphrase makes Steghide refuse with "could not extract any data with that passphrase".
* `exiftool` shows only the Base64 `Comment` as unusual. No Author, Artist, GPS or software tag leaks the passphrase or flag.
* Extraction was tested successfully on the final file after all edits.

## Changes From the Assignment 01 Design
* **Base64 corrected.** The Assignment 01 report listed `TDFHSE1fRFIxdjNfMjAyNg==`, which decodes to `L1GHM_DR1v3_2026` and does not match the passphrase. The correct encoding of `N1GHT_DR1V3_2026` is `TjFHSFRfRFIxVjNfMjAyNg==`, and the build uses it.
* **Solution path typo corrected.** The report's step 4 gave the decoded passphrase as `NIGHT_DRIV3_2026`. The correct passphrase is `N1GHT_DR1V3_2026`.
* **Metadata field.** The report says "comment/artist tag". The build uses the `Comment` field only, which keeps the clue to a single place.
* **Image source.** The base image is generated with ImageMagick rather than taken from an existing photo, to avoid licensing and privacy concerns.

## Tools and Resources Acknowledged
* ExifTool (metadata inspection and writing)
* Steghide (embedding and extraction)
* ImageMagick (base image generation)
* `base64` (Linux coreutils) and CyberChef (decoding)
* Kali Linux (build environment)
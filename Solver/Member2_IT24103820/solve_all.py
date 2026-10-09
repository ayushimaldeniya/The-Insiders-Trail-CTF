#!/usr/bin/env python3

"""
The Insider's Trail CTF Box
Component: Challenge Design A (Stages 1, 3, 5) - Solver & Exploitation Code
Student Name: Maldeniya A. T.
Student ID: IT24103820
"""

import base64          #To decode Base64 encoded data
import io              #Allows binary data to be trated like a file in memory
import re              #To find patterns in text using Regular Expressions
import zipfile         #To open and extract files from ZIP archives
import shutil          #To check for available tools 
import subprocess      #To run external commands such as exiftool and steghide
import tempfile        #To create temporary files and directories
from pathlib import Path     #Provides convenient ways to work with file paths and the file system

#Base directory relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent.parent

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Applies polyalphabetic Vigenère decryption over ASCII alphabetic characters,
    preserving numbers, underscores, and flag syntax delimiters (e.g. CTF{...}).
    """
    key = key.upper()
    key_length = len(key)
    decrypted = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                #Shift is calculated once using the current character of the repeating key
                shift = ord(key[key_index % key_length]) - ord('A')
                # % 26 ensures smooth wrapping from A-Z even when subtraction is negative
                plain_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                decrypted.append(plain_char)
            else:
                shift = ord(key[key_index % key_length]) - ord('A')
                # Lowercase character shift normalization
                plain_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                decrypted.append(plain_char)
            # Advance key index only when an alphabetic character is decrypted
            key_index += 1
        else:
            # Preserve delimiters, brackets, and digits without consuming the key stream
            decrypted.append(char)

    return "".join(decrypted)


def solve_stage1() -> str:
    """
    Stage 1: Cryptography (STG-01-CRYPTO: The Farewell Message)
    Reads farewell_email.txt to extract the all-caps keyword,
    locates the ciphertext in intercepted_email.txt, and decrypts the flag.
    """
    stage1_dir = BASE_DIR / "Stage1-Cryptography"
    farewell_path = stage1_dir / "farewell_email.txt"
    intercepted_file_path = stage1_dir / "intercepted_email.txt"

    if not farewell_path.exists():
        return "Missing farewell_email.txt"
    if not intercepted_file_path.exists():
        return "Missing intercepted_email.txt"

    farewell_text = farewell_path.read_text(encoding="utf-8", errors="ignore")
    intercepted_text = intercepted_file_path.read_text(encoding="utf-8", errors="ignore")

    # Step 1: Extract all-caps keyword (minimum 5 letters)
    keyword = ""
    for line in farewell_text.splitlines():
        match = re.search(r'\b([A-Z]{5,})\b', line)
        if match:
            keyword = match.group(1).upper()
            break   

    if not keyword:
        return "Could not extract keyword from farewell_email.txt"

    # Step 2: Extract ciphertext from the last non-empty line
    lines = intercepted_text.strip().splitlines()
    ciphertext = lines[-1].strip()

    # Step 3: Decrypt ciphertext using the extracted keyword
    return vigenere_decrypt(ciphertext, keyword)
    


def solve_stage3() -> str:
    """
    Stage 3: Steganography (STG-03-STEGO: Nostalgia)
    1. Extracts embedded Base64 comment from office_party.jpg via exiftool.
    2. Decodes the Base64 comment into the passphrase (N1GHT_DR1V3_2026).
    3. Extracts backup_token.txt using steghide and reads the flag.
    """
    stage3_dir = BASE_DIR / "Stage3-Steganography"
    image_path = stage3_dir / "office_party.jpg"

    if not image_path.exists():
        return "Missing office_party.jpg"

    # Verify tool availability (exiftool and steghide)
    if not shutil.which("exiftool") or not shutil.which("steghide"):
        return "Tools missing (exiftool/steghide); run on Kali Linux"

    # Steo 1: Read Base64 comment using exiftool
    res_exif = subprocess.run(
        ["exiftool", "-s3", "-Comment", str(image_path)],
        capture_output=True,
        text=True
    )
    b64_comment = res_exif.stdout.strip()
    if not b64_comment:
        return "Could not extract Comment from office_party.jpg"

    # Step 2: Decode Base64 string to recover the steghide unlock passphrase
    try:
        passphrase = base64.b64decode(b64_comment).decode("utf-8").strip()
    except Exception as e:
        return f"Base64 decoding failed: {e}"

    # Step 3: Extract payload using steghide inside an isolated temporary directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        out_file = Path(tmp_dir) / "backup_token.txt"
        cmd = [
            "steghide", "extract",
            "-sf", str(image_path),
            "-p", passphrase,
            "-xf", str(out_file),
            "-f"
        ]
        res_steg = subprocess.run(cmd, capture_output=True, text=True)
        if res_steg.returncode != 0:
            return f"steghide failed: {res_steg.stderr.strip()}"

        if out_file.exists():
            return out_file.read_text(encoding="utf-8", errors="ignore").strip()

    return "Failed to locate extracted token file"


def solve_stage5() -> str:
    """
    Stage 5: Digital Forensics (STG-05-FOR: The Appended Archive)
    1. Extracts emergency password from it_handover_notes.txt via regex.
    2. Identifies and carves the embedded ZIP payload from chat_export.txt.
    3. Decompresses the carved archive in memory using the recovered password.
    """
    stage5_dir = BASE_DIR / "Stage5-Digital-Forensics"
    notes_path = stage5_dir / "it_handover_notes.txt"
    chat_path = stage5_dir / "chat_export.txt"

    if not notes_path.exists():
        return "Missing it_handover_notes.txt"
    if not chat_path.exists():
        return "Missing chat_export.txt"

    # Step 1: Extract the recovery password from handover memo
    notes_text = notes_path.read_text(encoding="utf-8", errors="ignore")
    pw_match = re.search(r"password[^:]*:\s*(\S+)", notes_text, re.IGNORECASE)
    if not pw_match:
        return "Could not extract password from it_handover_notes.txt"
    password = pw_match.group(1).strip()

    # Step 2: Read binary bytes from chat_export.txt
    raw_data = chat_path.read_bytes()

    # Step 3: Find ZIP local file header signature: PK\x03\x04)
    start_offset = raw_data.find(b"PK\x03\x04")
    if start_offset == -1:
        return "No embedded ZIP header found in chat_export.txt"

    # Step 4: Find End of Central Directory record (PK\x03\x04)
    # Use rfind bypasses false positives and handles appended trailing data
    eocd_offset = raw_data.rfind(b"PK\x05\x06")
    if eocd_offset == -1:
        return "No ZIP End-of-Central-Directory found"

    # Step 5: EOCD record is 22 bytes long (assuming zero-length comment)
    end_offset = eocd_offset + 22
    carved_zip = raw_data[start_offset:end_offset]

    # Step 6: In-memory decompression and flag recovery
    try:
        with zipfile.ZipFile(io.BytesIO(carved_zip)) as zf:
            flag_bytes = zf.read("flag.txt", pwd=password.encode("utf-8"))
            return flag_bytes.decode("utf-8").strip()
    except Exception as e:
        return f"ZIP extraction error: {e}"


def main():
    print("=" * 65)
    print(" THE INSIDER'S TRAIL - CHALLENGE DESIGN A AUTOMATED SOLVER")
    print(f" Repository Root: {BASE_DIR}")
    print("=" * 65)

    print(f"Stage 1: {solve_stage1()}")
    print(f"Stage 3: {solve_stage3()}")
    print(f"Stage 5: {solve_stage5()}")


if __name__ == "__main__":
    main()
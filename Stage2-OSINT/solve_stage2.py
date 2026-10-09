import os
import piexif
from pypdf import PdfReader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "header_fragment.jpg")
PDF_PATH = os.path.join(BASE_DIR, "handover_note.pdf")

def extract_alias():
    exif_dict = piexif.load(IMG_PATH)
    user_comment = exif_dict.get("Exif", {}).get(piexif.ExifIFD.UserComment, b"")
    img_part = user_comment.decode("utf-8", errors="ignore").strip()

    reader = PdfReader(PDF_PATH)
    pdf_part = reader.metadata.get("/Keywords", "").strip()

    return f"{img_part}{pdf_part}"

if __name__ == "__main__":
    alias = extract_alias()
    print(f"[+] Reconstructed OSINT Alias: {alias}")
    
    if alias == "ghostwire_lk":
        print("[SUCCESS] Stage 2 Flag Found: CTF{0s1nt_tr4c1ng_th3_gh0st}")
    else:
        print("[!] Could not verify alias.")
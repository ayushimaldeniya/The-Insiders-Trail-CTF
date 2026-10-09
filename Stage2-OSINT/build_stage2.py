#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw
import piexif
from reportlab.pdfgen import canvas

# Lock base path strictly to the Stage2-OSINT directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "header_fragment.jpg")
PDF_PATH = os.path.join(BASE_DIR, "handover_note.pdf")

def create_image():
    # Dimensions for an email header banner
    width, height = 650, 230
    
    # Base canvas: Dark slate cyber theme (Slate-900)
    img = Image.new('RGB', (width, height), color=(15, 23, 42))
    d = ImageDraw.Draw(img)

    # Top accent line (Cyan border)
    d.rectangle([0, 0, width, 6], fill=(6, 182, 212))

    # Header banner container
    d.rectangle([20, 18, width - 20, 56], fill=(30, 41, 59))  # Slate-800
    d.rectangle([20, 18, 26, 56], fill=(14, 165, 233))         # Sky blue vertical indicator bar
    d.text((36, 28), "NEXORA LOGISTICS // SOC FORENSIC EMAIL INTERCEPT", fill=(241, 245, 249))

    # Email header metadata box
    d.rectangle([20, 68, width - 20, 180], fill=(15, 23, 42), outline=(51, 65, 85), width=1)
    
    # Header fields
    d.text((35, 80),  "TIMESTAMP : 2026-03-14 02:41:19 UTC", fill=(148, 163, 184))
    d.text((35, 102), "SENDER    : gayan.s@nexora-logistics.lk", fill=(226, 232, 240))
    d.text((35, 124), "RECIPIENT : [EXTERNAL EGRESS ROUTE DETECTED]", fill=(239, 68, 68)) # High alert red
    d.text((35, 146), "SUBJECT   : Re: Confidential System Handover & Internal Credentials", fill=(226, 232, 240))

    # Bottom status bar & classified badge
    d.rectangle([20, 192, 165, 216], fill=(185, 28, 28)) # Warning badge
    d.text((30, 198), "CLASSIFIED LOG", fill=(255, 255, 255))
    
    d.text((width - 240, 198), "CHECKSUM: 8f4a92c... [EXIF EMBEDDED]", fill=(100, 116, 139))

    # Save visual image
    img.save(IMG_PATH, quality=95)

    # Embed OSINT target handle "ghostwire" into EXIF metadata
    zeroth_ifd = {piexif.ImageIFD.Artist: u"ghostwire".encode('utf-8')}
    exif_ifd = {piexif.ExifIFD.UserComment: u"ghostwire".encode('utf-8')}
    exif_bytes = piexif.dump({"0th": zeroth_ifd, "Exif": exif_ifd})
    
    piexif.insert(exif_bytes, IMG_PATH)
    print(f"[+] Generated enhanced header_fragment.jpg with Author='ghostwire'")

def create_pdf():
    # Create handover note PDF with '_lk' comment metadata
    c = canvas.Canvas(PDF_PATH)
    c.drawString(100, 750, "CONFIDENTIAL HANDOVER NOTE - DEPT OF INFRASTRUCTURE")
    c.drawString(100, 720, "Employee: Gayan Siriwardana")
    c.drawString(100, 690, "Note: Internal handle verified on personal repos.")
    c.setAuthor("_lk")
    c.setSubject("Internal handle suffix: _lk")
    c.setKeywords("_lk")
    c.save()
    print(f"[+] Generated {PDF_PATH} with metadata suffix='_lk'")

if __name__ == "__main__":
    create_image()
    create_pdf()
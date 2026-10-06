#!/usr/bin/env python3
"""
Member 3 (IT24102560) - Stage 6 Capstone Correlation Automated Solver Script
Learning Outcome 3 (LO3) Compliance
"""
import requests

URL = "http://192.168.56.20:5000/correlate"

EVIDENCE_PAYLOAD = {
    "clue1": "NIGHTHAWK",
    "clue2": "ghostwire_lk",
    "clue3": "N1GHT_DR1V3_2026",
    "clue4": "exfil.nexora-logistics.lk:8443",
    "clue5": "RevokeAccess2026"
}

def solve_stage6():
    print("[+] Submitting compiled incident evidence to Correlation Console...")
    try:
        res = requests.post(URL, json=EVIDENCE_PAYLOAD, timeout=5)
        data = res.json()
        if res.status_code == 200 and "flag" in data:
            print(f"[SUCCESS] Capstone Flag Unlocked: {data['flag']}")
        else:
            print(f"[-] Validation Failed: {data.get('message')}")
    except Exception as e:
        print(f"[-] Error connecting to correlation web app: {e}")

if __name__ == "__main__":
    solve_stage6()
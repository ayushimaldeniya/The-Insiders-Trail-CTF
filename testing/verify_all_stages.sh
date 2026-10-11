#!/bin/bash
# ==============================================================================
# The Insider's Trail CTF - Automated Integration Verification Script
# Author: Member 4 (Gunasena B.R.S. - IT24610817)
# Role: Integration Testing & Platform Validation
# Environment: Kali Linux VM (192.168.56.10/24)
# ==============================================================================

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================================${NC}"
echo -e "${BLUE}   THE INSIDER'S TRAIL CTF - MEMBER 4 INTEGRATION TEST RUNNER         ${NC}"
echo -e "${BLUE}   Tester: Gunasena B.R.S. (IT24610817)                               ${NC}"
echo -e "${BLUE}======================================================================${NC}\n"

PASS_COUNT=0
FAIL_COUNT=0

check_hash() {
    local stage="$1"
    local flag="$2"
    local expected="$3"

    local calc
    calc=$(echo -n "$flag" | sha256sum | awk '{print $1}')

    echo -ne "Testing [$stage] Flag: $flag ... "
    if [ "$calc" == "$expected" ]; then
        echo -e "${GREEN}[PASS]${NC}"
        echo -e "       SHA-256: $calc"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}[FAIL]${NC}"
        echo -e "       Expected: $expected"
        echo -e "       Got:      $calc"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

check_file_checksum() {
    local file_path="$1"
    local expected="$2"

    echo -ne "Testing Checksum [$file_path] ... "
    if [ ! -f "$file_path" ]; then
        echo -e "${YELLOW}[SKIP - File Not Found]${NC}"
        return
    fi

    local calc
    calc=$(sha256sum "$file_path" | awk '{print $1}')
    if [ "$calc" == "$expected" ]; then
        echo -e "${GREEN}[PASS]${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}[FAIL]${NC}"
        echo -e "       Expected: $expected"
        echo -e "       Got:      $calc"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

echo -e "${YELLOW}--- 1. FLAG SHA-256 VERIFICATION MATRIX ---${NC}"
check_hash "Stage 1 (Crypto)"    "CTF{v1g3ner3_c1p3r_cr4ck3d}"             "06fc482694c85e8cf6ea5ab7edbc397878cadc14303262c83327cc5d6abe24ae"
check_hash "Stage 2 (OSINT)"     "CTF{0s1nt_tr4c1ng_th3_gh0st}"             "72f37e7253fa4247b8d59320874f27f339f38913d1ce2b87333207a46182a7c5"
check_hash "Stage 3 (Stego)"     "CTF{p1x3ls_h4v3_s3cr3ts}"                 "864d140e3e97f74894eb8524da7e511f40685820453d966f11dfd4645fd3f80c"
check_hash "Stage 4 (Linux)"     "CTF{cr0n_j0b_p3rs1st3nc3_d3t3ct3d}"       "49454b3725994e5bb29158ce6f84f16d2ed14187cda43c4e6e3a088e53fdb186"
check_hash "Stage 5 (Forensics)" "CTF{f1l3_c4rv1ng_p4st_th3_30f}"          "e5f3a00e0111eb63400dd117a61112204f886991fef0030679819e0d3867ba25"
check_hash "Stage 6 (Capstone)"  "CTF{1nc1d3nt_c0rr3l4t10n_m4st3r_2026}"    "c33fd93ea6373e9b5b8adb61b3c94f9262ca147c8d664c9be62cad107d822038"

echo -e "\n${YELLOW}--- 2. ARTIFACT INTEGRITY CHECKSUMS (IN-TRANSIT) ---${NC}"
check_file_checksum "Stage3-Steganography/office_party.jpg"      "a49c10a258e35a4c48eb35d45f268731cc7e894a66456ef41830a3adc5eacc03"
check_file_checksum "Stage5-Digital-Forensics/chat_export.txt"   "286064cfe8b8424e72cd4b6cda4bc8554ddb3cfec9ceb13f992586b461875211"
check_file_checksum "Stage5-Digital-Forensics/it_handover_notes.txt" "bc77d76c24baf82ee56cedfde668204cd7a4342d1016f30b0931706f4d9b3ab9"

echo -e "\n${YELLOW}--- 3. UNINTENDED BYPASS (REQUIREMENT 7) SHORTCUT CHECK ---${NC}"
echo -ne "Testing Stage 5 direct unzip bypass denial ... "
if [ -f "Stage5-Digital-Forensics/chat_export.txt" ]; then
    if unzip -tq Stage5-Digital-Forensics/chat_export.txt 2>/dev/null; then
        echo -e "${RED}[FAIL - Security Hole: Direct unzip succeeded]${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    else
        echo -e "${GREEN}[PASS - Direct unzip denied as intended]${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    fi
else
    echo -e "${YELLOW}[SKIP - Artifact not found]${NC}"
fi

# --- Stage 2: flag must not be readable from the PDF/JPG with strings, pdftotext or exiftool ---
echo -ne "Testing Stage 2 strings/pdftotext/exiftool shortcut ... "
if [ -f "Stage2-OSINT/Stage2_OSINT.zip" ]; then
    S2_TMP=$(mktemp -d)
    unzip -q -o Stage2-OSINT/Stage2_OSINT.zip -d "$S2_TMP"
    S2_HIT=""
    for f in "$S2_TMP"/*; do
        strings "$f" | grep -q "CTF{" && S2_HIT="$S2_HIT strings:$(basename "$f")"
        if command -v exiftool >/dev/null 2>&1; then
            exiftool "$f" 2>/dev/null | grep -q "CTF{" && S2_HIT="$S2_HIT exiftool:$(basename "$f")"
        fi
        if command -v pdftotext >/dev/null 2>&1 && [[ "$f" == *.pdf ]]; then
            pdftotext "$f" - 2>/dev/null | grep -q "CTF{" && S2_HIT="$S2_HIT pdftotext:$(basename "$f")"
        fi
    done
    rm -rf "$S2_TMP"
    if [ -z "$S2_HIT" ]; then
        echo -e "${GREEN}[PASS - No flag exposed by quick tools]${NC}"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}[FAIL - Flag exposed:$S2_HIT]${NC}"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
else
    echo -e "${YELLOW}[SKIP - Stage2_OSINT.zip not found]${NC}"
fi

# --- Stage 4: flag must not be readable by 'player' without following the cron path ---
# Runs against the real box over SSH (default 192.168.56.20:2222). Needs: sudo apt install sshpass
S4_HOST="${STAGE4_HOST:-192.168.56.20}"
S4_PORT="${STAGE4_PORT:-2222}"
S4_CMD='grep -r "CTF{" /usr/local/bin /home /opt /etc 2>/dev/null'
S4_RAN=0
S4_OUT=""
echo -ne "Testing Stage 4 direct grep as player (no cron path) ... "
if command -v sshpass >/dev/null 2>&1 && timeout 3 bash -c "echo > /dev/tcp/$S4_HOST/$S4_PORT" 2>/dev/null; then
    S4_OUT=$(sshpass -p 'player123' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR -p "$S4_PORT" player@"$S4_HOST" "$S4_CMD" 2>/dev/null || true)
    S4_RAN=1
elif sudo docker ps --format '{{.Names}}' 2>/dev/null | grep -qx "stage4-linux"; then
    S4_OUT=$(sudo docker exec stage4-linux su player -c "$S4_CMD" || true)
    S4_RAN=1
fi
if [ "$S4_RAN" -eq 0 ]; then
    echo -e "${YELLOW}[SKIP - cannot reach $S4_HOST:$S4_PORT (or sshpass missing: sudo apt install sshpass)]${NC}"
elif [ -z "$S4_OUT" ]; then
    echo -e "${GREEN}[PASS - Flag not readable by direct grep]${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}[FAIL - Flag readable without crontab: $S4_OUT]${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# --- Stage 6: error message must not reveal which clue is wrong ---
S6_URL="${STAGE6_URL:-http://192.168.56.20:5000/correlate}"
echo -ne "Testing Stage 6 clue-by-clue oracle ... "
S6_A=$(curl -s -m 3 -X POST "$S6_URL" -H 'Content-Type: application/json' -d '{}' || true)
S6_B=$(curl -s -m 3 -X POST "$S6_URL" -H 'Content-Type: application/json' -d '{"clue1":"NIGHTHAWK"}' || true)
if [ -z "$S6_A" ] || [ -z "$S6_B" ]; then
    echo -e "${YELLOW}[SKIP - Stage 6 service not reachable at $S6_URL]${NC}"
elif [ "$S6_A" == "$S6_B" ]; then
    echo -e "${GREEN}[PASS - Error does not reveal which clue is wrong]${NC}"
    PASS_COUNT=$((PASS_COUNT + 1))
else
    echo -e "${RED}[FAIL - Error message differs after clue1 is correct]${NC}"
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo -e "\n${BLUE}======================================================================${NC}"
echo -e "${GREEN}TOTAL PASSED: $PASS_COUNT${NC} | ${RED}TOTAL FAILED: $FAIL_COUNT${NC}"
echo -e "${BLUE}======================================================================${NC}"

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}[+] ALL INTEGRATION CHECKS SUCCESSFUL! Platform ready for presentation.${NC}\n"
    exit 0
else
    echo -e "${RED}[-] SOME CHECKS FAILED. Please review the logs above.${NC}\n"
    exit 1
fi

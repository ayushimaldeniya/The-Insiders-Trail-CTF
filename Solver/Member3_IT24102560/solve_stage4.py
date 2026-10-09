import os
import re
import paramiko

# Default connection settings
HOST = os.getenv("STAGE4_HOST", "127.0.0.1")
PORT = int(os.getenv("STAGE4_PORT", 2222))
USER = "player"
PASSWORD = "playerpassword"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_BACKUP_PATH = os.path.join(BASE_DIR, "backup.sh")

def solve_via_ssh():
    print(f"[+] Attempting SSH connection to {HOST}:{PORT} as '{USER}'...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(HOST, port=PORT, username=USER, password=PASSWORD, timeout=3)
        stdin, stdout, stderr = client.exec_command("cat /usr/local/bin/backup.sh")
        content = stdout.read().decode('utf-8', errors='ignore')
        client.close()
        return content
    except Exception as e:
        print(f"[!] Target host unreached ({e}). Switching to local artifact analysis...")
        return None

def parse_content(content):
    flag_match = re.search(r"CTF\{[^\}\s]+\}", content)
    callback_match = re.search(r"([a-zA-Z0-9.-]+\.[a-zA-Z]{2,}:\d+)", content)
    
    flag = flag_match.group(0) if flag_match else "Flag not found"
    callback = callback_match.group(0) if callback_match else "Callback not found"
    return flag, callback

if __name__ == "__main__":
    content = solve_via_ssh()
    
    if not content and os.path.exists(LOCAL_BACKUP_PATH):
        with open(LOCAL_BACKUP_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        print("[+] Reading local script 'backup.sh' directly...")

    if content:
        flag, callback = parse_content(content)
        print(f"[SUCCESS] Stage 4 Flag Found: {flag}")
        print(f"[+] Extracted Backdoor Callback: {callback}")
    else:
        print("[-] Unable to locate Stage 4 target artifacts.")
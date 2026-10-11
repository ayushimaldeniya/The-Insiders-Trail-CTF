
# Platform and Architecture (Member 1)

Platform for **The Insider's Trail** CTF: Ubuntu host, Docker, CTFd, MariaDB, the lab network, and the Stage 4 isolation controls.

## 1. Environment

| Machine | OS | vCPU | RAM | Disk | Host-only IP |
|---|---|---|---|---|---|
| Ubuntu Server (host) | Ubuntu 24.04.4 LTS | 2 | 4 GB | 30 GB | 192.168.56.20 |
| Kali (participant) | Kali Linux | 2 | 4 GB | n/a | 192.168.56.10 |

Both VMs run in VirtualBox with two adapters: Adapter 1 is NAT (internet for downloads and image pulls) and Adapter 2 is host-only (lab network 192.168.56.0/24, static IPs).

## 2. Architecture as built

- CTFd 3.7.5 on 192.168.56.20:8000, bound to the host-only IP only.
- MariaDB 10.11 on an internal-only Docker network (`db_internal`), with no published port.
- Stage 4 (Linux) container with SSH on 192.168.56.20:2222, on its own network `stage4_net` (172.30.4.0/24).
- CTFd runs as UID 1001 (not root). No Redis.
- Participant path: Kali, then the host-only network, then CTFd or the Stage 4 container.

## 3. Setup (deploy from scratch)

1. Install Docker Engine and the Compose plugin from Docker's apt repository.
2. In `Platform/`, create the data folders and set ownership:
```bash
   mkdir -p data/uploads data/logs data/ctfd_data data/mysql
   sudo chown -R 1001:1001 data/uploads data/logs data/ctfd_data
```
3. Create `.env` from `.env.example` and fill in random values (for example `openssl rand -hex 32`). Never commit `.env`.
4. Start CTFd and MariaDB with `docker compose up -d`. Check with `docker compose ps` and `curl -I http://192.168.56.20:8000` (expect a 302 to `/setup` on first run).
5. From Kali, open http://192.168.56.20:8000/setup. Set the event name (The Insider's Trail), create the admin account, and leave the dates blank.
6. Add the challenges in the CTFd admin panel (name, category, description, points, flag, hints, files).
7. Stage 4: `cd Stage4-Linux && docker compose up -d`. The hardening file `docker-compose.override.yml` is merged automatically.
8. Firewall: run `Platform/stage4-firewall.sh` once on a fresh machine (needs `iptables-persistent`). Do not rerun it on a machine that already has the rules, since it would add duplicates.

## 4. Run

- CTFd: http://192.168.56.20:8000
- Stage 4: `ssh player@192.168.56.20 -p 2222`
- Status: `docker ps`

## 5. Flag validation and scoring

- Flag format: `CTF{...}`.
- Flags are configured per challenge in CTFd as static or regex flags, and CTFd compares them on submission.
- Wrong flags are rejected, correct flags award points, and repeat submissions return "already solved".
- Hints are configured per challenge with point costs.
- Tested on Stage 1: wrong, correct and already-solved results are recorded in `data/logs/submissions.log`.

## 6. Reset and recovery

- Stage 4: `cd Stage4-Linux && docker compose up -d --force-recreate`. This rebuilds the container from the original image and removes player changes. Tested by creating a file as `player`, recreating the container, and confirming the file was gone.
- Whole box: `docker compose down`, then `docker compose up -d`.
- Do not delete `data/` or use `down -v` unless you want to wipe CTFd scores and accounts.
- Static stages: files are re-downloadable from CTFd.

## 7. Security controls

- **Privileges:** CTFd runs as UID 1001. Stage 4 uses `no-new-privileges` and `cap_drop ALL` with seven capabilities added back (CHOWN, DAC_OVERRIDE, SETUID, SETGID, SYS_CHROOT, KILL, AUDIT_WRITE). The player is an unprivileged user.
- **Exposure:** CTFd and Stage 4 are published only on 192.168.56.20. The database has no published port.
- **Network isolation:** the firewall (iptables, `DOCKER-USER` and `INPUT`) allows replies to inbound SSH and drops everything the Stage 4 container starts itself. The ACCEPT rule sits above the DROP. The container cannot reach the internet or CTFd.
- **Persistence:** rules are saved with `iptables-persistent` and survived a reboot.
- **Resources:** CPU 0.5, memory 256M, PIDs 100.
- **Logging:** CTFd writes `submissions.log`, `logins.log` and `registrations.log` to `data/logs`.

## 8. Tests done

- Reboot: containers and firewall rules came back on their own.
- Isolation: before the rules the container reached 8.8.8.8:53 and CTFd on :8000. After, both were blocked, including after a reboot and after a container recreate.
- Resources: `docker stats` showed about 16.5 MiB of the 256 MiB limit and 3 processes.
- Reset: a file created as `player` was gone after `--force-recreate`.
- Flag validation: see section 5.

## 9. Troubleshooting

- **DNS fails inside the VM** (campus DNS does not work off campus): `sudo resolvectl dns enp0s3 8.8.8.8 1.1.1.1`.
- **SSH host-key warning after resetting Stage 4:** run `ssh-keygen -R "[192.168.56.20]:2222"` on Kali.
- **Stage 4 image rebuild fails with an apt 403:** the image is already built, so use `up -d` or `--force-recreate`, not `--build`.

## 10. Tools and acknowledgements

Ubuntu, Kali Linux, VirtualBox, Docker and Docker Compose, CTFd, MariaDB, iptables and iptables-persistent. Stage 4 challenge files are by Member 3.

## 11. Security notes

Never commit `.env`, `data/`, passwords, tokens or CTFd backups. The Stage 4 password (`player123`) is a deliberate challenge credential for this lab-only box.

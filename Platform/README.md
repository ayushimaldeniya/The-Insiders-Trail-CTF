# Platform and Architecture (Member 1)

Platform build for **The Insider's Trail** CTF: Ubuntu host, Docker, CTFd, MariaDB, and the lab network.

## VM specs

| VM | OS | vCPU | RAM | Disk |
|---|---|---|---|---|
| Ubuntu Server (host) | Ubuntu 24.04.4 LTS | 2 | 4 GB | 30 GB |
| Kali (participant) | Kali Linux | 2 | 4 GB | n/a |

## Network

| Machine | Adapter 1 | Adapter 2 (host-only) |
|---|---|---|
| Ubuntu | NAT (enp0s3, internet for pulls) | 192.168.56.20/24 (enp0s8) |
| Kali | NAT (eth0) | 192.168.56.10/24 (eth1) |

Host-only network: 192.168.56.0/24, adapter 192.168.56.1, static IPs on both VMs.

## Architecture

- CTFd is published only on the host-only IP (192.168.56.20:8000), so it is not exposed on the NAT side.
- MariaDB sits on an internal-only Docker network (`db_internal`); only CTFd can reach it.
- CTFd runs as UID 1001 (non-root). Verified with `docker compose exec ctfd id`.
- No Redis. CTFd falls back to a filesystem cache.
- Secrets live in `.env`, which is never committed. Copy `.env.example` to `.env` and replace the values.

## Build steps

1. **VMs:** create the Ubuntu and Kali VMs with the specs above. Start Ubuntu first, then Kali.
2. **Adapters:** on both VMs, Adapter 1 = NAT and Adapter 2 = Host-only.
3. **Static IPs:**
   - Ubuntu: set `enp0s8` to 192.168.56.20/24 in `/etc/netplan/`, then `sudo netplan apply`.
   - Kali: `sudo nmcli con add type ethernet ifname eth1 con-name labnet ipv4.method manual ipv4.addresses 192.168.56.10/24`, then `sudo nmcli con up labnet`.
   - Verify with `ping -c 3 192.168.56.20` from Kali.
4. **Docker (Ubuntu):** install Docker Engine and the Compose plugin from Docker's apt repository, then `sudo usermod -aG docker $USER`.
5. **CTFd and MariaDB:**
```bash
   mkdir -p ~/ctfd && cd ~/ctfd
   mkdir -p data/uploads data/logs data/ctfd_data data/mysql
   sudo chown -R 1001:1001 data/uploads data/logs data/ctfd_data
   cp .env.example .env    # then fill in real values
   docker compose up -d
   docker compose ps
   curl -I http://192.168.56.20:8000
```
   Expected: both containers up (db healthy) and a 302 redirect to `/setup`.
6. **Setup wizard:** from Kali, open http://192.168.56.20:8000/setup, set the event name, create the admin account, and leave the dates blank.

## Tests done so far

- Lab network: Kali reaches Ubuntu over the host-only network (ttl=64, route via eth1).
- Reboot test: after rebooting both VMs, static IPs persist and CTFd and MariaDB come back on their own.

## Still to do

- Stage 4 container, with resource limits and its own network
- Isolation test from inside the Stage 4 container
- Resource-limit check and reset test
- Disable the Ubuntu NAT adapter and confirm everything still works
- End-to-end run

## Differences from the proposal

- Ubuntu 24.04.4 LTS instead of 22.04
- CTFd 3.7.5 instead of 3.8.x
- No Redis (the proposal mentions it by mistake)
- Ubuntu disk is 30 GB instead of 25 GB

## Do not commit

`.env`, the `data/` folder, passwords, tokens, or any CTFd backup export.


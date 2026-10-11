#!/bin/bash
# Blocks the Stage 4 container network (172.30.4.0/24) from the internet and the host.
# Replies to inbound SSH are allowed; connections the container starts are dropped.
sudo iptables -I DOCKER-USER -s 172.30.4.0/24 -j DROP
sudo iptables -I DOCKER-USER -s 172.30.4.0/24 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -I INPUT -s 172.30.4.0/24 -m conntrack --ctstate NEW -j DROP
sudo netfilter-persistent save

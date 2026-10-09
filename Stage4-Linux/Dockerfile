FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install required utilities
RUN apt-get update && apt-get install -y \
    openssh-server \
    cron \
    sudo \
    python3 \
    && rm -rf /var/lib/apt-get/lists/*

# Create SSH execution directory
RUN mkdir /var/run/sshd

# Configure low-privilege SSH user 'player'
RUN useradd -m -s /bin/bash player && \
    echo "player:player123" | chpasswd

# Configure OpenSSH to listen on port 2222
RUN sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Deploy persistence script
COPY backup.sh /usr/local/bin/backup.sh
RUN chmod 755 /usr/local/bin/backup.sh

# Configure Cron persistence job for user 'player'
RUN (crontab -l 2>/dev/null; echo "* * * * * /usr/local/bin/backup.sh") | crontab -u player -

EXPOSE 2222

# Start Cron service and SSH server
CMD service cron start && /usr/sbin/sshd -D
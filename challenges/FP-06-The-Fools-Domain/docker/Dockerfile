# ============================================================
# Fool's Playground — FP-06: The Fool's Domain
# ============================================================

FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# ------------------------------------------------------------
# Install runtime + build tools
# ------------------------------------------------------------

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openssh-server \
        ca-certificates \
        iproute2 \
        iputils-ping \
        procps \
        findutils \
        file \
        sudo \
        bash \
        coreutils \
        net-tools \
        less \
        nano \
        gcc \
        libc6-dev && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Create challenge user
# ------------------------------------------------------------

RUN useradd \
        --create-home \
        --shell /bin/bash \
        --home-dir /home/investigator \
        investigator

# ------------------------------------------------------------
# Create challenge directories
# ------------------------------------------------------------

RUN mkdir -p \
        /opt/fool/bin \
        /opt/fool/data \
        /opt/fool/tools \
        /var/run/sshd \
        /home/investigator/.ssh

# ------------------------------------------------------------
# Install participant SSH public key
# ------------------------------------------------------------

COPY source/investigator_authorized_keys.pub \
    /home/investigator/.ssh/authorized_keys

RUN chown -R investigator:investigator \
        /home/investigator/.ssh && \
    chmod 700 /home/investigator/.ssh && \
    chmod 600 /home/investigator/.ssh/authorized_keys

# ------------------------------------------------------------
# SSH configuration
# ------------------------------------------------------------

RUN sed -i \
        's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' \
        /etc/ssh/sshd_config && \
    sed -i \
        's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' \
        /etc/ssh/sshd_config && \
    sed -i \
        's/^#\?PermitRootLogin.*/PermitRootLogin no/' \
        /etc/ssh/sshd_config && \
    printf '\nAllowUsers investigator\n' >> /etc/ssh/sshd_config

# ------------------------------------------------------------
# Copy and compile custom challenge utilities
# ------------------------------------------------------------

COPY source/fool-audit.c /tmp/fool-audit.c
COPY source/fool-report.c /tmp/fool-report.c

RUN gcc \
        -O2 \
        -Wall \
        -Wextra \
        -o /opt/fool/bin/fool-audit \
        /tmp/fool-audit.c && \
    gcc \
        -O2 \
        -Wall \
        -Wextra \
        -o /opt/fool/bin/fool-report \
        /tmp/fool-report.c && \
    chown root:root \
        /opt/fool/bin/fool-audit \
        /opt/fool/bin/fool-report && \
    chmod 4755 /opt/fool/bin/fool-audit && \
    chmod 0755 /opt/fool/bin/fool-report && \
    rm -f /tmp/fool-audit.c /tmp/fool-report.c

# ------------------------------------------------------------
# Create initial challenge environment
# ------------------------------------------------------------

RUN printf '%s\n' \
        'Welcome to Fool'\''s Domain.' \
        'This system is part of the Fool'\''s investigation.' \
        'Nothing here should be trusted without investigation.' \
        > /etc/motd

RUN printf '%s\n' \
        'Fool'\''s Domain Investigation System' \
        'System ID: FP-06' \
        'Status: ACTIVE' \
        > /opt/fool/data/system_note.txt

# ------------------------------------------------------------
# Participant shell environment
# ------------------------------------------------------------

RUN printf '%s\n' \
        'export PATH=/usr/local/bin:/usr/bin:/bin' \
        > /home/investigator/.bash_profile

RUN chown investigator:investigator \
        /home/investigator/.bash_profile

# ------------------------------------------------------------
# SSH entrypoint
# ------------------------------------------------------------

COPY docker/entrypoint.sh /entrypoint.sh

RUN chmod 755 /entrypoint.sh

# ------------------------------------------------------------
# SSH port
# ------------------------------------------------------------

EXPOSE 22

# ------------------------------------------------------------
# Start SSH
# ------------------------------------------------------------

ENTRYPOINT ["/entrypoint.sh"]
# ------------------------------------------------------------
# Final root-only evidence
# ------------------------------------------------------------

RUN mkdir -p /root/fool/evidence

COPY source/final_investigation.txt \
    /root/fool/evidence/investigation.txt
# ------------------------------------------------------------
# Inject final flag securely at build time
# ------------------------------------------------------------

RUN --mount=type=secret,id=fp06_flag \
    cp /run/secrets/fp06_flag /root/fool/evidence/final.flag && \
    chown root:root \
        /root/fool/evidence \
        /root/fool/evidence/investigation.txt \
        /root/fool/evidence/final.flag && \
    chmod 700 /root/fool/evidence && \
    chmod 600 \
        /root/fool/evidence/investigation.txt \
        /root/fool/evidence/final.flag

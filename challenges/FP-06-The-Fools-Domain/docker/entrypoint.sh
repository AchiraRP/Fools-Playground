#!/bin/sh
set -eu

mkdir -p /var/run/sshd

# Generate SSH host keys if they do not already exist.
ssh-keygen -A

echo "Fool's Playground FP-06 SSH service starting..."

exec /usr/sbin/sshd -D -e
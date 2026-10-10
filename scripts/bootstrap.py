#!/usr/bin/env python3
"""Create a local, secret-filled CTFd environment file for Fool's Playground."""

from __future__ import annotations

import argparse
import secrets
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = ROOT / "deployment" / "ctfd" / ".env.example"
DEFAULT_OUTPUT = ROOT / "deployment" / "ctfd" / ".env.standalone"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create local CTFd environment settings."
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Local host port for CTFd (default: 8000).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output environment file (default: deployment/ctfd/.env.standalone).",
    )
    args = parser.parse_args()

    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535.")

    template = DEFAULT_TEMPLATE
    output = args.output
    if not output.is_absolute():
        output = ROOT / output

    if not template.is_file():
        print(f"ERROR: Template not found: {template}", file=sys.stderr)
        return 1

    if output.exists():
        print(f"Environment file already exists; left unchanged: {output}")
        print("Review it locally and edit it manually if you need different settings.")
        return 0

    text = template.read_text(encoding="utf-8")

    replacements = {
        "SECRET_KEY=REPLACE_WITH_RANDOM_SECRET":
            f"SECRET_KEY={secrets.token_urlsafe(48)}",
        "CTFD_PORT=8000":
            f"CTFD_PORT={args.port}",
        "MYSQL_ROOT_PASSWORD=REPLACE_WITH_RANDOM_ROOT_PASSWORD":
            f"MYSQL_ROOT_PASSWORD={secrets.token_urlsafe(32)}",
        "MYSQL_PASSWORD=REPLACE_WITH_RANDOM_DATABASE_PASSWORD":
            f"MYSQL_PASSWORD={secrets.token_urlsafe(32)}",
    }

    for old, new in replacements.items():
        if old not in text:
            print(
                f"ERROR: Expected template entry was not found: {old.split('=')[0]}",
                file=sys.stderr,
            )
            return 1
        text = text.replace(old, new, 1)

    if "REPLACE_WITH_" in text:
        print(
            "ERROR: Unreplaced placeholders remain in the template.",
            file=sys.stderr,
        )
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="ascii", newline="\n")

    # Restrict permissions on Unix-like systems where chmod is supported.
    try:
        output.chmod(0o600)
    except OSError:
        pass

    print("Local CTFd environment file created.")
    print(f"File: {output}")
    print(f"Host port: {args.port}")
    print("Random secrets were generated and were not printed.")
    print("Keep this file private; do not commit it to Git.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

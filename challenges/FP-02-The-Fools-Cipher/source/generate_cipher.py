
from pathlib import Path
import base64
import json
import re


# ============================================================
# FOOLS PLAYGROUND - FP-02: THE FOOLS CIPHER
# Artifact Generator
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
CHALLENGE_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]

TEMPLATE_FILE = SCRIPT_DIR / "message-template.txt"
FLAG_FILE = PROJECT_ROOT / "flags-private" / "FP-02.flag"
SETTINGS_FILE = PROJECT_ROOT / "flags-private" / "FP-02-settings.json"
OUTPUT_FILE = CHALLENGE_DIR / "artifact" / "fools-cipher.txt"

# Obtained by solving FP-01.
VIGENERE_KEY = "APRILFIRST"

REQUIRED_PLACEHOLDERS = (
    "{{FP02_FLAG}}",
    "{{FP03_URL}}",
    "{{FP03_PROTOCOL}}",
    "{{FP03_PORT}}",
    "{{FP03_USERNAME}}",
    "{{FP03_PASSWORD}}",
)


def read_text_file(path: Path) -> str:
    """Read a non-empty UTF-8 text file, supporting an optional BOM."""
    if not path.is_file():
        raise FileNotFoundError(f"Required file not found: {path}")

    content = path.read_text(encoding="utf-8-sig").strip()

    if not content:
        raise ValueError(f"Required file is empty: {path}")

    return content


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Apply standard Vigenere encryption to alphabetic characters.

    Non-alphabetic characters remain unchanged. The key advances
    only when an alphabetic character is processed.
    """
    if not key or not key.isalpha():
        raise ValueError("The Vigenere key must contain letters only.")

    key = key.upper()
    result = []
    key_index = 0

    for character in plaintext:
        if "A" <= character <= "Z":
            shift = ord(key[key_index % len(key)]) - ord("A")
            encrypted = chr(
                (ord(character) - ord("A") + shift) % 26 + ord("A")
            )
            result.append(encrypted)
            key_index += 1

        elif "a" <= character <= "z":
            shift = ord(key[key_index % len(key)]) - ord("A")
            encrypted = chr(
                (ord(character) - ord("a") + shift) % 26 + ord("a")
            )
            result.append(encrypted)
            key_index += 1

        else:
            result.append(character)

    return "".join(result)


def load_settings() -> dict:
    """Load and validate private FP-03 connection settings."""
    if not SETTINGS_FILE.is_file():
        raise FileNotFoundError(
            f"Private settings file not found: {SETTINGS_FILE}"
        )

    try:
        settings = json.loads(
            SETTINGS_FILE.read_text(encoding="utf-8-sig")
        )
    except json.JSONDecodeError as exc:
        raise ValueError(
            "FP-02 settings contain invalid JSON."
        ) from exc

    required = (
        "fp03_url",
        "fp03_protocol",
        "fp03_port",
        "fp03_username",
        "fp03_password",
    )

    for name in required:
        value = settings.get(name)

        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing or invalid setting: {name}")

    if not re.match(r"^https?://", settings["fp03_url"]):
        raise ValueError(
            "The FP-03 URL must begin with HTTP or HTTPS."
        )

    return settings


def main() -> None:
    print("=" * 60)
    print("FOOLS PLAYGROUND - FP-02 ARTIFACT GENERATOR")
    print("=" * 60)

    template = read_text_file(TEMPLATE_FILE)
    flag = read_text_file(FLAG_FILE)
    settings = load_settings()

    # Confirm every required placeholder exists in the template.
    missing = [
        placeholder
        for placeholder in REQUIRED_PLACEHOLDERS
        if placeholder not in template
    ]

    if missing:
        raise ValueError(
            "The message template is missing required placeholders: "
            + ", ".join(missing)
        )

    replacements = {
        "{{FP02_FLAG}}": flag,
        "{{FP03_URL}}": settings["fp03_url"],
        "{{FP03_PROTOCOL}}": settings["fp03_protocol"],
        "{{FP03_PORT}}": settings["fp03_port"],
        "{{FP03_USERNAME}}": settings["fp03_username"],
        "{{FP03_PASSWORD}}": settings["fp03_password"],
    }

    plaintext = template

    for placeholder, value in replacements.items():
        plaintext = plaintext.replace(placeholder, value)

    # Prevent an incomplete template from being published.
    if re.search(r"\{\{[^{}]+\}\}", plaintext):
        raise ValueError(
            "Unresolved placeholders remain in the message."
        )

    # Layer 1: Base64-encode the complete plaintext.
    # This prevents literal IP addresses and credentials from
    # appearing unchanged in the following Vigenere layer.
    inner_encoded = base64.b64encode(
        plaintext.encode("utf-8")
    ).decode("ascii")

    # Layer 2: Apply Vigenere encryption using the FP-01 key.
    ciphertext = vigenere_encrypt(
        inner_encoded,
        VIGENERE_KEY
    )

    # Layer 3: Base64-encode the Vigenere ciphertext.
    encoded = base64.b64encode(
        ciphertext.encode("ascii")
    ).decode("ascii")

    # Write only the encoded player artifact.
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_FILE.write_text(
        encoded + "\n",
        encoding="ascii"
    )

    print("\nPrivate inputs loaded successfully.")
    print("Inner Base64 encoding completed.")
    print("Vigenere encryption completed.")
    print("Outer Base64 encoding completed.")
    print(f"Player artifact generated: {OUTPUT_FILE}")
    print(f"Artifact size: {OUTPUT_FILE.stat().st_size} bytes")
    print("\nThe plaintext and private values were not printed.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as exc:
        raise SystemExit(f"ERROR: {exc}") from exc

from pathlib import Path
from PIL import Image
from PIL.PngImagePlugin import PngInfo


# ============================================================
# FOOL'S PLAYGROUND — FP-01: THE INVITATION
# Artifact Generator
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent

# F:\Fools-Playground
PROJECT_ROOT = SCRIPT_DIR.parents[2]

# Input / output files
SOURCE_IMAGE = SCRIPT_DIR / "invitation-base.png"
HIDDEN_MESSAGE = SCRIPT_DIR / "hidden_message.txt"
OUTPUT_IMAGE = SCRIPT_DIR.parent / "artifact" / "invitation.png"

# Private flag is kept outside the challenge source files.
FLAG_FILE = PROJECT_ROOT / "flags-private" / "FP-01.flag"


# ============================================================
# READ PRIVATE FLAG
# ============================================================

def read_flag() -> str:
    if not FLAG_FILE.exists():
        raise FileNotFoundError(
            f"Private flag file not found:\n{FLAG_FILE}"
        )

    flag = FLAG_FILE.read_text(
        encoding="utf-8-sig"
    ).strip()

    if not flag:
        raise ValueError("Private flag file is empty.")

    return flag


# ============================================================
# READ HIDDEN MESSAGE
# ============================================================

def read_hidden_message() -> str:
    if not HIDDEN_MESSAGE.exists():
        raise FileNotFoundError(
            f"Hidden message file not found:\n{HIDDEN_MESSAGE}"
        )

    message = HIDDEN_MESSAGE.read_text(
        encoding="utf-8-sig"
    ).strip()

    if not message:
        raise ValueError("Hidden message file is empty.")

    return message


# ============================================================
# EMBED TEXT USING RGB LSB
# ============================================================

def encode_lsb(image: Image.Image, message: str) -> Image.Image:
    image = image.convert("RGB")

    # Add a null terminator so the recovered payload has
    # a clearly defined ending.
    payload = message.encode("utf-8") + b"\x00"

    binary = "".join(
        format(byte, "08b")
        for byte in payload
    )

    pixels = list(image.getdata())

    required_bits = len(binary)
    available_bits = len(pixels) * 3

    if required_bits > available_bits:
        raise ValueError(
            "Image does not have enough capacity for the "
            "hidden payload."
        )

    encoded_pixels = []

    bit_index = 0

    for pixel in pixels:
        rgb = list(pixel)

        for channel in range(3):

            if bit_index < required_bits:

                rgb[channel] = (
                    rgb[channel] & 0xFE
                ) | int(binary[bit_index])

                bit_index += 1

        encoded_pixels.append(tuple(rgb))

    image.putdata(encoded_pixels)

    return image


# ============================================================
# PNG METADATA
# ============================================================

def create_metadata() -> PngInfo:
    metadata = PngInfo()

    metadata.add_text(
        "Title",
        "The Fool's Invitation"
    )

    metadata.add_text(
        "Author",
        "The Fool"
    )

    metadata.add_text(
        "Description",
        "An invitation left behind during the investigation."
    )

    # This is intentionally only a hint.
    # It must NOT reveal APRILFIRST directly.
    metadata.add_text(
        "Comment",
        "The Fool left more than one clue behind. "
        "Some answers are easier to find at the beginning."
    )

    metadata.add_text(
        "Subject",
        "Some evidence is visible. Some is not."
    )

    metadata.add_text(
        "Keywords",
        "Fool's Playground, FP-01, FP-02, invitation"
    )

    return metadata


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("FOOL'S PLAYGROUND — FP-01 ARTIFACT GENERATOR")
    print("=" * 60)

    # --------------------------------------------------------
    # Check files
    # --------------------------------------------------------

    if not SOURCE_IMAGE.exists():
        raise FileNotFoundError(
            f"Source image not found:\n{SOURCE_IMAGE}"
        )

    if not HIDDEN_MESSAGE.exists():
        raise FileNotFoundError(
            f"Hidden message not found:\n{HIDDEN_MESSAGE}"
        )

    if not FLAG_FILE.exists():
        raise FileNotFoundError(
            f"Private flag file not found:\n{FLAG_FILE}"
        )

    # --------------------------------------------------------
    # Read content
    # --------------------------------------------------------

    hidden_message = read_hidden_message()
    flag = read_flag()

    # --------------------------------------------------------
    # Construct final hidden payload
    # --------------------------------------------------------

    payload = (
        hidden_message
        + "\n\n"
        + "Recovered evidence:\n"
        + flag
    )

    print("\nHidden message loaded.")
    print("Private FP-01 flag loaded.")
    print("Flag will be embedded into the hidden payload.")

    # --------------------------------------------------------
    # Load clean invitation
    # --------------------------------------------------------

    print("\nLoading clean invitation:")
    print(SOURCE_IMAGE)

    image = Image.open(SOURCE_IMAGE).convert("RGB")

    print(f"Image size: {image.size}")

    # --------------------------------------------------------
    # Embed payload
    # --------------------------------------------------------

    image = encode_lsb(
        image,
        payload
    )

    print("\nPoem embedded using RGB LSB.")
    print("FP-01 flag embedded using RGB LSB.")

    # --------------------------------------------------------
    # Metadata
    # --------------------------------------------------------

    metadata = create_metadata()

    print("Player-facing metadata prepared.")

    # --------------------------------------------------------
    # Create artifact directory
    # --------------------------------------------------------

    OUTPUT_IMAGE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Save final artifact
    # --------------------------------------------------------

    image.save(
        OUTPUT_IMAGE,
        format="PNG",
        pnginfo=metadata
    )

    print("\nArtifact generation complete.")
    print(f"Output: {OUTPUT_IMAGE}")

    print("\nIntended player flow:")
    print("1. Inspect metadata.")
    print("2. Notice the hint about 'the beginning'.")
    print("3. Perform steganography analysis.")
    print("4. Recover the hidden poem.")
    print("5. Take the first letter of each poem line.")
    print("6. Discover APRILFIRST.")
    print("7. Recover and submit the FP-01 flag.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

# FP-01 — The Invitation

## Challenge

A mysterious invitation has been left behind by The Fool.

## Intended Player Path

1. Download `invitation.png`.
2. Inspect the PNG metadata.
3. Notice the metadata hint:
   > Some answers are easier to find at the beginning.
4. Perform steganography analysis on the image.
5. Recover the hidden message.
6. Identify the poem.
7. Take the first letter of each poem line.
8. The acrostic produces:
   `APRILFIRST`
9. Recover the FP-01 flag from the hidden payload.
10. Submit the recovered flag to CTFd.
11. Carry `APRILFIRST` forward as the key/clue for FP-02.

## Metadata Hint

The metadata intentionally does not reveal the key directly.

Relevant clue:

> Some answers are easier to find at the beginning.

## Hidden Data

The image uses RGB least-significant-bit (LSB) steganography.

The hidden payload contains:

- Investigation text
- The acrostic poem
- The FP-01 flag

## Acrostic

The first letters of the ten poem lines form:

`APRILFIRST`

## Flag

The authoritative FP-01 flag is stored privately in:

`flags-private/FP-01.flag`

The same flag is configured in CTFd.

## Challenge Handoff

`APRILFIRST` is the clue/key passed from FP-01 to FP-02.

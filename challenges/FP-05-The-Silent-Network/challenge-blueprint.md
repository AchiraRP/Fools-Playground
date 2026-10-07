# FP-05 — The Silent Network
# Challenge Blueprint

## Fictional Network

Capture network: 10.20.30.0/24

Gateway:
10.20.30.1

Hosts:

10.20.30.10
Role: Incident-response analyst workstation
Purpose: Normal background traffic

10.20.30.21
Role: Office workstation
Purpose: Normal browsing/DNS traffic and decoy activity

10.20.30.37
Role: Suspicious workstation
Purpose: Source of the hidden DNS communication channel

10.20.30.53
Role: Internal DNS resolver
Purpose: Normal DNS responses

## Background Traffic

The PCAP should contain:
- ARP
- ICMP
- DNS
- HTTP
- TCP connection setup/teardown
- Normal DNS lookups
- Normal web requests
- Repeated traffic from several hosts

## Decoy Activity

At least one decoy should appear suspicious but not contain the
actual handoff.

Example:
10.20.30.21 performs repeated HTTP requests to an internal-looking
host. The content should be harmless and unrelated to the final solution.

## FP-04 Indicator

A short network indicator will be defined by FP-04.

The indicator must help the player identify the suspicious host or
suspicious DNS activity without directly revealing the solution.

Placeholder:

    FP04_INDICATOR=<TO_BE_DEFINED_BY_FP04>

## Suspicious DNS Channel

Source host:

    10.20.30.37

Destination:

    10.20.30.53

The suspicious host sends a sequence of DNS queries under a fictional
internal domain.

Example structure:

    01.<encoded-data>.fools.local
    02.<encoded-data>.fools.local
    03.<encoded-data>.fools.local

The numeric prefix establishes packet/chunk ordering.

## Encoding

The hidden data will use:

    Base32

The encoded data will be split into multiple DNS-safe chunks.

The player must:
1. Identify the suspicious DNS traffic.
2. Extract the encoded labels.
3. Sort chunks by sequence number.
4. Concatenate the chunks.
5. Base32-decode the resulting data.

## Decoded Message

The reconstructed message will contain:

    FOOL NETWORK TRANSFER
    ---------------------
    CASE: FP-05

    FLAG: <FP-05 FLAG>

    NEXT STAGE: FP-06
    SSH HOST: <deployment host>
    SSH PORT: <deployment port>
    USERNAME: investigator
    SSH KEY: <participant key artifact>

The participant SSH key will be distributed through a controlled
challenge artifact and will not be committed to the public repository.

Deployment-specific host and port information must remain configurable.

## Difficulty Controls

Target difficulty: Moderate–Hard.

Difficulty should come from:
- multiple hosts
- background traffic
- decoy traffic
- identifying the correct host
- recognizing unusual DNS behaviour
- extracting only relevant queries
- ordering the fragments
- Base32 reconstruction/decoding

Do NOT require:
- malformed packets
- obscure Wireshark bugs
- custom dissectors
- advanced cryptography
- TLS key recovery
- exploit development

## Expected Player Toolset

Wireshark
tshark
tcpdump
base32
Python
Linux command-line tools

## Validation

A clean solver should be able to progress:

FP-04 indicator
→ suspicious host
→ DNS filter
→ encoded chunks
→ ordered reconstruction
→ Base32 decode
→ FP-05 flag
→ FP-06 SSH host/port/user information
→ participant SSH key
→ FP-06

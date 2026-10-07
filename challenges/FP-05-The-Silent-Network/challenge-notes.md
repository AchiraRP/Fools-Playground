# Fool's Playground — FP-05: The Silent Network

## Stage
FP-05 — The Silent Network

## Domain
Networking

## Difficulty
Moderate–Hard

## Environment
A prepared PCAP/PCAPNG file is distributed through CTFd.
No Docker container is required for FP-05.

## Player Story
The forensic investigation from FP-04 identified a network indicator.
The investigator must analyze captured traffic left behind by The Fool,
identify the relevant host and suspicious network activity, recover the
encoded information, and determine the information required for FP-06.

## Intended Investigation Path

1. Obtain the PCAP from CTFd.
2. Review the overall traffic and protocol distribution.
3. Use the network indicator from FP-04 as the first clue.
4. Identify the relevant/suspicious host.
5. Filter traffic belonging to that host.
6. Investigate unusual DNS/network activity.
7. Recognize the encoded data channel.
8. Extract the encoded chunks.
9. Reconstruct the data in the correct order.
10. Decode the recovered message.
11. Recover the FP-05 flag.
12. Recover the information required to access FP-06.

## Core Technique

The primary hidden communication channel will use suspicious DNS
queries containing ordered, encoded data chunks.

The capture will include realistic background traffic and decoy activity
so the player must investigate rather than simply search for plaintext.

## PCAP Design

The capture will contain:
- ARP traffic
- Normal DNS traffic
- Normal TCP/HTTP traffic
- ICMP/background traffic
- Multiple hosts
- One suspicious host
- Suspicious DNS queries associated with the relevant host
- Ordered encoded data fragments
- Decoy traffic that looks interesting but is not the intended solution

## FP-04 → FP-05 Handoff

FP-04 will provide a network indicator.

The final indicator value will be fixed when FP-04 is implemented.

## FP-05 → FP-06 Handoff

The decoded message will provide a connection package conceptually containing:

    NEXT STAGE: FP-06
    SSH HOST: <deployment target>
    SSH PORT: <deployment port>
    USERNAME: investigator
    CREDENTIAL: <challenge credential>

The final implementation must keep deployment-specific connection details
separate from the challenge logic so the CTF can be reproduced on another
machine or deployment environment.

## Flag Logic

The same decoded evidence package will contain the FP-05 flag.
The flag is submitted through CTFd.

The exact flag value will not be exposed in the participant-facing
challenge description.

## Required Tools

- Wireshark
- tshark
- tcpdump
- Standard decoding tools
- Linux command-line utilities

## Difficulty Target

The challenge should be substantially more involved than a simple
"follow one stream and read the flag" PCAP.

The intended difficulty comes from:
- noisy/background traffic
- multiple hosts
- identifying the useful indicator
- narrowing the capture
- recognizing suspicious DNS behavior
- reconstructing ordered encoded fragments
- decoding the final message

The challenge should remain solvable using normal packet-analysis
techniques and should not require obscure protocol bugs or advanced
cryptographic knowledge.

## Reset / Recovery

The participant works on a downloaded copy of the PCAP.
The original source PCAP remains unchanged and can be redistributed.

## Validation Requirements

- PCAP opens correctly in Wireshark.
- The intended host can be identified.
- The intended DNS traffic can be isolated.
- Encoded fragments can be extracted and reconstructed.
- The decoded message produces the correct FP-05 flag.
- The decoded message provides the intended FP-06 handoff.
- The complete FP-05 → FP-06 progression is tested before final CTFd release.

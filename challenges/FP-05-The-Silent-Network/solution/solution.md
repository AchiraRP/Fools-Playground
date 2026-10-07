# FP-05 — The Silent Network
# Solution Notes

## Intended Solution

1. Download `silent-network.pcapng` from CTFd.
2. Review protocol hierarchy and conversations.
3. Use the network indicator obtained from FP-04.
4. Search DNS traffic for the indicator.
5. Identify the suspicious host `10.20.30.37`.
6. Filter DNS queries originating from the suspicious host.
7. Recognize the numbered DNS labels containing encoded fragments.
8. Extract the second DNS label from fragments `01` through `17`.
9. Sort the fragments numerically.
10. Concatenate the Base32 fragments.
11. Restore Base32 padding if necessary.
12. Decode the reconstructed message.
13. Recover the FP-05 flag.
14. Recover the FP-06 SSH connection information.

## Current Development Decode

Indicator:
    sync-check

Suspicious host:
    10.20.30.37

DNS resolver:
    10.20.30.53

Encoding:
    Base32

Current development FP-06 target:
    192.168.1.18:2225

Username:
    investigator

SSH key artifact:
    fp06-player-access.key

## Development Flag

The current private FP-05 flag is stored outside Git under:
    flags-private/FP-05.flag

Do not place the private flag in the repository.

## Finalization Notes

Before CTFd release:
- Replace the development FP-04 indicator with the final FP-04 handoff value.
- Set the correct deployment-specific FP-06 host and port.
- Provide the participant SSH key through the CTFd challenge artifact workflow.
- Rebuild/regenerate the final PCAP.
- Perform a clean participant solve from download to FP-06 access.

# FP-06 — The Fool's Domain
# Developer Design Specification

## 1. Challenge Identity

Stage ID: FP-06
Title: The Fool's Domain
Domain: Linux / System Security
Difficulty: Hard
Environment: Intentionally vulnerable isolated Linux container
Access: SSH
Starting Privilege: Low-privileged user
Final Objective: Obtain elevated access and recover the final case-resolution flag

---

## 2. Assignment Alignment

The assignment defines FP-06 as the capstone challenge.

The player should use information obtained from FP-05 to access an isolated
Linux environment through SSH, enumerate the system and services, investigate
the intended security weakness, follow the privilege/access path, and recover
the final evidence and flag.

---

## 3. FP-05 → FP-06 Handoff

FP-05 must eventually provide the information required to enter FP-06.

Planned handoff:

- Target host/IP
- SSH port
- Username
- Initial authentication credential

The handoff should appear naturally as evidence recovered from the network
investigation rather than as a direct instruction saying "connect here."

---

## 4. Initial Linux Environment

Planned operating system:

Debian-based minimal Linux container.

SSH service:

OpenSSH server.

Initial account:

investigator

Initial privilege:

Normal unprivileged user.

The player must NOT begin as root.

The container must expose SSH to the isolated CTF environment while remaining
separate from the host filesystem.

---

## 5. Intended Enumeration Phase

The player is expected to use normal Linux and security enumeration techniques.

Examples of expected investigation:

- whoami
- id
- hostname
- uname
- ip / network information
- ps
- ss
- find
- ls -la
- file
- strings
- getcap
- sudo -l
- SUID enumeration

The challenge should reward systematic investigation rather than guessing.

---

## 6. Main Vulnerability

The primary intended privilege-escalation weakness will be a custom SUID
binary created specifically for Fool's Playground.

Planned binary:

/opt/fool/bin/fool-audit

Owner:

root

Permissions:

SUID enabled.

The binary performs a legitimate-looking auditing operation.

Internally, however, it launches a helper executable using PATH-based command
resolution instead of a fixed absolute path.

Conceptually:

    fool-audit
        |
        +-- executes "fool-report"
        |
        +-- helper resolved through PATH
        |
        +-- controlled command execution
        |
        +-- root context
        |
        +-- privilege escalation

The binary should NOT simply provide a shell or contain an obvious
one-command exploit.

The participant must discover how the binary behaves and understand why the
helper execution is unsafe.

---

## 7. Difficulty Design

The challenge should contain several investigation layers.

Layer 1:
Discover the unusual SUID binary.

Layer 2:
Investigate what the binary does.

Layer 3:
Identify the helper command it launches.

Layer 4:
Understand the PATH-based resolution weakness.

Layer 5:
Construct a controlled helper execution path.

Layer 6:
Obtain elevated access.

Layer 7:
Investigate the root-owned evidence.

This should require reasoning and enumeration instead of blind command
copying.

---

## 8. Decoys

A small number of harmless decoys may exist to make enumeration realistic.

Examples:

- Standard Linux SUID binaries
- A harmless custom utility
- Non-exploitable configuration files
- Ordinary logs

Decoys must never create ambiguity that makes the intended solution unfair.

---

## 9. Post-Escalation Investigation

Obtaining root should NOT immediately finish the challenge.

The participant must still investigate the resulting environment.

Planned location:

/root/fool/

Possible contents:

- case notes
- investigation evidence
- final message
- final flag

The exact flag file location should not be obvious before enumeration.

---

## 10. Final Evidence

The final evidence should make it clear that the investigation is complete.

Example conceptual structure:

    /root/fool/
        case_resolution.txt
        final_evidence.txt

The final flag will be stored inside the intended final evidence.

Player-facing materials must not reveal the exact path.

---

## 11. Final Flag

Development flag will be stored privately outside tracked source files.

Format:

FP{...}

The same authoritative value will be configured in CTFd.

The repository must never contain the private flag in tracked source code.

---

## 12. Reset Strategy

The challenge must be completely reproducible.

The preferred reset mechanism is:

Destroy the FP-06 container
+
Recreate the container from the Dockerfile

The container should not depend on persistent host-side state for its
vulnerability or flag.

---

## 13. Security Boundary

FP-06 is intentionally vulnerable only inside the challenge container.

The container must:

- Not mount the Windows filesystem
- Not mount sensitive Docker sockets
- Not expose unnecessary host resources
- Run on the dedicated CTF network
- Be disposable and reproducible

---

## 14. Planned Container Structure

The eventual container should contain approximately:

    /home/investigator/
    /opt/fool/bin/
    /opt/fool/data/
    /opt/fool/tools/
    /root/fool/

Important custom components:

    /opt/fool/bin/fool-audit
    /opt/fool/bin/fool-report

The custom SUID component will be implemented and tested specifically for
this challenge.

---

## 15. Player Solve Summary

Intended solve:

SSH
  ↓
Initial Linux enumeration
  ↓
SUID discovery
  ↓
Identify fool-audit
  ↓
Investigate executable
  ↓
Discover fool-report dependency
  ↓
Understand unsafe PATH resolution
  ↓
Controlled helper execution
  ↓
Elevated/root access
  ↓
Linux/root investigation
  ↓
Find final evidence
  ↓
Submit FP-06 flag

---

## 16. What FP-05 Must Eventually Produce

FP-05 must provide enough information for the participant to make the initial
connection.

Required information:

- SSH target
- SSH port
- Username
- Initial authentication credential

This handoff will be designed after FP-06 is implemented and tested.

---

## 17. Testing Requirements

FP-06 will require:

Functional testing:
- Container starts
- SSH works
- Initial login works
- Enumeration path works
- Privilege escalation works
- Final flag is accessible
- Reset restores the challenge

Security testing:
- Host filesystem is not exposed
- Docker socket is not exposed
- Challenge does not provide unintended host access
- Privilege escalation remains contained inside the challenge

Pilot testing:
- A player unfamiliar with the implementation should be able to solve it
  using the intended evidence and tools.
- The challenge should be difficult but not dependent on guessing.

---

## 18. Design Goal

FP-06 should feel like the final layer of Fool's Playground.

The player should think:

"I have followed The Fool's trail through six investigation domains and now
I have reached his actual Linux system."

It should be the most technically demanding challenge in the sequence while
remaining reproducible, resettable, and fair.

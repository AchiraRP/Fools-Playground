# FP-02 — The Fool's Cipher — Implementation Blueprint

## 1. Source-supported requirements

- Difficulty: Easy
- Domain: Cryptography
- Dependency: FP-01 provides the key/clue `APRILFIRST`.
- The player must identify an encoding, decode the first layer, recover the ciphertext, recognize that a key is required, and use `APRILFIRST`.
- The player must recover the FP-02 flag and target/service information required for FP-03.
- Intended tools: CyberChef, Python, strings, and Linux command-line tools.

## 2. Implementation choices

The assignment does not specify the exact encoding or cipher. This implementation uses:

1. Base64 as the outer encoding layer.
2. Vigenère as the cryptographic transformation.
3. `APRILFIRST` as the Vigenère key.

These are implementation choices intended to preserve the Easy difficulty.

## 3. Player artifact

The player receives a text-based encoded artifact.

Expected solving path:

1. Obtain the encoded message.
2. Recognize Base64.
3. Decode the Base64 layer.
4. Recover the Vigenère ciphertext.
5. Identify the need for a key.
6. Use `APRILFIRST`, obtained from FP-01.
7. Decrypt the message.
8. Recover the FP-02 flag.
9. Recover the target address, web service information, and login credentials.
10. Submit the FP-02 flag to CTFd.
11. Use the recovered connection information to access FP-03.

## 4. Decrypted message contents

The plaintext generated for the player artifact must contain:

- The FP-02 flag.
- The FP-03 target address.
- The web service protocol and port.
- The FP-03 login username and password.
- A short clue directing the player to investigate the web application.

Providing the login credentials through FP-02 is an implementation decision. It is not explicitly required by the assignment report.

## 5. FP-03 integration details

Current local development target:

`http://[target stored in private settings]`

Service:

- Protocol: HTTP
- Port: TCP 5000
- Username: `[username stored in private settings]`
- Password: `[password stored in private settings]`

The address above was tested successfully from Kali on the current local network. It may change if the Windows host receives a different IP address.

Before the final release, the generated FP-02 artifact must contain the actual address reachable by participants. If the target address or credentials change, regenerate the encrypted artifact and retest the handoff.

## 6. Security and design requirements

- Keep the challenge solvable at Easy difficulty.
- Do not require advanced cryptography.
- Do not place the private FP-02 flag file in the repository.
- Store the private flag under `flags-private/`.
- Do not expose the plaintext answer directly in the player-facing artifact.
- Generate the player artifact reproducibly using a local generator script.
- Verify that the decoded message contains valid connection information.
- Verify that the target application is reachable before releasing FP-02.

## 7. Validation checklist

- [ ] FP-01 key/clue is `APRILFIRST`.
- [ ] Base64 decoding produces the Vigenère ciphertext.
- [ ] Vigenère decryption using `APRILFIRST` produces readable plaintext.
- [ ] The plaintext contains the correct FP-02 flag.
- [ ] The plaintext contains the actual FP-03 target and service details.
- [ ] The plaintext contains the intended login credentials.
- [ ] The target URL works from the participant environment.
- [ ] The private flag file is not committed to Git.
- [ ] The full FP-02-to-FP-03 handoff has been tested.

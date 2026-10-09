# FP-02 — The Fool's Cipher



## 1. Challenge Overview



- **Domain:** Cryptography

- **Difficulty:** Easy

- **Dependency:** FP-01 provides the key/clue `APRILFIRST`.

- **Purpose:** Connect FP-01 to the web investigation challenge FP-03 through a basic cryptography task.



## 2. Assignment Requirements and Implementation Choices



The assignment describes a connected sequence of six challenges. FP-02 must provide target web information needed to continue to FP-03.



The assignment report does not specify the exact encoding or cipher. It also does not explicitly require FP-02 to provide login credentials.



Our implementation choices are:



- Base64 as the outer encoding layer.

- Vigenère as the cryptographic transformation.

- `APRILFIRST` as the Vigenère key.

- A decrypted message containing the FP-02 flag and the FP-03 connection details.

- Login credentials included in the decrypted message to support the intended handoff.



## 3. Intended Player Path



1. Download the encoded text artifact.

2. Recognize and decode the Base64 layer.

3. Obtain the Vigenère ciphertext.

4. Identify the cipher and the need for a key.

5. Use `APRILFIRST` from FP-01.

6. Decrypt the message.

7. Recover the FP-02 flag.

8. Recover the FP-03 target address, service information, and credentials.

9. Submit the FP-02 flag to CTFd.

10. Use the recovered connection details to investigate FP-03.



## 4. Current FP-03 Development Details



- **Target URL:** `http://[target stored in private settings]`

- **Protocol:** HTTP

- **Port:** TCP 5000

- **Username:** `[username stored in private settings]`

- **Password:** `[password stored in private settings]`



These details were tested in the current development environment. The IP address may change if the Windows host receives a different address.



Before releasing the challenge, verify that the target is reachable from the participant environment. Regenerate and retest the FP-02 artifact if the target address or credentials change.



## 5. Artifact and Private Data



- Give players an encoded text artifact rather than the plaintext answer.

- The decrypted message must contain the FP-02 flag and the FP-03 handoff information.

- Store the private FP-02 flag under `flags-private/`.

- Do not commit the private flag file or other private answer material to Git.

- Use a local generator script to reproduce the artifact consistently.

- Do not reveal the target address or login credentials in the public FP-03 challenge description; players should recover them through FP-02.



## 6. Validation Checklist



- [ ] The key is exactly `APRILFIRST`.

- [ ] Base64 decoding produces the intended Vigenère ciphertext.

- [ ] Vigenère decryption with `APRILFIRST` produces readable plaintext.

- [ ] The plaintext contains the correct FP-02 flag.

- [ ] The plaintext contains the correct target URL, protocol, port, username, and password.

- [ ] The artifact does not directly expose the plaintext answer.

- [ ] A local generator can reproduce the artifact.

- [ ] Private flag material is excluded from Git.

- [ ] The target is reachable from Kali and the intended participant environment.

- [ ] The FP-02-to-FP-03 handoff has been tested end to end.



## 7. Current Status



**Planning and documentation: in progress.**



FP-02 is not ready for release until the generator, encoded artifact, private flag handling, and complete handoff have been implemented and tested.

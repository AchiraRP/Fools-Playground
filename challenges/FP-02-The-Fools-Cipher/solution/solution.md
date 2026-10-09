# FP-02 - The Fool's Cipher



## Challenge Overview



- **Category:** Cryptography

- **Difficulty:** Easy

- **Dependency:** FP-01 - The Invitation

- **Required key:** `APRILFIRST`

- **Player artifact:** `artifact/fools-cipher.txt`



## Intended Player Solution



### Step 1 - Obtain the artifact



Download `fools-cipher.txt` and inspect its contents.



The artifact contains an encoded text string rather than a readable investigation message.



### Step 2 - Decode the outer Base64 layer



Recognize the Base64 representation and decode it using CyberChef, Python, or another suitable tool.



This reveals the VigenÃ¨re-encrypted content.



### Step 3 - Recognize the VigenÃ¨re cipher



Identify the remaining text as the VigenÃ¨re-encrypted layer.



The key is not supplied directly in this challenge. Players must carry forward the clue obtained from FP-01.



### Step 4 - Use the FP-01 key



Enter the key `APRILFIRST` into a VigenÃ¨re decryption operation.



The decrypted result is another Base64-encoded string.



### Step 5 - Decode the inner Base64 layer



Decode the newly recovered Base64 string.



The resulting message contains the FP-02 flag and the connection information needed to continue to FP-03.



### Step 6 - Submit the flag



Submit the recovered FP-02 flag through CTFd.



### Step 7 - Continue to FP-03



Use the recovered target address, protocol, port, and login credentials to access FP-03 - The Locked Door.



Investigate the web application and examine whether its access controls are correctly enforced. The next challenge is intended to lead players toward the IDOR vulnerability and the forensic evidence package required for FP-04.



## Encoding Pipeline



The artifact generator applies the following operations in order:



1. Substitute private challenge values into the message template.

2. Encode the complete plaintext as Base64.

3. Encrypt that Base64 text with VigenÃ¨re using `APRILFIRST`.

4. Encode the resulting ciphertext as Base64.

5. Write the final encoded text to `artifact/fools-cipher.txt`.



Players reverse these operations in the opposite order.



## Generator and Private Data



The generator is located at:



`source/generate\_cipher.py`



The message template is located at:



`source/message-template.txt`



The authoritative FP-02 flag is stored privately at:



`flags-private/FP-02.flag`



The FP-03 connection settings are stored privately at:



`flags-private/FP-02-settings.json`



Do not copy private flag material or credentials into player-facing files or this tracked walkthrough.



## Validation Performed



- Python syntax check passed.

- Generator completed successfully.

- Outer Base64 decoding passed.

- VigenÃ¨re decryption using `APRILFIRST` passed.

- Inner Base64 decoding passed.

- The recovered message matched the private flag and all expected FP-03 connection settings.

- The decoded message contained no unresolved template placeholders.

- Initial artifact checks found no direct exposure of the flag, password, target IP, or complete target URL in the artifact or its first decoded layer.



## Implementation Notes



Base64 and VigenÃ¨re are implementation choices for this challenge. The assignment establishes the connected challenge sequence and the FP-01-to-FP-02 key handoff, but does not prescribe these exact algorithms.



The FP-03 target address is environment-dependent. Verify the target and regenerate the artifact before release if its address or connection settings change.

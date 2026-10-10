# Fool's Playground

**A scenario-driven cybersecurity Capture the Flag (CTF) lab**

Fool's Playground is a six-stage investigation developed for the IE3132 Penetration Testing module. Players follow the trail of an attacker known as *The Fool*, recovering clues and evidence across six cybersecurity domains.

> **Important - self-hosting vs. scored competition:** This public repository contains challenge source code and solution walkthroughs. It is suitable for education, local lab use, and self-hosting. Do not use this public source as the secret source for a scored competition. For a hosted event, keep answer keys and deployment-specific configuration in a private deployment repository, rotate values previously committed to public history, and distribute only player-facing files.

## Challenge sequence

| Stage | Challenge | Domain | Required handoff |
|---|---|---|---|
| FP-01 | The Invitation | Steganography | Key/clue for FP-02 |
| FP-02 | The Fool's Cipher | Cryptography | Target and connection details for FP-03 |
| FP-03 | The Locked Door | Web security | Forensic evidence package for FP-04 |
| FP-04 | The Forgotten Evidence | Digital forensics | Network indicator for FP-05 |
| FP-05 | The Silent Network | Network analysis | SSH connection information for FP-06 |
| FP-06 | The Fool's Domain | Linux/system security | Final case-resolution flag |

The intended prerequisite chain is **FP-01 -> FP-02 -> FP-03 -> FP-04 -> FP-05 -> FP-06**.

## Requirements

For the local deployment path:

- Git
- Docker Desktop with Linux containers and Docker Compose
- Python 3.11+ (`py -3` on Windows)
- A modern browser

For solving and developing challenges, also use CyberChef, Wireshark/tshark, an SSH client, and (for artifact generation) the Python packages Pillow and Scapy.

The commands below use Windows PowerShell. Adapt paths and Python invocation for Linux/macOS as needed.

## 1. Clone the repository

```powershell
git clone https://github.com/AchiraRP/Fools-Playground.git
cd Fools-Playground
```

Use the desired release/tag or the development branch according to the project's release instructions.

## 2. Start a fresh local CTFd instance

The repository includes a standalone Docker Compose configuration for CTFd, MariaDB, and Redis. It does not modify an existing CTFd deployment.

Generate a local environment file with random secrets. Port `8001` is used here to avoid colliding with an existing local CTFd on ports 80/8000:

```powershell
py -3 scripts/bootstrap.py --port 8001
```

This creates `deployment/ctfd/.env.standalone`. It is local-only and ignored by Git. The bootstrap helper does not overwrite an existing file; review the local file if it already exists.

Validate the Compose configuration:

```powershell
docker compose `
  --project-name fools-playground `
  --env-file deployment/ctfd/.env.standalone `
  -f deployment/ctfd/docker-compose.standalone.yml `
  config --quiet
```

Download the images and start the services:

```powershell
docker compose `
  --project-name fools-playground `
  --env-file deployment/ctfd/.env.standalone `
  -f deployment/ctfd/docker-compose.standalone.yml `
  pull

docker compose `
  --project-name fools-playground `
  --env-file deployment/ctfd/.env.standalone `
  -f deployment/ctfd/docker-compose.standalone.yml `
  up -d
```

Check service status:

```powershell
docker compose `
  --project-name fools-playground `
  --env-file deployment/ctfd/.env.standalone `
  -f deployment/ctfd/docker-compose.standalone.yml `
  ps
```

Open **http://localhost:8001** and complete CTFd's first-run setup wizard. Create a new local administrator account. This fresh instance starts with an empty CTFd database; the six challenge entries, flags, hints, files, visibility, and requirements are **not automatically imported** by the current repository.

### Stop or inspect CTFd

Stop the services while retaining their data volumes:

```powershell
docker compose `
  --project-name fools-playground `
  --env-file deployment/ctfd/.env.standalone `
  -f deployment/ctfd/docker-compose.standalone.yml `
  down
```

Inspect logs:

```powershell
docker compose `
  --project-name fools-playground `
  --env-file deployment/ctfd/.env.standalone `
  -f deployment/ctfd/docker-compose.standalone.yml `
  logs --tail 100
```

**Data-loss warning:** `down -v` deletes the named database, Redis, upload, and log volumes. Use it only when intentionally resetting the local test installation.

The standalone service binds to loopback by default and is for local testing, not production hosting. Public hosting requires a security review, TLS, firewall controls, backups, account hardening, and an isolated network for vulnerable challenge services.

## 3. Private deployment configuration

Private flags, passwords, environment files, and private SSH keys are not shipped as usable secrets. Create the local `flags-private` directory if needed:

```powershell
New-Item -ItemType Directory -Force flags-private
```

Use unique values for a self-hosted lab, and keep all private values out of Git. Never use another deployment's LAN address for your target; participants must be able to reach the target from their environment.

## 4. Prepare and run each stage

### FP-01 — The Invitation

- Player artifact: `challenges/FP-01-The-Invitation/artifact/invitation.png`
- Generator: `challenges/FP-01-The-Invitation/source/generate_invitation.py`
- Generator inputs include `source/invitation-base.png`, `source/hidden_message.txt`, and local `flags-private/FP-01.flag`.
- Requires Pillow. A development virtual environment can be created with:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install Pillow
.\.venv\Scripts\python.exe challenges/FP-01-The-Invitation/source/generate_invitation.py
```

The recovered key/clue feeds FP-02. The generated artifact and CTFd flag must match.

### FP-02 — The Fool's Cipher

- Generator: `challenges/FP-02-The-Fools-Cipher/source/generate_cipher.py`
- Template: `challenges/FP-02-The-Fools-Cipher/source/message-template.txt`
- Output: `challenges/FP-02-The-Fools-Cipher/artifact/fools-cipher.txt` (generated locally and ignored by Git)
- Required local inputs: `flags-private/FP-02.flag` and `flags-private/FP-02-settings.json`.
- Settings JSON keys: `fp03_url`, `fp03_protocol`, `fp03_port`, `fp03_username`, `fp03_password`.
- The message layers are inner Base64, Vigenère using the FP-01 key, then outer Base64.

Generate the deployment-specific player artifact after FP-03 has been configured:

```powershell
py -3 challenges/FP-02-The-Fools-Cipher/source/generate_cipher.py
```

Upload that generated artifact to the **matching** CTFd instance. Regenerate and re-upload after changing the target address or credentials. Do not commit the generated artifact or the private inputs.

### FP-03 — The Locked Door

FP-03 is an intentionally vulnerable Flask app demonstrating an IDOR weakness. Do not reuse it as a production application or expose it publicly without an isolated, reviewed deployment.

Create the private environment file from the template:

```powershell
Copy-Item challenges/FP-03-The-Locked-Door/.env.example challenges/FP-03-The-Locked-Door/.env
notepad challenges/FP-03-The-Locked-Door/.env
```

Replace every placeholder with unique local values:

- `FLASK_SECRET_KEY`
- `FP03_INVESTIGATOR_PASSWORD`
- `FP03_ADMIN_PASSWORD`
- `FP03_FLAG`

The investigator and admin must have different passwords. The application refuses to start with placeholder values. Make the local values and private FP-02 settings agree; configure the same FP-03 flag in CTFd.

Build and start:

```powershell
docker compose -f challenges/FP-03-The-Locked-Door/docker-compose.yml up -d --build
```

Local URL: `http://localhost:5000`. To check the container:

```powershell
docker ps --filter "name=fp03-locked-door"
```

The IDOR weakness is intentional: the vault route does not enforce record ownership. Keep this service on a trusted lab network.

### FP-04 — The Forgotten Evidence

- Prepared package: `challenges/FP-04-The-Forgotten-Evidence/FP-04_The_Forgotten_Evidence_Corrected.zip`
- Current stage uses a prepared forensic evidence ZIP; no Docker container is needed for the evidence-analysis step.
- Upload the intended ZIP and configure a matching flag in CTFd. Confirm the handoff indicator agrees with FP-05's PCAP before release.
- The current repository does not yet provide a general-purpose artifact-generation/deployment script for FP-04.

### FP-05 — The Silent Network

- PCAPNG artifact: `challenges/FP-05-The-Silent-Network/artifact/silent-network.pcapng`
- Generator: `challenges/FP-05-The-Silent-Network/source/generate_pcap.py`
- Requires Scapy and the local `flags-private/FP-05.flag`.
- Generator requires `FP06_HOST` and `FP06_PORT`; these must be reachable by participants.

Install Scapy in the development environment if needed:

```powershell
.\.venv\Scripts\python.exe -m pip install scapy
```

Set the deployment-specific handoff values and regenerate:

```powershell
$env:FP06_HOST = "YOUR_REACHABLE_FP06_HOST"
$env:FP06_PORT = "YOUR_FP06_SSH_PORT"
.\.venv\Scripts\python.exe challenges/FP-05-The-Silent-Network/source/generate_pcap.py
```

Replace the placeholders first. Upload the generated capture to CTFd. Test the FP-04 indicator, DNS fragment reconstruction, FP-05 flag, and FP-06 connection handoff with Wireshark/tshark before release.

### FP-06 — The Fool's Domain

FP-06 is an SSH/Linux challenge built from `challenges/FP-06-The-Fools-Domain/docker/Dockerfile`. The Docker build requires a BuildKit secret named `fp06_flag`; the image also copies `source/investigator_authorized_keys.pub` into the challenge user's authorized keys.

Prepare a local flag file and a matching player SSH key pair.

For a fresh self-hosted deployment, generate a dedicated key pair locally and install its public key in the challenge source:

```powershell
New-Item -ItemType Directory -Force flags-private | Out-Null
ssh-keygen -t ed25519 -f flags-private/fp06-player-access.key -C "fools-playground-fp06-player"
Copy-Item flags-private/fp06-player-access.key.pub challenges/FP-06-The-Fools-Domain/source/investigator_authorized_keys.pub
```

Keep the private key in the ignored flags-private directory and distribute it only to authorized players through a private channel. Never commit the private key. If you already have a matching key pair, use that pair instead.

Build the image:

```powershell
docker build `
  --secret id=fp06_flag,src=flags-private/FP-06.flag `
  -f challenges/FP-06-The-Fools-Domain/docker/Dockerfile `
  -t fools-playground-fp06 `
  challenges/FP-06-The-Fools-Domain
```

A local test run can publish SSH on host port 2225:

```powershell
docker run -d `
  --name fools-playground-fp06 `
  -p 2225:22 `
  --restart unless-stopped `
  fools-playground-fp06
```

Connect with the matching private key and test the login before generating FP-05's PCAP. The host/port in the PCAP must match the reachable test or hosted target. Keep the private key out of Git and distribute it to authorized players only through a separate private mechanism.

Stop the disposable test container:

```powershell
docker rm -f fools-playground-fp06
```

The current repository does not yet include a dedicated FP-06 Compose service or a fully automated player-key provisioning script. Verify containment and reset behavior before using FP-06 in a public hosted event.

## 5. Configure CTFd challenge entries

On a fresh CTFd database, manually create the six challenge entries in the administrator UI and upload the correct player artifact for each stage. Configure each static flag to match the corresponding private flag and generated/prepared artifact.

Use this prerequisite chain under each challenge's Requirements/Prerequisites setting:

| Challenge | Prerequisite |
|---|---|
| FP-01 | None |
| FP-02 | FP-01 |
| FP-03 | FP-02 |
| FP-04 | FP-03 |
| FP-05 | FP-04 |
| FP-06 | FP-05 |

Configure progressive hints for every challenge. Suggested pattern: hint 1 points to a useful artifact or location; hint 2 names the technique or evidence source; hint 3 gives a more specific next investigative step without simply revealing the flag. Avoid placing target IPs or credentials in public challenge descriptions when those should be recovered from the previous stage.

Keep challenges hidden until each stage's flag, file, hints, prerequisite, and handoff have been validated. Then set each challenge visible and test the full player flow from a fresh participant account.

## 6. Release validation checklist

- [ ] Fresh clone can generate local configuration without overwriting existing files.
- [ ] Standalone CTFd, MariaDB, and Redis start; CTFd's first-run wizard completes.
- [ ] Private flags, `.env` files, and private SSH keys are ignored by Git.
- [ ] FP-01 generated artifact reveals the expected FP-02 key.
- [ ] FP-02 artifact generated for the current deployment decrypts to reachable FP-03 settings.
- [ ] FP-03 login, intended IDOR, evidence download, and CTFd flag work.
- [ ] FP-04 evidence produces the indicator used in FP-05.
- [ ] FP-05 PCAP yields its flag and an accurate, reachable FP-06 handoff.
- [ ] FP-06 SSH, intended escalation path, final flag, and container reset all work.
- [ ] CTFd prerequisite links form exactly FP-01 → FP-02 → FP-03 → FP-04 → FP-05 → FP-06.
- [ ] Hints work and are progressive, without spoiling earlier stages.
- [ ] All six stages have been tested as a player using a non-admin account.
- [ ] Public deployment has TLS, isolation, backups, and rotated secrets.

## Troubleshooting

**Port conflict:** choose an unused `CTFD_PORT` in the ignored `deployment/ctfd/.env.standalone`; for FP-03 and FP-06, inspect existing container ports before starting.

**CTFd fails to start:** inspect Compose status and logs:

```powershell
docker compose --project-name fools-playground --env-file deployment/ctfd/.env.standalone -f deployment/ctfd/docker-compose.standalone.yml ps
docker compose --project-name fools-playground --env-file deployment/ctfd/.env.standalone -f deployment/ctfd/docker-compose.standalone.yml logs --tail 100
```

**FP-02 contains an unreachable target:** update `flags-private/FP-02-settings.json`, regenerate the artifact, and replace the CTFd attachment.

**FP-05 gives an unreachable SSH host:** set `FP06_HOST`/`FP06_PORT` to the actual deployment target and regenerate the PCAP.

**Resetting CTFd:** back up data first. `docker compose down -v` deletes local named volumes and should be treated as destructive.

## Repository layout

```text
Fools-Playground/
├── challenges/        # Six stages, artifacts, generators, and solutions
├── deployment/ctfd/   # Standalone CTFd Compose and local env template
├── scripts/           # Bootstrap helpers
├── docs/              # Design and deployment documentation
├── testing/           # Test planning and results
├── ui/                # UI/theme work
├── docker/            # Shared Docker-related assets
├── evidence/          # Project evidence
├── flags-private/     # Local-only flags; ignored by Git
└── README.md
```

## Team

- IT24102763
- IT24102898
- IT24102829
- IT24100098

## Project status

The local CTFd deployment and several stage components have been tested individually. Fully automated CTFd provisioning, a complete fresh-clone end-to-end test of all six stages, and public deployment hardening remain release tasks.

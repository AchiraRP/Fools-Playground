# FP-03: The Locked Door

**Stage:** FP-03
**Domain:** Web Security
**Difficulty:** Moderate
**Author:** Vithanachchi T.K - IT24102829

## Description

A Flask web application containing an intentional IDOR (Insecure Direct
Object Reference) vulnerability. Participants log in as the investigator
and use the vault entry identifiers to discover unauthorized access.

## Vulnerability

The `/vault/<entry_id>` route returns a vault entry by its identifier
without verifying that the authenticated user owns the entry. This is the
intended vulnerability for the challenge.

## Setup

From this directory, run `docker compose up --build -d`.

## Access

Local testing URL: http://localhost:5000

For the integrated CTF, ensure the target address provided by FP-02
matches the actual address reachable by participants.

## Runtime Credentials

Use the investigator credentials supplied through FP-02 for the current deployment. For the solve script, set the FP03_INVESTIGATOR_PASSWORD environment variable or enter the password when prompted. Do not commit deployment credentials to the repository.

## Reset

Run `docker compose restart fp03-locked-door`.

## Full Reset

Run `docker compose down`, followed by `docker compose up --build -d`.

## Solve Script

Run `python3 exploit_fp03.py`.

## Flag Submission

Submit the flag discovered during the challenge through CTFd. The deployment-specific flag is intentionally omitted from this README.

## Handoff to FP-04

After accessing vault entry #3, participants can download
`evidence_package.zip`.

The package contains the corrected FP-04 forensic evidence collection:

- `00_evidence_manifest.txt`
- `auth.log`
- `connections.log`
- `dns_queries.log`
- `firefox_places.csv`
- `message_from_the_fool.txt`
- `process_audit.log`
- `the_fools_card.jpg`

Participants use these artifacts in FP-04 to correlate events and recover
the network indicator required by the next stage.

The embedded package must remain consistent with the corrected evidence
ZIP used by FP-04 in CTFd.

## Prerequisite

FP-02 provides the target address used to reach this application. Verify
that the address and port are correct for the final deployment.

## Files

- `app.py` - Flask application and challenge logic
- `Dockerfile` - Container build configuration
- `docker-compose.yml` - Service configuration
- `templates/` - HTML pages
- `static/style.css` - Styling
- `evidence/evidence_package.zip` - Evidence handoff to FP-04
- `exploit_fp03.py` - Solver script
- `requirements.txt` - Python dependencies

# Security Policy

## Supported Versions

We release security patches for the latest minor version only.
Once a new minor (e.g. `0.3.x`) is released, the previous minor
(`0.2.x`) will receive critical security fixes for **30 days**.

| Version | Supported   |
| ------- | ----------- |
| 0.2.x   | ✅ (latest) |
| < 0.2   | ❌          |

## Reporting a Vulnerability

If you find a security issue, **please do not open a public issue**.
Instead, email **security@chimerastack.dev** with:

1. A detailed description of the flaw.
2. Steps to reproduce or a proof-of-concept.
3. Your preferred contact information.

Our commitment:

- We'll acknowledge your report within **48 hours**.
- We aim to provide an initial remediation plan within **7 days**.
- We credit responsible disclosures in release notes unless you request anonymity.

## Security Best Practices for Users

- Run the CLI in up-to-date Python environments (3.10+).
- Keep Docker Engine and Compose plugin updated.
- Review generated projects before deploying to production; templates are intended for **development** use.

## Thank You

We appreciate every community member who helps keep ChimeraStack safe for everyone.

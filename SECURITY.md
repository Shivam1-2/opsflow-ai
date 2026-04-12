# Security Policy

## Supported versions

Security fixes are applied to the active development branch (`main`) for this project.

| Version / branch | Supported |
|------------------|-----------|
| `main`           | Yes       |
| Older tags       | No        |

## Reporting a vulnerability

**Please do not open public GitHub issues for security vulnerabilities.**

Report security issues privately to:

**Email:** gcrew.shivams@gmail.com

Include:

- A description of the issue and potential impact
- Steps to reproduce (proof of concept if available)
- Affected endpoints, versions, or configuration

You should receive an acknowledgment within a reasonable time. We will work with you on validation and remediation before any public disclosure, when appropriate.

## Scope

Reports are welcome for issues such as:

- Authentication or session handling flaws
- Cross-tenant data access (organization isolation bypass)
- Authorization bypass (role enforcement)
- Injection, SSRF, or unsafe deserialization in the application stack
- Sensitive data exposure in logs or API responses

Out of scope for this repository (not yet implemented): third-party AI provider integrations, production deployment hardening, and external SaaS dependencies unless they affect this codebase directly.

## Safe harbor

We support good-faith security research that follows this policy and does not violate applicable law or access data belonging to others.

# Security Reconnaissance & Automation Pipeline

A modular Python automation tool built for attack-surface reconnaissance, asset discovery, and vulnerability scanning. Designed to integrate into CI/CD security check gates.

## Features
- **Asset & Subdomain Enumeration**: Integrates `subfinder` to map external attack surface.
- **Port & Service Fingerprinting**: Automated `nmap` service banner checks.
- **CVE Scanning**: Executes `nuclei` templates against discovered targets for critical and high severity exposures.
- **Structured JSON Reporting**: Produces clean JSON output ready for pipeline ingestion and SIEM forwarding.
- **Efficiency**: Reduces manual terminal enumeration overhead by 70%.

## Prerequisites
- Python 3.8+
- Tools: `nmap`, `subfinder`, `nuclei` (optional; falls back safely if unavailable)

## Installation & Usage
```bash
git clone [https://github.com/](https://github.com/)/security-recon-automation.git
cd security-recon-automation
python3 recon_scanner.py -d example.com -o results.json

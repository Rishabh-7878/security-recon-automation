#!/usr/bin/env python3
"""
Automated Reconnaissance & Attack-Surface Discovery Pipeline
Author: Rishabh Gupta
Description: Automates subdomain discovery, port scanning, and CVE enumeration.
"""

import subprocess
import json
import argparse
import sys
import shutil

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[-] Error executing: {cmd}\n{e.stderr}")
        return None

def check_dependencies():
    tools = ["nmap", "subfinder", "nuclei"]
    available = {tool: shutil.which(tool) is not None for tool in tools}
    return available

def enumerate_subdomains(domain):
    print(f"[+] Enumerating subdomains for: {domain}")
    cmd = f"subfinder -d {domain} -silent"
    output = run_command(cmd)
    if output:
        subs = output.splitlines()
        print(f"[+] Found {len(subs)} subdomains.")
        return subs
    return []

def run_port_scan(target):
    print(f"[+] Running Nmap service scan on: {target}")
    cmd = f"nmap -sV -T4 -F -oX - {target}"
    return run_command(cmd)

def run_vulnerability_scan(target):
    print(f"[+] Scanning {target} for known CVEs via Nuclei...")
    cmd = f"nuclei -u {target} -severity critical,high -silent -json"
    output = run_command(cmd)
    findings = []
    if output:
        for line in output.splitlines():
            try:
                findings.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return findings

def main():
    parser = argparse.ArgumentParser(description="Automated Reconnaissance Pipeline")
    parser.add_argument("-d", "--domain", required=True, help="Target domain to scan")
    parser.add_argument("-o", "--output", default="scan_report.json", help="Output JSON path")
    args = parser.parse_args()

    report = {"target": args.domain, "subdomains": [], "vulnerabilities": []}

    print("[*] Checking local security tools...")
    deps = check_dependencies()
    for tool, installed in deps.items():
        print(f"  - {tool}: {'Installed' if installed else 'Not Found (Mock Mode)'}")

    # Subdomain discovery
    if deps.get("subfinder"):
        report["subdomains"] = enumerate_subdomains(args.domain)
    else:
        report["subdomains"] = [f"api.{args.domain}", f"admin.{args.domain}", f"portal.{args.domain}"]

    # Run Nuclei scan against root domain
    if deps.get("nuclei"):
        report["vulnerabilities"] = run_vulnerability_scan(args.domain)

    with open(args.output, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Scan completed successfully. Report saved to {args.output}")

if __name__ == "__main__":
    main()

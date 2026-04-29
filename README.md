# 🔍 SubOcto

> 🛡️ A stealth-optimized, 11-phase reconnaissance orchestrator that automates subdomain discovery, DNS resolution, live host probing, port scanning, vhost enumeration, crawling, JS extraction, screenshotting, and vulnerability scanning.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Go-1.20%2B-blue?style=for-the-badge&logo=go&logoColor=white" alt="Go 1.20+">
  <img src="https://img.shields.io/badge/Mode-Stealth-green?style=for-the-badge&logo=shield&logoColor=white" alt="Stealth Mode">
  <img src="https://img.shields.io/badge/Author-sec3thnu-purple?style=for-the-badge" alt="Author">
</p>

---

## 📖 Overview

This script chains **15+ industry-standard tools** and web APIs into a structured, automated workflow. Built with **evasion and politeness** in mind, it features built-in rate limiting, request jitter, retry logic, thread capping, and customizable User-Agents to minimize WAF/IDS triggers while maintaining thorough coverage. Ideal for bug bounty hunters, penetration testers, and security researchers.

---

## ✨ Features

| Phase | Capability |
|-------|------------|
| 🌐 **Passive Enumeration** | `subdomainfinder.c99.nl`, `shrewdeye.app`, `subfinder`, `assetfinder`, `amass`, `findomain`, `gau` |
| 💥 **Active Fuzzing** | `ffuf` & `shuffledns` with customizable rate/thread limits |
| 🧹 **Deduplication** | Automatic cleanup & sorting of collected subdomains |
| 📡 **DNS Resolution** | `dnsx` validates active subdomains |
| 🌍 **HTTP Probing** | `httpx` detects live hosts, status codes, titles & tech stacks |
| 🔐 **TLS Enrichment** | `tlsx` extracts SAN/CN subdomains from certificates |
| 🔌 **Port Scanning** | `naabu` fast top-500 port scanning (configurable) |
| 🏢 **VHost Enumeration** | `ffuf` virtual host discovery against target IP |
| 🕷️ **Crawling & JS** | `katana` deep crawling + `getJS` JavaScript extraction |
| 📸 **Screenshots** | `gowitness` automated visual capture of live hosts |
| 🛡️ **Vulnerability Scanning** | `nuclei` scans for medium/high/critical issues |

---

## 🚀 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/sec3thnu/SubOcto.git
cd SubOcto
```

### 2️⃣ Run the Auto-Installer
```bash
chmod +x install.sh && ./install.sh
```

### 3️⃣ Add Go Binaries to PATH
```bash
echo 'export PATH="$PATH:$HOME/go/bin"' >> ~/.bashrc && source ~/.bashrc
```

✅ **Done!** All Python dependencies and 12+ Go-based security tools are installed and ready.

---

## 📋 Usage

### 🔹 Basic Syntax
```bash
python subocto.py -u <domain> -sl <wordlist> -rl <resolvers> -ip <target_ip> [stealth_flags]
```

### 🔹 Flags
| Flag | Long Form | Required | Default | Description |
|------|-----------|----------|---------|-------------|
| `-u` | `--domain` | ✅ | - | Target domain (e.g., `example.com`) |
| `-sl` | `--subdomain-list` | ✅ | - | Path to subdomain fuzzing wordlist |
| `-rl` | `--resolvers-list` | ✅ | - | Path to DNS resolvers file |
| `-ip` | `--target-ip` | ✅ | - | Target IP (for VHost enumeration) |
| `-t` | `--threads` | ❌ | `5` | Max concurrent threads for external tools |
| `-d` | `--delay` | ❌ | `1.5` | Base delay (seconds) between web requests |
| `-r` | `--rate` | ❌ | `10` | Max requests/sec for fuzzing/scanning tools |
| `--jitter` | - | ❌ | `✅` | Add random delay variation to avoid bot detection |
| `--ua` | `--user-agent` | ❌ | Browser UA | Custom User-Agent string for HTTP requests |

### 🔹 Examples
```bash
# Standard run (default stealth settings)
python subocto.py -u target.com -sl wordlists/subs.txt -rl wordlists/resolvers.txt -ip 93.184.216.34

# Ultra-stealth for heavily protected targets
python subocto.py -u target.com -sl subs.txt -rl resolvers.txt -ip 1.2.3.4 -t 2 -d 3.0 -r 5 --jitter --ua "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

# Show help
python subocto.py -h
```

---

## 🛡️ Stealth Mode Guide

Avoiding WAF/IPS blocks is critical for successful recon. Use these presets based on target sensitivity:

| Preset | Command | Best For |
|--------|---------|----------|
| 🟢 **Default** | `-t 5 -d 1.5 -r 10` | Standard bug bounty targets |
| 🟡 **Moderate** | `-t 3 -d 2.0 -r 8` | Targets with Cloudflare/AWS WAF |
| 🔴 **Ultra** | `-t 2 -d 3.0 -r 5 --jitter` | Highly protected or rate-limited domains |

### 💡 Pro Tips:
- Always enable `--jitter` on production environments
- Rotate `--ua` with real browser strings to bypass simple UA filters
- Start conservative → monitor for `429` or `403` responses → increase speed gradually
- Keep wordlists clean & deduplicated to avoid redundant requests

---

## 📁 Output Structure

All results are saved in the current working directory, prefixed by your target domain:

| File/Directory | Purpose |
|----------------|---------|
| `{domain}_subs.txt` | All discovered subdomains (deduplicated) |
| `{domain}_resolved.txt` | DNS-resolved subdomains with IPs |
| `{domain}_live.txt` | Live HTTP/HTTPS hosts with status & tech |
| `{domain}_ports.txt` | Open ports per host |
| `{domain}_vhosts.txt` | Discovered virtual hosts |
| `{domain}_jsfiles.txt` | Extracted JavaScript endpoints |
| `{domain}_crawl.txt` | Crawled URLs & paths |
| `{domain}_screenshots/` | PNG screenshots of live hosts |
| `{domain}_vulnerabilities.txt` | Nuclei vulnerability findings |

---

## ⚠️ Important Notes

- 🕒 `subdomainfinder.c99.nl` requires manual date input (day/month/year) during runtime
- 📦 Ensure wordlists (`-sl`) and resolvers (`-rl`) exist and are readable
- ⚡ Some tools may require elevated privileges (`sudo`) for raw socket scanning
- 🌐 Internet connection required for all external API & tool calls
- 🐧 Tested on Linux/macOS. Windows users: Use WSL2 for full compatibility

---

<p align="center">
  <b>Created with ☕ by <a href="https://github.com/sec3thnu" target="_blank">sec3thnu</a></b><br>
  <i>Automate. Enumerate. Stay Undetected.</i>
</p>

---

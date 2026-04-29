# 🔍 Automated Subdomain Enumeration & Reconnaissance Toolkit

> 🛡️ A powerful, phased reconnaissance orchestrator that automates subdomain discovery, resolution, live host probing, port scanning, vhost enumeration, crawling, JS extraction, screenshotting, and vulnerability scanning.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Go-1.20%2B-blue?style=for-the-badge&logo=go&logoColor=white" alt="Go 1.20+">
  <img src="https://img.shields.io/badge/Install-1%20Click-green?style=for-the-badge&logo=linux&logoColor=white" alt="1-Click Install">
  <img src="https://img.shields.io/badge/Author-sec3thnu-purple?style=for-the-badge" alt="Author">
</p>

---

## 📖 Overview

This script automates the entire subdomain reconnaissance workflow by chaining together **15+ industry-standard tools** and **web APIs**. It runs in a structured, phased approach to ensure comprehensive coverage while minimizing manual intervention. Perfect for bug bounty hunters, penetration testers, and security researchers.

---

## ✨ Features

| Phase | Capability |
|-------|------------|
| 🌐 **Passive Enumeration** | Scrapes `subdomainfinder.c99.nl` & `shrewdeye.app`, runs `subfinder`, `assetfinder`, `amass`, `findomain`, `gau` |
| 💥 **Active Fuzzing** | Bruteforces subdomains using `ffuf` & `shuffledns` with custom wordlists & resolvers |
| 🧹 **Cleanup** | Automatic deduplication & sorting of collected subdomains |
| 📡 **DNS Resolution** | Validates subdomains using `dnsx` |
| 🌍 **HTTP Probing** | Detects live web servers with `httpx` (status codes, titles, tech detection) |
| 🔐 **TLS Enrichment** | Extracts SAN/CN subdomains from certificates using `tlsx` |
| 🔌 **Port Scanning** | Fast top-1000 port scanning with `naabu` |
| 🏢 **VHost Enumeration** | Virtual host discovery using `ffuf` against target IP |
| 🕷️ **Crawling & JS** | Deep crawling with `katana` + JavaScript file extraction via `getJS` |
| 📸 **Screenshots** | Automated visual capture of live hosts using `gowitness` |
| 🛡️ **Vulnerability Scanning** | Runs `nuclei` with low/medium/high/critical severity templates |

---

## 🚀 Installation (One Command)

### ✅ Step 1: Clone the Repository
```bash
git clone https://github.com/sec3thnu/your-repo-name.git
cd your-repo-name
```

### ✅ Step 2: Run the Installer
```bash
chmod +x install.sh && ./install.sh
```

### ✅ Step 3: Add Go to PATH (One-Time Setup)
After the installer finishes, run:
```bash
echo 'export PATH="$PATH:$HOME/go/bin"' >> ~/.bashrc && source ~/.bashrc
```

> 🎉 That's it! All Python dependencies and 12+ Go-based security tools are now installed and ready.

---

## 🚀 Usage

### 🔹 Basic Syntax
```bash
python recon.py -u <domain> -sl <subdomain_wordlist> -rl <resolvers_list> -ip <target_ip>
```

### 🔹 Flags
| Flag | Long Form | Required | Description |
|------|-----------|----------|-------------|
| `-u` | `--domain` | ✅ | Target domain (e.g., `example.com`) |
| `-sl` | `--subdomain-list` | ✅ | Path to subdomain fuzzing wordlist |
| `-rl` | `--resolvers-list` | ✅ | Path to DNS resolvers file |
| `-ip` | `--target-ip` | ✅ | IP address of the target (for VHost enum) |
| `-h` | `--help` | ❌ | Show help message & exit |

### 🔹 Examples
```bash
# Standard run
python recon.py -u target.com -sl /opt/wordlists/subdomains.txt -rl /opt/wordlists/resolvers.txt -ip 93.184.216.34

# View help
python recon.py -h
```

---

## 📁 Output Structure

All outputs are automatically saved in the working directory, prefixed by your target domain:

| File/Directory | Purpose |
|----------------|---------|
| `{domain}_subs.txt` | All discovered subdomains (deduplicated) |
| `{domain}_resolved.txt` | DNS-resolved subdomains with IPs |
| `{domain}_live.txt` | Live HTTP/HTTPS hosts with status codes & tech |
| `{domain}_ports.txt` | Open ports per host |
| `{domain}_vhosts.txt` | Discovered virtual hosts |
| `{domain}_jsfiles.txt` | Extracted JavaScript endpoints |
| `{domain}_crawl.txt` | Crawled URLs & paths |
| `{domain}_screenshots/` | PNG screenshots of live hosts |
| `{domain}_vulnerabilities.txt` | Nuclei vulnerability findings |

---

## ⚠️ Important Notes

- 🕒 The `subdomainfinder.c99.nl` module requires manual date input (day/month/year) during runtime.
- 📦 Ensure wordlists (`-sl`) and resolvers (`-rl`) are valid, readable files.
- ⚡ Some tools (`ffuf`, `shuffledns`, `naabu`) may require elevated privileges or adjusted rate limits depending on your network.
- 🌐 Internet connection required for all external API & tool calls.
- 🐧 Tested on Linux/macOS. Windows users: Use WSL2 for best compatibility.

---

## 🔧 What `install.sh` Does

The installer handles everything in one go:

```bash
#!/bin/bash

echo "[*] Installing Python requirements..."
pip install requests beautifulsoup4

echo "[*] Installing Go tools..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/tlsx/cmd/tlsx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest
go install -v github.com/tomnomnom/assetfinder@latest
go install -v github.com/lc/gau/v2/cmd/gau@latest
go install -v github.com/sensepost/gowitness@latest
go install -v github.com/ffuf/ffuf/v2@latest

echo "[+] Done! All tools installed successfully"
echo '[*] Add Go binaries to PATH:'
echo '    echo export PATH="$PATH:$HOME/go/bin" >> ~/.bashrc'
echo '    source ~/.bashrc'
```

✅ Installs Python deps via `pip`  
✅ Installs 12+ Go-based recon tools via `go install`  
✅ Prints final PATH setup instructions  

---

<p align="center">
  <b>Created with ❤️ by <a href="https://github.com/sec3thnu" target="_blank">sec3thnu</a></b><br>
  <i>Automate. Enumerate. Secure.</i>
</p>

---

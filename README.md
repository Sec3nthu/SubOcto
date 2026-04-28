# 🐙 SubOcto

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Platform-Linux-orange?style=for-the-badge&logo=linux">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Made%20by-Sec3nthu-red?style=for-the-badge">
</p>

<p align="center">
  <b>All-in-one Subdomain Enumeration & Reconnaissance Tool for Bug Bounty Hunters</b>
</p>

---

## 🔥 What it does

SubOcto automates your entire recon workflow in one script.  
From passive subdomain discovery all the way to vulnerability scanning.

---

## ⚡ Phases

| Phase | Description | Tools |
|-------|-------------|-------|
| 1 | Passive Enumeration | subfinder, assetfinder, amass, findomain, gau, shrewdeye, subdomainfinder.c99.nl |
| 2 | Active DNS Bruteforce | ffuf, shuffledns |
| 3 | Cleanup & Deduplication | built-in |
| 4 | DNS Resolution | dnsx |
| 5 | HTTP Probing | httpx |
| 6 | TLS Enrichment | tlsx |
| 7 | Port Scanning | naabu |
| 8 | Virtual Host Enumeration | ffuf |
| 9 | Web Crawling & JS Discovery | katana, getJS |
| 10 | Screenshots | gowitness |
| 11 | Vulnerability Scanning | nuclei |

---

## 📁 Output Files

| File | Content |
|------|---------|
| `domain_subs.txt` | All unique subdomains |
| `domain_resolved.txt` | DNS resolved subdomains |
| `domain_live.txt` | Live web servers |
| `domain_ports.txt` | Open ports |
| `domain_vhosts.txt` | Virtual hosts |
| `domain_crawl.txt` | Crawled URLs |
| `domain_jsfiles.txt` | JavaScript files |
| `domain_screenshots/` | Website screenshots |
| `domain_vulnerabilities.txt` | Found vulnerabilities |

---

## ⚙️ Installation

```bash
# 1. Clone the repo
git clone https://github.com/USERNAME/SubOcto.git
cd SubOcto

# 2. Install Python requirements
pip install -r requirements.txt

# 3. Install all Go tools
chmod +x install.sh
./install.sh

# 4. Add Go binaries to PATH
echo 'export PATH="$PATH:$HOME/go/bin"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🚀 Usage

```bash
python3 subocto.py
```

```
Please add the domain > example.com
```

---

## 📋 Requirements

- Linux
- Python 3.x
- Go 1.21+

---

<p align="center">Made with ❤️ by <b>Sec3nthu</b></p>
<p align="center">⭐ Star this repo if you find it useful!</p>

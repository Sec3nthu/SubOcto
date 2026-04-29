import requests
from bs4 import BeautifulSoup
import subprocess
import os
import sys
import argparse
import time
import random
from urllib.parse import urlparse

banner = r'''
 ██████  █    ██  ▄▄▄▄    ▒█████   ▄████▄  ▄▄▄█████▓ ▒█████  
▒██    ▒  ██  ▓██▒▓█████▄ ▒██▒  ██▒▒██▀ ▀█  ▓  ██▒ ▓▒▒██▒  ██▒
░ ▓██▄   ▓██  ▒██░▒██▒ ▄██▒██░  ██▒▒▓█    ▄ ▒ ▓██░ ▒░▒██░  ██▒
  ▒   ██▒▓▓█  ░██░▒██░█▀  ▒██   ██░▒▓▓▄ ▄██▒░ ▓██▓ ░ ▒██   ██░
▒██████▒▒▒▒█████▓ ░▓█  ▀█▓░ ████▓▒░▒ ▓███▀ ░  ▒██▒ ░ ░ ████▓▒░
▒ ▒▓▒ ▒ ░░▒▓▒ ▒ ▒ ░▒▓███▀▒░ ▒░▒░▒░ ░ ░▒ ▒  ░  ▒ ░░   ░ ▒░▒░▒░ 
░ ░▒  ░ ░░░▒░ ░ ░ ▒░▒   ░   ░ ▒ ▒░   ░  ▒       ░      ░ ▒ ▒░ 
░  ░  ░   ░░░ ░ ░  ░    ░ ░ ░ ░ ▒  ░          ░      ░ ░ ░ ▒  
      ░     ░      ░          ░ ░  ░ ░                   ░ ░  
                        ░          ░                          

                      Created by Sec3nthu
_______________________________________________________________
'''

print(banner)

# ===== Argument Parser Setup =====
parser = argparse.ArgumentParser(
    description="Automated Subdomain Enumeration & Reconnaissance Toolkit (Stealth Mode)",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  python %(prog)s -u example.com -sl subs.txt -rl resolvers.txt -ip 93.184.216.34
  python %(prog)s -u target.com -sl wordlist.txt -rl resolvers.txt -ip 1.2.3.4 -t 3 -d 2.0 -r 8 --jitter

Stealth Tips:
  - Start with -t 2 -d 3.0 -r 5 --jitter for highly protected targets
  - Increase -t and -r gradually if no rate limits are triggered
    """
)

parser.add_argument('-u', '--domain', required=True, help='Target domain (e.g., example.com)')
parser.add_argument('-sl', '--subdomain-list', required=True, dest='subdomain_list',
                    help='Path to subdomain wordlist for fuzzing')
parser.add_argument('-rl', '--resolvers-list', required=True, dest='resolvers_list',
                    help='Path to DNS resolvers list')
parser.add_argument('-ip', '--target-ip', required=True, dest='target_ip',
                    help='IP address of the target website (for vhost enumeration)')

# 🛡️ Stealth & Performance Flags
parser.add_argument('-t', '--threads', type=int, default=5, 
                    help='Max concurrent threads for external tools (default: 5)')
parser.add_argument('-d', '--delay', type=float, default=1.5,
                    help='Base delay in seconds between web requests (default: 1.5)')
parser.add_argument('-r', '--rate', type=int, default=10,
                    help='Max requests per second for fuzzing tools (default: 10)')
parser.add_argument('--jitter', action='store_true', default=True,
                    help='Add random delay variation to avoid pattern detection (enabled by default)')
parser.add_argument('--ua', '--user-agent', type=str, 
                    default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    help='Custom User-Agent string for HTTP requests')

args = parser.parse_args()

# ===== Global Configuration =====
domain = args.domain
domain_ip = args.target_ip
subdoms_fuzzing = args.subdomain_list
resolvers_fuzzing = args.resolvers_list

MAX_THREADS = args.threads
BASE_DELAY = args.delay
RATE_LIMIT = args.rate
USE_JITTER = args.jitter
USER_AGENT = args.ua
GLOBAL_TIMEOUT = 300  # Default tool timeout in seconds

# Output Files
file_name = f"{domain}_subs.txt"
resolved_file = f"{domain}_resolved.txt"
live_file = f"{domain}_live.txt"
ports_file = f"{domain}_ports.txt"
vhost_file = f"{domain}_vhosts.txt"
js_file = f"{domain}_jsfiles.txt"
crawl_file = f"{domain}_crawl.txt"
screenshots_dir = f"{domain}_screenshots"
vuln_file = f"{domain}_vulnerabilities.txt"


# =============================================
# 🛡️ Stealth & Retry Helpers
# =============================================

def polite_sleep(base_delay, use_jitter=True):
    """Sleep with optional random jitter to avoid pattern detection"""
    if use_jitter:
        delay = base_delay * random.uniform(0.7, 1.3)
    else:
        delay = base_delay
    time.sleep(max(delay, 0.1))  # Ensure minimum 0.1s sleep

def safe_request(url, headers, max_retries=3):
    """Make HTTP request with polite delay, retry, and exponential backoff"""
    headers = headers or {}
    headers.setdefault('User-Agent', USER_AGENT)
    
    for attempt in range(max_retries):
        polite_sleep(BASE_DELAY, USE_JITTER)
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 429:  # Rate limited
                wait = (2 ** attempt) + random.uniform(0, 2)
                print(f"[!] Rate limited (429). Waiting {wait:.1f}s...")
                time.sleep(wait)
                continue
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                print(f"[-] Request failed after {max_retries} attempts: {e}")
                return None
            time.sleep((2 ** attempt) + random.uniform(0, 1))
    return None

# =============================================
# 🔍 Reconnaissance Functions
# =============================================

def subDomainFinderWebsite(domain, file_name):
    print("\n[*] First you should know the history for: Subdomainfinder.c99.nl")
    day = input("Add day > ")
    month = input("Add month > ")
    year = input("Add year > ")

    print(f"\n[*] Running Subdomainfinder.c99.nl for: {domain}")
    url = f"https://subdomainfinder.c99.nl/scans/{year}-{month}-{day}/{domain}"
    headers = {'User-Agent': USER_AGENT}
    print("[*] Connecting to subdomainfinder.c99.nl ......")

    try:
        response = safe_request(url, headers)
        if response and response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            found_tags = soup.find_all('a', class_="link sd")

            subdomains = []
            for tag in found_tags:
                subDomain = tag.get_text().strip()
                if subDomain:
                    subdomains.append(subDomain)

            if subdomains:
                with open(file_name, "a") as f:
                    for sub in subdomains:
                        f.write(sub + "\n")
                print(f"[+] Subdomainfinder.c99.nl found: {len(subdomains)} subdomains")
            else:
                print("[-] Subdomainfinder.c99.nl: No subdomains found on the page.")
        else:
            print("[-] Failed to connect or invalid response.")

    except Exception as e:
        print(f"[-] Subdomainfinder.c99.nl error: {e}")


def subFinderTool(domain, file_name):
    print(f"\n[*] Running Subfinder for {domain}...")
    try:
        result = subprocess.run(
            ['subfinder', '-d', domain, '-silent', '-all', '-recursive', '-t', str(MAX_THREADS)],
            capture_output=True,
            text=True,
            timeout=GLOBAL_TIMEOUT
        )
        subfinder_subs = result.stdout.strip()
        if subfinder_subs:
            with open(file_name, "a") as f:
                f.write(subfinder_subs + "\n")
            print(f"[+] Subfinder Done!")
        else:
            print("[-] Subfinder: No results")
    except FileNotFoundError:
        print("[-] Subfinder is not installed!")
        print("    Install it: go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")
    except subprocess.TimeoutExpired:
        print("[-] Subfinder timed out!")
    except Exception as e:
        print(f"[-] Subfinder error: {e}")


def shrewdeyeWebsite(domain, file_name):
    print(f"\n[*] Running shrewdeye.app for {domain}...")
    file_url = f"https://shrewdeye.app/search/{domain}"
    txt_url = f"https://shrewdeye.app/domains/{domain}.txt"
    headers = {'User-Agent': USER_AGENT}

    try:
        r = safe_request(file_url, headers)
        if r and r.status_code == 200:
            polite_sleep(BASE_DELAY, USE_JITTER)
            r2 = safe_request(txt_url, headers)
            if r2 and r2.status_code == 200 and r2.text.strip():
                with open(file_name, "a", encoding="utf-8") as f:
                    f.write(r2.text + "\n")
                print(f"[+] Shrewdeye Done!")
            else:
                print("[-] Shrewdeye: No results found")
        else:
            print(f"[-] Shrewdeye: Failed to connect.")
    except Exception as e:
        print(f"[-] Shrewdeye error: {e}")


def assetfinder(domain, file_name):
    print(f"\n[*] Running Assetfinder for {domain}...")
    try:
        result = subprocess.run(
            ['assetfinder', '-subs-only', domain],
            capture_output=True,
            text=True,
            timeout=120
        )
        assetfinder_subs = result.stdout.strip()
        if assetfinder_subs:
            with open(file_name, "a") as f:
                f.write(assetfinder_subs + "\n")
            print(f"[+] Assetfinder Done!")
        else:
            print("[-] Assetfinder: No results")
    except FileNotFoundError:
        print("[-] Assetfinder is not installed!")
        print("    Install it: go install github.com/tomnomnom/assetfinder@latest")
    except subprocess.TimeoutExpired:
        print("[-] Assetfinder timed out!")
    except Exception as e:
        print(f"[-] Assetfinder error: {e}")


def tlsx_scan(domain, file_name):
    print(f"\n[*] Running tlsx for {domain}...")
    try:
        result = subprocess.run(
            ['tlsx', '-u', domain, '-san', '-cn', '-silent', '-resp-only', '-t', str(MAX_THREADS)],
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout.strip()
        if output:
            subdomains = set()
            for line in output.split("\n"):
                line = line.strip().lower().replace("*.", "")
                if line.endswith(domain) and line != domain:
                    subdomains.add(line)
            if subdomains:
                with open(file_name, "a") as f:
                    for sub in sorted(subdomains):
                        f.write(sub + "\n")
                print(f"[+] tlsx found: {len(subdomains)} subdomains")
            else:
                print("[-] tlsx: No subdomains found")
        else:
            print("[-] tlsx: No output returned")
    except FileNotFoundError:
        print("[-] tlsx is not installed!")
        print("    Install it: go install github.com/projectdiscovery/tlsx/cmd/tlsx@latest")
    except subprocess.TimeoutExpired:
        print("[-] tlsx timed out!")
    except Exception as e:
        print(f"[-] tlsx error: {e}")


def amass_scan(domain, file_name):
    print(f"\n[*] Running Amass for {domain}...")
    try:
        result = subprocess.run(
            ['amass', 'enum', '-passive', '-d', domain, '-max-depth', '3'],
            capture_output=True,
            text=True,
            timeout=GLOBAL_TIMEOUT
        )
        subs = result.stdout.strip()
        if subs:
            with open(file_name, "a") as f:
                f.write(subs + "\n")
            print(f"[+] Amass Done!")
        else:
            print("[-] Amass: No results")
    except FileNotFoundError:
        print("[-] Amass is not installed!")
        print("    Install it: go install -v github.com/owasp-amass/amass/v4/...@master")
    except subprocess.TimeoutExpired:
        print("[-] Amass timed out!")
    except Exception as e:
        print(f"[-] Amass error: {e}")


def findomain_scan(domain, file_name):
    print(f"\n[*] Running Findomain for {domain}...")
    try:
        result = subprocess.run(
            ['findomain', '-t', domain, '-q'],
            capture_output=True,
            text=True,
            timeout=120
        )
        subs = result.stdout.strip()
        if subs:
            with open(file_name, "a") as f:
                f.write(subs + "\n")
            print(f"[+] Findomain Done!")
        else:
            print("[-] Findomain: No results")
    except FileNotFoundError:
        print("[-] Findomain is not installed!")
        print("    Install it: https://github.com/Findomain/Findomain/releases")
    except subprocess.TimeoutExpired:
        print("[-] Findomain timed out!")
    except Exception as e:
        print(f"[-] Findomain error: {e}")


def gau_scan(domain, file_name):
    print(f"\n[*] Running gau for {domain}...")
    try:
        result = subprocess.run(
            ['gau', '--subs', domain, '--threads', str(MAX_THREADS), '--timeout', '15'],
            capture_output=True,
            text=True,
            timeout=300
        )
        urls = result.stdout.strip().split('\n')
        subdomains = set()
        for url in urls:
            try:
                parsed = urlparse(url)
                host = parsed.netloc.lower()
                if host and host.endswith(domain):
                    subdomains.add(host)
            except:
                pass
        if subdomains:
            with open(file_name, "a") as f:
                for sub in subdomains:
                    f.write(sub + "\n")
            print(f"[+] gau found: {len(subdomains)} subdomains")
        else:
            print("[-] gau: No results found")
    except FileNotFoundError:
        print("[-] gau is not installed!")
        print("    Install: go install github.com/lc/gau/v2/cmd/gau@latest")
    except subprocess.TimeoutExpired:
        print("[-] gau timed out!")
    except Exception as e:
        print(f"[-] gau error: {e}")


def fuzzing(domain, file_name):
    print(f"\n[*] Fuzzing Subdomains with ffuf & shuffledns tools...")

    # ffuf scan
    print(f"\n[*] Running ffuf for {domain}...")
    result = subprocess.run(
        [
            "ffuf",
            "-u", f"https://FUZZ.{domain}",
            "-w", subdoms_fuzzing,
            "-mc", "200,301,302,403",
            "-rate", str(RATE_LIMIT),
            "-t", str(MAX_THREADS),
            "-timeout", "10",
            "-v"
        ],
        capture_output=True,
        text=True
    )
    subs = result.stdout.strip()
    if subs:
        with open(file_name, "a") as f:
            f.write(subs + "\n")
        print("[+] ffuf Done!")
    else:
        print("[-] ffuf: No results found")

    # shuffledns scan
    print(f"\n[*] Running shuffledns for {domain}...")
    try:
        result = subprocess.run(
            [
                "shuffledns",
                "-d", domain,
                "-w", subdoms_fuzzing,
                "-r", resolvers_fuzzing,
                "-rate", str(RATE_LIMIT),
                "-t", str(MAX_THREADS),
                "-timeout", str(GLOBAL_TIMEOUT),
                "-silent"
            ],
            capture_output=True,
            text=True,
            timeout=GLOBAL_TIMEOUT
        )
        subs = result.stdout.strip()
        if subs:
            with open(file_name, "a") as f:
                f.write(subs + "\n")
            print("[+] shuffledns Done!")
        else:
            print("[-] shuffledns: No results found")
    except FileNotFoundError:
        print("[-] shuffledns is not installed!")
        print("    Install it: go install -v github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest")
    except subprocess.TimeoutExpired:
        print("[-] shuffledns timed out!")
    except Exception as e:
        print(f"[-] shuffledns error: {e}")


def filter_results(file_name):
    if os.path.exists(file_name):
        print("\n[*] Filtering duplicates...")
        with open(file_name, "r") as f:
            lines = f.readlines()
        unique_lines = sorted(set(line.strip() for line in lines if line.strip()))
        with open(file_name, "w") as f:
            for line in unique_lines:
                f.write(line + "\n")
        print(f"[+] Done! Total unique subdomains: {len(unique_lines)}")
        print(f"[+] Subdomains saved at ==> {file_name}")
    else:
        print("[-] No output file found. No subdomains were collected.")


def dnsx_resolve(input_file, output_file):
    print(f"\n[*] Running dnsx to resolve subdomains...")
    try:
        result = subprocess.run(
            ['dnsx', '-l', input_file, '-silent', '-a', '-resp-only', '-t', str(MAX_THREADS)],
            capture_output=True,
            text=True,
            timeout=600
        )
        resolved = result.stdout.strip()
        if resolved:
            with open(output_file, "w") as f:
                f.write(resolved)
            count = len(resolved.split('\n'))
            print(f"[+] dnsx Done! Resolved: {count} subdomains")
            print(f"[+] Saved at ==> {output_file}")
        else:
            print("[-] dnsx: No resolved subdomains found")
    except FileNotFoundError:
        print("[-] dnsx is not installed!")
        print("    Install: go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest")
    except subprocess.TimeoutExpired:
        print("[-] dnsx timed out!")
    except Exception as e:
        print(f"[-] dnsx error: {e}")


def httpx_probe(input_file, output_file):
    print(f"\n[*] Running httpx to find live web servers...")
    try:
        result = subprocess.run(
            [
                'httpx',
                '-l', input_file,
                '-silent',
                '-status-code',
                '-title',
                '-tech-detect',
                '-follow-redirects',
                '-threads', str(MAX_THREADS),
                '-rate-limit', str(RATE_LIMIT * 2),
                '-timeout', '10'
            ],
            capture_output=True,
            text=True,
            timeout=600
        )
        live_hosts = result.stdout.strip()
        if live_hosts:
            with open(output_file, "w") as f:
                f.write(live_hosts)
            count = len(live_hosts.split('\n'))
            print(f"[+] httpx Done! Live hosts: {count}")
            print(f"[+] Saved at ==> {output_file}")
        else:
            print("[-] httpx: No live hosts found")
    except FileNotFoundError:
        print("[-] httpx is not installed!")
        print("    Install: go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest")
    except subprocess.TimeoutExpired:
        print("[-] httpx timed out!")
    except Exception as e:
        print(f"[-] httpx error: {e}")


def naabu_scan(input_file, output_file):
    print(f"\n[*] Running naabu port scan...")
    try:
        result = subprocess.run(
            [
                'naabu',
                '-list', input_file,
                '-top-ports', '500',
                '-rate', str(RATE_LIMIT),
                '-threads', str(MAX_THREADS),
                '-timeout', '5',
                '-silent'
            ],
            capture_output=True,
            text=True,
            timeout=600
        )
        output = result.stdout.strip()
        if output:
            with open(output_file, "w") as f:
                f.write(output)
            count = len(output.split('\n'))
            print(f"[+] naabu Done! Open ports found: {count}")
            print(f"[+] Saved at ==> {output_file}")
        else:
            print("[-] naabu: No open ports found")
    except FileNotFoundError:
        print("[-] naabu is not installed!")
        print("    Install: go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest")
    except subprocess.TimeoutExpired:
        print("[-] naabu timed out!")
    except Exception as e:
        print(f"[-] naabu error: {e}")


def vhost_enum(domain, input_file, output_file):
    print(f"\n[*] Running Virtual Host Enumeration...")
    try:
        result = subprocess.run(
            [
                "ffuf",
                "-u", f"http://{domain_ip}",
                "-H", f"Host: FUZZ.{domain}",
                "-w", subdoms_fuzzing,
                "-mc", "200,301,302,403",
                "-fs", "0",
                "-rate", str(RATE_LIMIT),
                "-t", str(MAX_THREADS),
                "-timeout", "10",
                "-v"
            ],
            capture_output=True,
            text=True,
            timeout=600
        )
        output = result.stdout.strip()
        if output:
            with open(output_file, "w") as f:
                f.write(output)
            print(f"[+] VHost Enumeration Done!")
            print(f"[+] Saved at ==> {output_file}")
        else:
            print("[-] VHost: No results found")
    except FileNotFoundError:
        print("[-] ffuf is not installed!")
        print("    Install: go install github.com/ffuf/ffuf/v2@latest")
    except subprocess.TimeoutExpired:
        print("[-] VHost enumeration timed out!")
    except Exception as e:
        print(f"[-] VHost error: {e}")


def katana_scan(input_file, output_file):
    print(f"\n[*] Running katana crawler...")
    try:
        result = subprocess.run(
            [
                'katana',
                '-list', input_file,
                '-silent',
                '-jc',
                '-kf', 'all',
                '-d', '3',
                '-aff',
                '-timeout', '15'
            ],
            capture_output=True,
            text=True,
            timeout=600
        )
        output = result.stdout.strip()
        if output:
            with open(output_file, "w") as f:
                f.write(output)
            count = len(output.split('\n'))
            print(f"[+] katana Done! URLs found: {count}")
            print(f"[+] Saved at ==> {output_file}")
        else:
            print("[-] katana: No URLs found")
    except FileNotFoundError:
        print("[-] katana is not installed!")
        print("    Install: go install github.com/projectdiscovery/katana/cmd/katana@latest")
    except subprocess.TimeoutExpired:
        print("[-] katana timed out!")
    except Exception as e:
        print(f"[-] katana error: {e}")


def getJS_scan(input_file, output_file):
    print(f"\n[*] Extracting JavaScript files...")
    try:
        result = subprocess.run(
            ['getJS', '--input', input_file, '--complete'],
            capture_output=True,
            text=True,
            timeout=300
        )
        output = result.stdout.strip()
        if output:
            with open(output_file, "w") as f:
                f.write(output)
            count = len(output.split('\n'))
            print(f"[+] getJS Done! JS files found: {count}")
            print(f"[+] Saved at ==> {output_file}")
        else:
            print("[-] getJS: No JS files found")
    except FileNotFoundError:
        print("[-] getJS is not installed!")
        print("    Install: go install github.com/003random/getJS@latest")
    except subprocess.TimeoutExpired:
        print("[-] getJS timed out!")
    except Exception as e:
        print(f"[-] getJS error: {e}")


def gowitness_screenshot(input_file, output_dir):
    print(f"\n[*] Taking screenshots with gowitness...")
    os.makedirs(output_dir, exist_ok=True)
    try:
        subprocess.run(
            [
                'gowitness', 'file',
                '-f', input_file,
                '-P', output_dir,
                '--no-http',
                '-c', str(MAX_THREADS)
            ],
            capture_output=True,
            text=True,
            timeout=600
        )
        print(f"[+] gowitness Done!")
        print(f"[+] Screenshots saved at ==> {output_dir}/")
    except FileNotFoundError:
        print("[-] gowitness is not installed!")
        print("    Install: go install github.com/sensepost/gowitness@latest")
    except subprocess.TimeoutExpired:
        print("[-] gowitness timed out!")
    except Exception as e:
        print(f"[-] gowitness error: {e}")


def nuclei_scan(input_file, output_file):
    print(f"\n[*] Running nuclei vulnerability scan...")
    try:
        result = subprocess.run(
            [
                'nuclei',
                '-l', input_file,
                '-severity', 'medium,high,critical',
                '-c', str(MAX_THREADS),
                '-rl', str(RATE_LIMIT),
                '-timeout', '10',
                '-silent'
            ],
            capture_output=True,
            text=True,
            timeout=1800
        )
        output = result.stdout.strip()
        if output:
            with open(output_file, "w") as f:
                f.write(output)
            count = len(output.split('\n'))
            print(f"[+] nuclei Done! Vulnerabilities found: {count}")
            print(f"[+] Saved at ==> {output_file}")
        else:
            print("[-] nuclei: No vulnerabilities found")
    except FileNotFoundError:
        print("[-] nuclei is not installed!")
        print("    Install: go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest")
    except subprocess.TimeoutExpired:
        print("[-] nuclei timed out!")
    except Exception as e:
        print(f"[-] nuclei error: {e}")


# =============================================
# 🚀 Execution Phases
# =============================================

print("\n" + "="*50)
print("🚀 STARTING RECONNAISSANCE PHASES")
print("="*50)

# Phase 1: Passive Subdomain Enumeration
subDomainFinderWebsite(domain, file_name)
subFinderTool(domain, file_name)
shrewdeyeWebsite(domain, file_name)
assetfinder(domain, file_name)
amass_scan(domain, file_name)
findomain_scan(domain, file_name)
gau_scan(domain, file_name)

# Phase 2: Active DNS Enumeration / Bruteforce
fuzzing(domain, file_name)

# Phase 3: Cleanup
filter_results(file_name)

# Phase 4: DNS Resolution
dnsx_resolve(file_name, resolved_file)

# Phase 5: HTTP Probing
httpx_probe(resolved_file, live_file)

# Phase 6: TLS Enrichment
tlsx_scan(domain, live_file)

# Phase 7: Port Scanning
naabu_scan(resolved_file, ports_file)

# Phase 8: Virtual Host Enumeration
vhost_enum(domain, live_file, vhost_file)

# Phase 9: Crawling / URL & JS Discovery
katana_scan(live_file, crawl_file)
getJS_scan(live_file, js_file)

# Phase 10: Screenshots
gowitness_screenshot(live_file, screenshots_dir)

# Phase 11: Vulnerability Scanning
nuclei_scan(live_file, vuln_file)

print("\n✅ Reconnaissance Complete! Check output files for results.")

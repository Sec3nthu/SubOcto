import requests
from bs4 import BeautifulSoup
import subprocess
import os
import sys
import argparse  # ← Added for argument parsing

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
    description="Automated Subdomain Enumeration & Reconnaissance Toolkit",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
Examples:
  python %(prog)s -u example.com -sl subs.txt -rl resolvers.txt -ip 93.184.216.34
  python %(prog)s --domain example.com --subdomain-list wordlist.txt --resolvers-list dns.txt --target-ip 1.2.3.4

Use -h or --help for this help message.
    """
)

parser.add_argument('-u', '--domain', required=True, help='Target domain (e.g., example.com)')
parser.add_argument('-sl', '--subdomain-list', required=True, dest='subdomain_list',
                    help='Path to subdomain wordlist for fuzzing')
parser.add_argument('-rl', '--resolvers-list', required=True, dest='resolvers_list',
                    help='Path to DNS resolvers list')
parser.add_argument('-ip', '--target-ip', required=True, dest='target_ip',
                    help='IP address of the target website (for vhost enumeration)')

args = parser.parse_args()

# ===== Assign parsed values to your existing variable names =====
domain = args.domain
domain_ip = args.target_ip
subdoms_fuzzing = args.subdomain_list
resolvers_fuzzing = args.resolvers_list

file_name = f"{domain}_subs.txt"
resolved_file = f"{domain}_resolved.txt"
live_file = f"{domain}_live.txt"
ports_file = f"{domain}_ports.txt"
vhost_file = f"{domain}_vhosts.txt"
js_file = f"{domain}_jsfiles.txt"
crawl_file = f"{domain}_crawl.txt"
screenshots_dir = f"{domain}_screenshots"
vuln_file = f"{domain}_vulnerabilities.txt"


def subDomainFinderWebsite(domain, file_name):
    print("\n[*] First you should know the history for: Subdomainfinder.c99.nl")
    day = input("Add day > ")
    month = input("Add month > ")
    year = input("Add year > ")

    print(f"\n[*] Running Subdomainfinder.c99.nl for: {domain}")
    url = f"https://subdomainfinder.c99.nl/scans/{year}-{month}-{day}/{domain}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    print("[*] Connecting to subdomainfinder.c99.nl ......")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
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
            print(f"[-] Failed to connect. Status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("[-] Subdomainfinder.c99.nl: Connection error!")
    except requests.exceptions.Timeout:
        print("[-] Subdomainfinder.c99.nl: Request timed out!")
    except Exception as e:
        print(f"[-] Subdomainfinder.c99.nl error: {e}")


def subFinderTool(domain, file_name):
    print(f"\n[*] Running Subfinder for {domain}...")
    try:
        result = subprocess.run(
            ['subfinder', '-d', domain, '-silent', '-all', '-recursive'],
            capture_output=True,
            text=True,
            timeout=300
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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        r = requests.get(file_url, headers=headers, timeout=10)
        if r.status_code == 200:
            r2 = requests.get(txt_url, headers=headers, timeout=10)
            if r2.status_code == 200 and r2.text.strip():
                with open(file_name, "a", encoding="utf-8") as f:
                    f.write(r2.text + "\n")
                print(f"[+] Shrewdeye Done!")
            else:
                print("[-] Shrewdeye: No results found")
        else:
            print(f"[-] Shrewdeye: Failed to connect. Status code: {r.status_code}")
    except requests.exceptions.ConnectionError:
        print("[-] Shrewdeye: Connection error!")
    except requests.exceptions.Timeout:
        print("[-] Shrewdeye: Request timed out!")
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
            ['tlsx', '-u', domain, '-san', '-cn', '-silent', '-resp-only'],
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout.strip()

        if output:
            subdomains = set()

            for line in output.split("\n"):
                line = line.strip().lower()
                line = line.replace("*.", "")

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
            ['amass', 'enum', '-passive', '-d', domain],
            capture_output=True,
            text=True,
            timeout=300
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
            ['gau', '--subs', domain],
            capture_output=True,
            text=True,
            timeout=300
        )

        urls = result.stdout.strip().split('\n')
        subdomains = set()

        for url in urls:
            try:
                from urllib.parse import urlparse
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
            "-rate", "10",
            "-t", "5",
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
                "-silent"
            ],
            capture_output=True,
            text=True,
            timeout=300
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
            [
                'dnsx',
                '-l', input_file,
                '-silent',
                '-a',
                '-resp-only'
            ],
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
                '-follow-redirects'
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
                '-top-ports', '1000',
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
                "-rate", "100",
                "-t", "20",
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
                '-aff'
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

    try:
        subprocess.run(
            [
                'gowitness', 'file',
                '-f', input_file,
                '-P', output_dir,
                '--no-http'
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
                '-severity', 'low,medium,high,critical',
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
# Phase 1: Passive Subdomain Enumeration
# =============================================

subDomainFinderWebsite(domain, file_name)
subFinderTool(domain, file_name)
shrewdeyeWebsite(domain, file_name)
assetfinder(domain, file_name)
amass_scan(domain, file_name)
findomain_scan(domain, file_name)
gau_scan(domain, file_name)

# =============================================
# Phase 2: Active DNS Enumeration / Bruteforce
# =============================================
fuzzing(domain, file_name)

# =============================================
# Phase 3: Cleanup
# =============================================
filter_results(file_name)

# =============================================
# Phase 4: DNS Resolution
# =============================================
dnsx_resolve(file_name, resolved_file)

# =============================================
# Phase 5: HTTP Probing
# =============================================
httpx_probe(resolved_file, live_file)

# =============================================
# Phase 6: TLS Enrichment
# =============================================
tlsx_scan(domain, live_file)

# =============================================
# Phase 7: Port Scanning
# =============================================
naabu_scan(resolved_file, ports_file)

# =============================================
# Phase 8: Virtual Host Enumeration
# =============================================
vhost_enum(domain, live_file, vhost_file)

# =============================================
# Phase 9: Crawling / URL & JS Discovery
# =============================================
katana_scan(live_file, crawl_file)
getJS_scan(live_file, js_file)

# =============================================
# Phase 10: Screenshots
# =============================================
gowitness_screenshot(live_file, screenshots_dir)

# =============================================
# Phase 11: Vulnerability Scanning
# =============================================
nuclei_scan(live_file, vuln_file)

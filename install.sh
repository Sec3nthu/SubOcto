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

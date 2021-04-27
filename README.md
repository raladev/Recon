## dns_recon.sh - DNS enumeration using amass/bruteforce/alterations
'bash dns_recon.sh -f <domains.txt> -p <project_name> -m full'
'bash dns_recon.sh -d <domain.com> -p <project_name> -m full'

Notes:
- Need to provide correct pathes to tools and project folder - edit dns_recon.sh 
- Also, would be good to provide api-keys for some services to amass in config.ini (check amass documentation and amass run line in dns_recon.sh)

## get_asn.sh - ASN identification 
'bash get_asn.sh -f $<domains.txt> > <output_asn.txt>'

## get_cors.py - CORS retrieving
'python3.7 get_cors.py --file <domains.txt> --output <output_folder>'

## webscreenshot.py - screenshot taking
'python3.7 <path_to_websceenshot_folder>/webscreenshot.py -i <domains.txt> -o <output_folder>'

## flan - nmap scan with pretty reports
'docker run -v $(CURDIR)/shared:/shared -e format=html flan_scan -sC -Pn -p- -min-rate=400 --min-parallelism=512'
$(CURDIR)/shared - this dir is dir on host machine and should contain ips.txt file, also it will contain report after the scan

## gobuster - dir/vhost bruteforce
gobuster dir -u <host> -c <cookies> -t 50 -w <dictionary> -x .php,.html


## requiered tools
- python3 - to run several python scripts for brute-list building/reporting (sub_scripts folder, get_cors.py)  
- amass - to collect subdomains from third party services (dns_recon.sh)
- massdns - to resolve dns records (dns_recon.sh)
- pip3, dnsgen - to create alterations using valid dns records (dns_recon.sh) 
- phantomjs, webscreenshot - to screen domains
- docker, flan - port scanning and reporting
- go, gobuster - bruteforce dirs and vhost

## Installation flow (Ubuntu 20.04 x64 / 4GB RAM,80GB SSD / git, python3, docker are preinstalled):
sud apt-get update
apt install python3-pip
apt install unzip
sudo apt install p7zip


git clone https://github.com/raladev/Recon.git
mkdir Projects Tools && cd Tools

pip3 install dnsgen

mkdir amass && cd amass && wget https://github.com/OWASP/Amass/releases/download/v3.12.2/amass_linux_amd64.zip && unzip amass_linux_amd64.zip && rm amass_linux_amd64.zip
cd amass_linux_amd64 && nano config.ini (You should provide api key for services - https://github.com/OWASP/Amass/blob/master/examples/config.ini)

cd ~/Tools && git clone https://github.com/blechschmidt/massdns.git && make

(phantomJS instrution - https://gist.github.com/telbiyski/ec56a92d7114b8631c906c18064ce620)
cd ~/Tools && git clone https://github.com/maaaaz/webscreenshot.git

cd ~/Tools && git clone https://github.com/cloudflare/flan.git && cd flan && make

cd ~/Tools && mkdir gobuster && cd gobuster && wget https://github.com/OJ/gobuster/releases/download/v3.1.0/gobuster-linux-amd64.7z && unzip gobuster-linux-amd64.7z && cd gobuster-linux-amd64 && chmod +x gobuster


cd ~/Recon && nano dns_recon.sh && (edit path variables for tools)
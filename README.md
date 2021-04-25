##dns_recon.sh - DNS enumeration using amass/bruteforce/alterations
'bash dns_recon.sh -f <domains.txt> -p <project_name> -m full'
'bash dns_recon.sh -d <domain.com> -p <project_name> -m full'

Notes:
- Need to provide correct pathes to tools and project folder - edit dns_recon.sh 
- Also, would be good to provide api-keys for some services to amass in config.ini (check amass documentation and amass run line in dns_recon.sh)

##get_asn.sh - ASN identification 
'bash get_asn.sh -f $<domains.txt> > <output_asn.txt>'

##get_cors.py - CORS retrieving
'python3.7 get_cors.py --file <domains.txt> --output <output_folder>'

##webscreenshot.py - screenshot taking
'python3.7 <path_to_websceenshot_folder>/webscreenshot.py -i <domains.txt> -o <output_folder>'

##flan - nmap scan with pretty reports
'docker run -v $(CURDIR)/shared:/shared flan_scan -sC -Pn -p- -min-rate=400 --min-parallelism=512'
$(CURDIR)/shared - this dir is dir on host machine and should contain ips.txt file, also it will contain report after the scan

##gobuster - dir/vhost bruteforce
TODO

##requiered tools
- python3.7 - to run several python scripts for brute-list building/reporting (sub_scripts folder, get_cors.py)  
- amass - to collect subdomains from third party services (dns_recon.sh)
- massdns - to resolve dns records (dns_recon.sh)
- dnsgen - to create alterations using valid dns records (dns_recon.sh)  
- phantomjs, webscreenshot - to screen domains
- docker, flan - port scanning and reporting
- go, gobuster - bruteforce dirs and vhost

##Installation flow (clean Ubuntu 20)
TODO
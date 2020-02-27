from __future__ import print_function

from requests import get, exceptions
import click
from socket import gethostbyname, gaierror
from sys import version_info, exit

import logging
import tldextract
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

__author__ = "Bharath(github.com/yamakira)"
__version__ = "0.0.1"
__purpose__ = '''Parse and print domain names from Content Security Policy(CSP) header'''


class Domain:
    def __init__(self, domain=None, apex_domain=None, available=None, ip=None, raw_csp_url=None):
        self.domain = domain
        self.apex_domain = apex_domain
        self.available = available
        self.ip = ip
        self.raw_csp_url = raw_csp_url


def clean_domains(domains):
    for domain in domains:
        ext = tldextract.extract(str(domain.raw_csp_url))
        # If subdomain is wildcard or empty
        if ext[0] in ['*', '']:
            # Join all but the subdomain (a wildcard or empty)
            domain.domain = '.'.join(ext[1:])
        else:
            domain.domain = '.'.join(ext)
        domain.apex_domain = ".".join(tldextract.extract(domain.domain)[1:])
    return domains


def get_csp_header(url):
    try:
        logger.info("[+] Fetching headers for {}".format(url))
        r = get("https://" + url)
    except exceptions.RequestException as e:
        print(e)
        exit(1)

    if 'Content-Security-Policy' in r.headers:
        csp_header = r.headers['Content-Security-Policy']
        return csp_header
    elif 'content-security-policy-report-only' in r.headers:
        csp_header = r.headers['content-security-policy-report-only:']
        return csp_header
    else:
        logger.info("[+] {} doesn't support CSP header".format(url))
        return None

def get_domains(csp_header):
    domains = []
    csp_header_values = csp_header.split(" ")
    for line in csp_header_values:
        if "." in line:
            line = line.replace(";", "")
            domains.append(Domain(raw_csp_url=line))
        else:
            pass
    return clean_domains(domains)


def get_csp_from_one_domain(url, output):
    csp_header = get_csp_header(url)
    # Retrieve list of domains "clean" or not
    if csp_header:
        domains = get_domains(csp_header)
        if output:
            with open(output + "/" + url + ".txt", 'w+') as outfile:
                json.dump(dict(domains=[ob.__dict__ for ob in domains]), outfile, sort_keys=True, indent=4)

@click.command()
@click.option('--url', '-u',
              help='Url to retrieve the CSP header from')
@click.option('--file', '-u',
              help='File with Urls')
@click.option('--output', '-o', default=False,
              help='output dir (w/o /)')
def main(url, file, output):
    
    if file:
        file_from_domains = open(file).read().splitlines()
        for i in file_from_domains:
            get_csp_from_one_domain(i, output)
    elif url:
        get_csp_from_one_domain(url, output)
    else:
        print("url or file must be specified")

if __name__ == '__main__':
    main()
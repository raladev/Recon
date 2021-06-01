import sys
import re

if __name__ == "__main__":

    project_dir = sys.argv[1]
    resolved_passive = sys.argv[2]
    resolved_brute = sys.argv[3]
    resolved_alt = sys.argv[4]
    print(project_dir)
    print(resolved_passive)
    print(resolved_brute)
    print(resolved_alt)

    passive_list = open(resolved_passive).read().splitlines()
    brute_list = open(resolved_brute).read().splitlines()
    alt_list = open(resolved_alt).read().splitlines()
 
    passive_domain_list = [re.match("([a-z0-9-\._]*)\. ", i).group(1) for i in passive_list]
    brute_domain_list = [re.match("([a-z0-9-\._]*)\. ", i).group(1) for i in brute_list]
    alt_domain_list = [re.match("([a-z0-9-\._]*)\. ", i).group(1) for i in alt_list]

    #File with domains only
    set_of_domain_lists = set(passive_domain_list + brute_domain_list + alt_domain_list)
    with open(project_dir+'/fin_only_domains.txt', 'w+') as f:
        for word in sorted(set_of_domain_lists, key=lambda i:len(i)):
            f.write(f'{word}\n')

    #File with full A records (for CNAME detection)
    set_of_lists = set(passive_list + brute_list + alt_list)
    with open(project_dir+'/fin_a_dns_records.txt', 'w+') as f:
        for word in sorted(set_of_lists, key=lambda i:len(i)):
            f.write(f'{word}\n')

    #File with statistic of enum
    with open(project_dir + '/fin_statistic.txt', 'w+') as f:

        unique_passive_domains = set(passive_domain_list)
        f.write(f'PASSIVE SCAN - {len(unique_passive_domains)} unique domains\n')
        for word in sorted(unique_passive_domains, key=lambda i:len(i)):
            f.write(f'{word}\n')
        f.write(f'\n')

        unique_brute_domains = set(brute_domain_list).difference(unique_passive_domains)
        f.write(f'BRUTEFORCE - {len(unique_brute_domains)} unique domains\n')
        for word in sorted(unique_brute_domains, key=lambda i:len(i)):
            f.write(f'{word}\n')
        f.write(f'\n')

        unique_alt_domains = set(alt_domain_list).difference(unique_passive_domains, unique_brute_domains)
        f.write(f'ALTERATIONS BRUTE - {len(unique_alt_domains)} unique domains\n')
        for word in sorted(unique_alt_domains, key=lambda i: len(i)):
            f.write(f'{word}\n')
        f.write(f'\n')
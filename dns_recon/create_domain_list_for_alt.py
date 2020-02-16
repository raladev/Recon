import sys
import re

if __name__ == "__main__":

    project_dir = sys.argv[1]
    amass_out = sys.argv[2]
    brute_out = sys.argv[3]

    amass_domain_list = [re.match("([a-z1-9-\.]*)\. ", i).group(1) for i in open(amass_out).read().splitlines()]
    brute_domain_list = [re.match("([a-z1-9-\.]*)\. ", i).group(1) for i in open(brute_out).read().splitlines()]

    set_of_lists = set(amass_domain_list + brute_domain_list)

    with open(project_dir+'/domains_for_alt.txt', 'w+') as f:
        for word in set_of_lists:

            f.write(f'{word}\n')



import sys
import re

if __name__ == "__main__":

    project_dir = sys.argv[1]
    passive_out = sys.argv[2]
    resolved_out = sys.argv[3]

    passive_list = [i for i in open(passive_out).read().splitlines()]
    resolved_list = [re.match("([a-z0-9-\._]*)\. ", i).group(1) for i in open(resolved_out).read().splitlines()]

    set_of_lists = set(passive_list) ^ set(resolved_list)

    with open(project_dir+'/unresolved_passive.txt', 'w+') as f:
        for word in set_of_lists:

            f.write(f'{word}\n')



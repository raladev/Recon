import sys

if __name__ == "__main__":

    path_to_dict = sys.argv[1]
    project_dir = sys.argv[2]
    domain = sys.argv[3]

    wordlist = open(path_to_dict).read().splitlines()

    with open(project_dir+'/brute_list.txt', 'w+') as f:
        for word in wordlist:
            if not word.strip():
                continue
            f.write(f'{word}.{domain}\n')



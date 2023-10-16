import sys
import ast


def main(pac_dict):
    new_dict = {}
    max_len = 0
    for key, value in pac_dict.items():
        tmp_dict = {}
        for pac_dict in value.get('packages', {}):
            name = ''
            version = ''
            for k, v in pac_dict.items():
                if k == 'name':
                    name = v
                    max_len = max(max_len, len(v))
                if k == 'version':
                    version = v
            tmp_dict.setdefault(name, version)
        new_dict.setdefault(key, tmp_dict)

    print("{:<{}} {}".format("Package", max_len, "Version"))
    print("-" * (2 * max_len))
    for ip, package in new_dict.items():
        print("[%s]" % ip)
        for name, version in package.items():
            print("{:<{}}  {}".format(name, max_len, version))


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        json_pac = f.read()
        dict_pac = ast.literal_eval(json_pac)
        main(dict_pac)

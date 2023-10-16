import glob
import json
import os
import sys


def main(jsons_path, output_path):
    os.chdir(jsons_path)
    json_files = glob.glob("*.json")
    merged_data = {}
    for file in json_files:
        with open(file, 'r') as f:
            data = json.load(f)
            for key, value in data.items():
                if key in merged_data:
                    merged_data.get(key, {}).update(value)
                else:
                    merged_data.setdefault(key, value)

    flags = os.O_WRONLY | os.O_CREAT
    with os.fdopen(os.open(output_path + '/report.json', flags, 0o644), 'w', newline='') as f:
        json.dump(merged_data, f)


if __name__ == '__main__':
    from_path = sys.argv[1]
    to_path = sys.argv[2]
    main(from_path, to_path)

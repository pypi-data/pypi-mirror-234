import json
import os
from p.constant import ROOTDIR


def read_data(json_file):
    with open(json_file, "r", encoding="utf8") as f:
        return json.load(f)


def main():
    current_titme = "10/10/2023 下午 10:52:24"
    print(f"current time: {current_titme}")
    data_path = os.path.join(ROOTDIR, "data", "data.json")
    data = read_data(data_path)
    print(f"read data: {data}")


if __name__ == "__main__":
    main()

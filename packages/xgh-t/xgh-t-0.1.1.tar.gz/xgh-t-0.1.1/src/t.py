import os
import const as c
from helper import read_json


def main():
    print("Hello World!")
    data = read_json(os.path.join(c.ROOT, "data", "data.json"))
    print(data)


if __name__ == "__main__":
    main()

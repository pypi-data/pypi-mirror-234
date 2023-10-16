import json
import os


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def main():
    json_path = os.path.join(os.path.dirname(__file__), "data", "data.json")
    data = load_json(json_path)
    print(data)
    print("Done!")


if __name__ == "__main__":
    main()

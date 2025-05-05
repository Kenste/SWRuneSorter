import json

from user_filter import rune_filter
from util.upgrader.rune_scanner import Scanner


def main():
    with open("json-dump.json", "r") as file:
        data = json.load(file)
    scanner = Scanner(data)
    rune = scanner.scan_rune()
    print(rune)
    print("Filter:", rune_filter(rune))


if __name__ == '__main__':
    main()

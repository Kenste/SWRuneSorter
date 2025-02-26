import json
import traceback

from user_filter import rune_filter
from util.upgrader.navigator import Navigator
from util.upgrader.rune_scanner import Scanner


def read_rune(scanner: Scanner):
    try:
        return scanner.scan_rune()
    except KeyError as k:
        print(f"Error while reading the Rune. Could not correctly read {k}!")
    except AttributeError:
        # Ignore as there is most likely no rune shown
        pass
    except Exception:
        traceback.print_exc()
    return None


def main():
    with open("json-dump.json", "r") as file:
        data = json.load(file)
    scanner = Scanner(data)
    navigator = Navigator(data)

    rune = read_rune(scanner)
    print(rune)
    if not rune_filter(rune):
        print("Sell - Did not pass filter!")
    else:
        print("Upgrade / Keep!")

if __name__ == '__main__':
    main()

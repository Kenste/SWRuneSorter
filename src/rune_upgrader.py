import json
import sys
import time
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
    navigator = Navigator(data, base_delay=0)

    kept_runes = []

    for slot in navigator.slot_iterator():
        iterations = 0
        navigator.reset_rune_i()
        while iterations < len(data["runes_row"]):
            navigator.open_next_rune()
            rune = read_rune(scanner)
            if rune is None:
                navigator.increment_rune_i()
                iterations += 1
                continue

            # TODO: do rune stuff
            print("Found Rune")
            print(rune)
            iterations = 0

            if rune.level >= 1:
                print(f"Finished Slot {slot}\n")
                navigator.close_rune()
                break

            if not rune_filter(rune):
                print("Sell - Did not pass filter!")
                if rune.quality == "Legend":
                    navigator.sell_rune(level=12)
                else:
                    navigator.sell_rune()
            else:
                navigator.upgrade_rune(9)
                rune = read_rune(scanner)
                print(rune)
                if not rune_filter(rune):
                    print("Sell - Did not pass filter!")
                    if rune.quality == "Legend":
                        navigator.sell_rune(12)
                    else:
                        navigator.sell_rune()
                else:
                    navigator.upgrade_rune(12)
                    rune = read_rune(scanner)
                    print(rune)
                    if not rune_filter(rune):
                        print("Sell - Did not pass filter")
                        navigator.sell_rune(12)
                    else:
                        print("KEEP!")
                        kept_runes.append(rune)
            print("--------------------\n")
    print("\n"*5)
    print("Kept Runes:")
    for rune in kept_runes:
        print(rune)


if __name__ == '__main__':
    main()

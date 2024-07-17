import json
import traceback

from runescorer import scorer
from util import json_helper
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
    profiles = json_helper.weight_profiles_from_json("../resources/weights.json")
    for profile in profiles:
        scorer.add_profile(profile)

    with open("json-dump.json", "r") as file:
        data = json.load(file)
    scanner = Scanner(data)
    navigator = Navigator(data)

    kept_runes = []
    # TODO: configure
    score_threshold = 60

    for slot in navigator.slot_iterator():
        iterations = 0
        while iterations < len(data["runes_row"]):
            navigator.open_next_rune()
            rune = read_rune(scanner)
            if rune is None:
                navigator.increment_rune_i()
                iterations += 1
                continue

            # TODO: do rune stuff
            print("Found Rune")
            print(scorer.max_score(rune), rune)
            iterations = 0

            if rune.level >= 12:
                print(f"Finished Slot {slot}\n")
                navigator.close_rune()
                break

            if scorer.max_score(rune)[0] < score_threshold:
                print("Sell - Low Score!")
                if rune.quality == "Legend":
                    navigator.sell_rune(level=12)
                else:
                    navigator.sell_rune()
            else:
                navigator.upgrade_rune(9)
                rune = read_rune(scanner)
                print(scorer.max_score(rune), rune)
                if scorer.max_score(rune)[0] < score_threshold:
                    print("Sell - Low Score!")
                    if rune.quality == "Legend":
                        navigator.sell_rune(12)
                    else:
                        navigator.sell_rune()
                else:
                    navigator.upgrade_rune(12)
                    rune = read_rune(scanner)
                    print(scorer.max_score(rune), rune)
                    if scorer.max_score(rune)[0] < score_threshold:
                        print("Sell - Low Score!")
                        navigator.sell_rune(12)
                    else:
                        print("KEEP!")
                        kept_runes.append(rune)
            print("--------------------\n")
    print("\n"*5)
    print("Kept Runes:")
    for rune in kept_runes:
        print(scorer.max_score(rune), rune)


if __name__ == '__main__':
    main()

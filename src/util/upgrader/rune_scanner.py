import re

import cv2
import numpy as np
import pyscreenshot
import pytesseract

from runescorer.rune import Rune, RuneStat

stat_map = {
    "ATK": "ATK",
    "ATK%": "ATK%",
    "DEF": "DEF",
    "DEF%": "DEF%",
    "HP": "HP",
    "HP%": "HP%",
    "SPD": "SPD",
    "CRI Rate%": "CRate",
    "CRI Dmg%": "CDmg",
    "Resistance%": "RES",
    "Accuracy%": "ACC"
}


def find_flat_stat_value(text):
    match = re.search(r'\b(ATK|DEF|HP) \+(\d+)\b(?!%)', text)
    if match:
        return match.group(2)  # Return the number after the "+"
    return None

def extract_stat_and_value(input_string):
    # Define the regular expression to capture the required parts
    pattern = re.compile(r"([A-Za-z\s%]+)\s*(\+|\#)?(\d+\.?\d*)%?")

    match = pattern.match(input_string)
    if match:
        stat = match.group(1).strip()
        value = float(match.group(3))
        if '%' in input_string:
            stat += '%'
        stat = stat_map[stat]
        return stat, value
    else:
        return None



class Scanner:
    def __init__(self, data):
        self._bbox_name = data["rune_name"]
        self._bbox_substats = data["rune_subs"]
        self._bbox_innate = data["rune_innate"]
        self._bbox_main = data["rune_main"]
        self._bbox_quality = data["rune_quality"]

    def scan_rune(self) -> Rune:
        img = pyscreenshot.grab()
        img = np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_name = self._sub_image(img, self._bbox_name)
        img_quality = self._sub_image(img, self._bbox_quality)
        img_main = self._sub_image(img, self._bbox_main)
        img_innate = self._sub_image(img, self._bbox_innate)
        img_subs = self._sub_image(img, self._bbox_substats)
        # cv2.imshow("Name", img_name)
        # cv2.imshow("Quality", img_quality)
        # cv2.imshow("Main", img_main)
        # cv2.imshow("Innate", img_innate)
        # cv2.imshow("Subs", img_subs)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        name = pytesseract.image_to_string(img_name, config=r"--oem 3 --psm 7").strip()
        slot_pattern = re.compile(r".*\((\d)\)")
        slot_match = slot_pattern.match(name)
        slot = int(slot_match.group(1))

        level_pattern = re.compile(r"\+(\d+)")
        level_match = level_pattern.match(name)
        if level_match:
            level = int(level_match.group(1))
        else:
            level = 0

        quality = pytesseract.image_to_string(img_quality).strip()

        main = pytesseract.image_to_string(img_main, config=r"--oem 3 --psm 7").strip()
        main = extract_stat_and_value(main)

        innate = pytesseract.image_to_string(img_innate, config=r"--oem 3 --psm 7").strip()
        innate = extract_stat_and_value(innate)

        if innate is not None:
            innate = RuneStat(innate[0], innate[1])

        new_subs = []
        subs = pytesseract.image_to_string(img_subs, config=r"--oem 3 --psm 6").strip().split("\n")
        for sub in subs:
            if sub == "":
                continue
            new_subs.append(extract_stat_and_value(sub))
        return Rune(RuneStat(main[0], main[1]), innate, [RuneStat(sub[0], sub[1]) for sub in new_subs], level, slot,
                    quality, set="", stars=6)

    def _sub_image(self, img: np.array, bbox: [int]) -> np.array:
        x1, y1, x2, y2 = bbox
        return img[y1:y2, x1:x2]

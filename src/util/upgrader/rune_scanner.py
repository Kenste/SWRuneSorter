import os
import re
from datetime import datetime

import cv2
import numpy as np
import pyscreenshot
import pytesseract
from runescorer.rune import Rune, RuneStat


class RuneNotReadableException(Exception):
    def __init__(self, message, screenshot):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.folder = "rune_errors"
        os.makedirs(self.folder, exist_ok=True)

        # Save screenshot
        self.screenshot_path = os.path.join(self.folder, f"rune_error_{self.timestamp}.png")
        # screenshot is a PIL Image, save directly
        screenshot.save(self.screenshot_path)

        # Save error message
        self.log_path = os.path.join(self.folder, f"rune_error_{self.timestamp}.txt")
        with open(self.log_path, "w") as f:
            f.write(message)

        super().__init__(f"{message}\nScreenshot saved to: {self.screenshot_path}\nLog saved to: {self.log_path}")


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


def _sub_image(img: np.array, bbox: [int]) -> np.array:
    x1, y1, x2, y2 = bbox
    return img[y1:y2, x1:x2]


def _create_rune_from_strings(name_str, quality_str, main_str, innate_str, subs_str) -> Rune:
    # Parse slot from name string
    slot_pattern = re.compile(r".*\((\d)\)")
    slot_match = slot_pattern.match(name_str)
    slot = int(slot_match.group(1)) if slot_match else 0

    # Parse set from name string
    set_pattern = re.compile(r"(\w+)\s+Rune")
    set_match = re.search(set_pattern, name_str)
    set = set_match.group(1) if set_match else ""

    # Parse level from name string
    level_pattern = re.compile(r"\+(\d+)")
    level_match = level_pattern.search(name_str)
    level = int(level_match.group(1)) if level_match else 0

    # Parse main stat
    main = extract_stat_and_value(main_str)

    # Parse innate stat
    innate = extract_stat_and_value(innate_str)
    if innate is not None:
        innate = RuneStat(innate[0], innate[1])

    # Parse substats
    new_subs = []
    subs = subs_str.split("\n")
    for sub in subs:
        if sub == "":
            continue
        stat_val = extract_stat_and_value(sub)
        if stat_val is not None:
            new_subs.append(RuneStat(stat_val[0], stat_val[1]))

    return Rune(
        RuneStat(main[0], main[1]),
        innate,
        new_subs,
        level,
        slot,
        quality_str,
        set=set,
        stars=6
    )


class Scanner:
    def __init__(self, data):
        self._bbox_name = data["rune_name"]
        self._bbox_substats = data["rune_subs"]
        self._bbox_innate = data["rune_innate"]
        self._bbox_main = data["rune_main"]
        self._bbox_quality = data["rune_quality"]

    def scan_rune(self) -> Rune:
        screen = pyscreenshot.grab()
        img = np.array(screen)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        preprocessing_steps = [
            lambda image: cv2.threshold(image, 115, 255, cv2.THRESH_BINARY_INV)[1]
        ]
        for preprocessing_step in preprocessing_steps:
            img = preprocessing_step(img)

            img_name = _sub_image(img, self._bbox_name)
            img_quality = _sub_image(img, self._bbox_quality)
            img_main = _sub_image(img, self._bbox_main)
            img_innate = _sub_image(img, self._bbox_innate)
            img_subs = _sub_image(img, self._bbox_substats)

            name_str = pytesseract.image_to_string(img_name, config=r"--oem 3 --psm 7").strip()
            quality_str = pytesseract.image_to_string(img_quality, config=r"--oem 3 --psm 7").strip()
            main_str = pytesseract.image_to_string(img_main, config=r"--oem 3 --psm 7").strip()
            innate_str = pytesseract.image_to_string(img_innate, config=r"--oem 3 --psm 7").strip()
            subs_str = pytesseract.image_to_string(img_subs, config=r"--oem 3 --psm 6").strip()

            try:
                return _create_rune_from_strings(name_str, quality_str, main_str, innate_str, subs_str)
            except AttributeError:
                # Ignore as there is most likely no rune shown
                return None
            except Exception as e:
                print(e)
                raise RuneNotReadableException(e, screen)
        raise RuneNotReadableException("Could not read the Rune", screen)

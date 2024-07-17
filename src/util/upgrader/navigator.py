import time

import pyautogui


class Navigator:
    def __init__(self, data):
        self._rune_clicks = data["runes_row"]
        self._rune_slots = [
            data["rune_slot_1"],
            data["rune_slot_2"],
            data["rune_slot_3"],
            data["rune_slot_4"],
            data["rune_slot_5"],
            data["rune_slot_6"]
        ]
        self._power_up_button = data["power_up"]
        self._nine_button = data["+9"]
        self._twelve_button = data["+12"]
        self._upgrade_button = data["upgrade"]
        self._ok_button = data["ok"]
        self._close_button = data["close"]
        self._sell_button = data["sell"]
        self._yes_sell = data["sell_confirm"]
        self._yes_sell_6 = data["sell_confirm_6"]

        self._rune_i = 0

    def upgrade_rune(self, level: int) -> None:
        pyautogui.moveTo(self._power_up_button)
        pyautogui.click()
        time.sleep(0.2)
        if level == 9:
            pyautogui.moveTo(self._nine_button)
        else:
            pyautogui.moveTo(self._twelve_button)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(self._upgrade_button)
        pyautogui.click()
        time.sleep(3)
        pyautogui.moveTo(self._ok_button)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(self._close_button)
        pyautogui.click()
        time.sleep(0.2)

    def close_rune(self):
        pyautogui.press("esc")

    def sell_rune(self, level: int = 9) -> None:
        pyautogui.moveTo(self._sell_button)
        pyautogui.click()
        time.sleep(0.2)
        pyautogui.moveTo(self._yes_sell)
        pyautogui.click()
        if level > 9:
            time.sleep(0.5)
            pyautogui.moveTo(self._yes_sell_6)
            pyautogui.click()
        time.sleep(1)
        # move
        self._rune_i = (self._rune_i + 1) % len(self._rune_clicks)

    def open_next_rune(self) -> None:
        pyautogui.moveTo(self._rune_clicks[self._rune_i])
        pyautogui.click()

    def increment_rune_i(self) -> None:
        self._rune_i = (self._rune_i + 1) % len(self._rune_clicks)

    def slot_iterator(self):
        for i, rune_slot in enumerate(self._rune_slots):
            pyautogui.moveTo(rune_slot)
            pyautogui.click()
            pyautogui.moveTo(self._rune_clicks[0])
            pyautogui.scroll(-1000)
            yield i + 1
            pyautogui.moveTo(rune_slot)
            pyautogui.click()

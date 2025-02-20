import ast
import json
from enum import StrEnum

import pygubu
from tkinter import filedialog
from PIL import ImageGrab, ImageTk, Image


class CanvasState(StrEnum):
    ROI = "ROI"
    BUTTON = "BUTTON"
    SCREENSHOT = "SCREENSHOT"


class State(StrEnum):
    INITIAL_SCREEN = "Initial Screen"
    RUNES_ROW = "runes_row"
    RUNE_SLOT_1 = "rune_slot_1"
    RUNE_SLOT_2 = "rune_slot_2"
    RUNE_SLOT_3 = "rune_slot_3"
    RUNE_SLOT_4 = "rune_slot_4"
    RUNE_SLOT_5 = "rune_slot_5"
    RUNE_SLOT_6 = "rune_slot_6"
    RUNE_SCREEN = "Rune Screen"
    POWER_UP = "power_up"
    SELL = "sell"
    RUNE_NAME = "rune_name"
    RUNE_MAIN = "rune_main"
    RUNE_INNATE = "rune_innate"
    RUNE_SUBS = "rune_subs"
    RUNE_QUALITY = "rune_quality"
    POWER_UP_SCREEN = "Power-Up Screen"
    UPGRADE = "upgrade"
    UP_9 = "+9"
    UP_12 = "+12"
    CLOSE = "close"
    UP_RESULT_SCREEN = "Power-Up Result Screen"
    OK = "ok"
    SELL_CONFIRM_SCREEN = "Sell Confirm Screen"
    YES = "sell_confirm"
    SELL_CONFIRM_SCREEN2 = "Sell Confirm 6* Legend Screen"
    YES2 = "sell_confirm_6"


class ScreenMarker:
    def __init__(self):
        self.builder = pygubu.Builder()
        self.builder.add_from_file("../resources/screenmarker.ui")
        self.mainwindow = self.builder.get_object("mainframe")
        self.canvas = self.builder.get_object("canvas")
        self.label = self.builder.get_object("promptLabel")
        self._combobox = self.builder.get_object("combobox")

        self.canvas_screenshot = None
        self.screenshot = None
        self.marker = None
        self._set_canvas_state(CanvasState.SCREENSHOT)
        self._set_state(State.INITIAL_SCREEN)
        self.label.config(text=self.state)

        self._rune_rows = {}

        self.imgs = {}
        self.coordinates = None
        self.coords = {}

        self.builder.connect_callbacks(self)
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

    def run(self) -> None:
        self.mainwindow.mainloop()

    def screenshot_clicked(self) -> None:
        if self.canvas_state != CanvasState.SCREENSHOT:
            return

        if self.canvas_screenshot is not None:
            self.canvas.delete(self.canvas_screenshot)
        try:
            img = ImageGrab.grab()
        except:
            file_path = filedialog.askopenfilename(
                title="Cannot create a Screenshot, please select an image",
            )
            img = Image.open(file_path)
        self.screenshot = ImageTk.PhotoImage(img)
        self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
        self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())

    def previous_clicked(self) -> None:
        match self.state:
            case State.INITIAL_SCREEN:
                # Do nothing, as there is no prior state
                pass
            case State.RUNES_ROW:
                for marker in self._rune_rows.values():
                    self.canvas.delete(marker)
                self.marker = None
                self._rune_rows.clear()

                self._set_state(State.INITIAL_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)
            case State.RUNE_SLOT_1:
                if self.marker is not None:
                    self.canvas.delete(self.marker)
                    self.marker = None

                self._set_state(State.RUNES_ROW)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    for c in self.coords[self.state]:
                        self.coordinates = c
                        self.marker = self.draw_circle(*self.coordinates)
                        self._rune_rows[c] = self.marker
                    self._combobox.configure(values=[str(c) for c in self._rune_rows.keys()])
                    self._combobox.set(str(self.coordinates))
            case State.RUNE_SLOT_2:
                if self.marker is not None:
                    self.canvas.delete(self.marker)
                    self.marker = None

                self._set_state(State.RUNE_SLOT_1)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_3:
                if self.marker is not None:
                    self.canvas.delete(self.marker)
                    self.marker = None

                self._set_state(State.RUNE_SLOT_2)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_4:
                if self.marker is not None:
                    self.canvas.delete(self.marker)
                    self.marker = None

                self._set_state(State.RUNE_SLOT_3)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_5:
                if self.marker is not None:
                    self.canvas.delete(self.marker)
                    self.marker = None

                self._set_state(State.RUNE_SLOT_4)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_6:
                if self.marker is not None:
                    self.canvas.delete(self.marker)
                    self.marker = None

                self._set_state(State.RUNE_SLOT_5)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SCREEN:
                self._set_state(State.RUNE_SLOT_6)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.POWER_UP:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)
            case State.SELL:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.POWER_UP)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_NAME:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.SELL)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_MAIN:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_NAME)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_INNATE:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_MAIN)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_SUBS:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_INNATE)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_QUALITY:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_SUBS)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.POWER_UP_SCREEN:
                self._set_state(State.RUNE_QUALITY)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.UPGRADE:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.POWER_UP_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)
            case State.UP_9:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.UPGRADE)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UP_12:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.UP_9)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.CLOSE:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.UP_12)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UP_RESULT_SCREEN:
                self._set_state(State.CLOSE)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.OK:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.UP_RESULT_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)
            case State.SELL_CONFIRM_SCREEN:
                self._set_state(State.OK)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.YES:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.SELL_CONFIRM_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)
            case State.SELL_CONFIRM_SCREEN2:
                self._set_state(State.YES)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.YES2:
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.SELL_CONFIRM_SCREEN2)
                self._set_canvas_state(CanvasState.SCREENSHOT)
            case _:
                print("How?")
        self.label.config(text=self.state)

    def next_clicked(self) -> None:
        match self.state:
            case State.INITIAL_SCREEN:
                # save current state
                self.imgs[self.state] = self.screenshot

                # prepare next state
                self._set_state(State.RUNES_ROW)
                self._set_canvas_state(CanvasState.BUTTON)

                # load next state if already visited
                if self.state in self.coords:
                    for c in self.coords[self.state]:
                        self.coordinates = c
                        self.marker = self.draw_circle(*self.coordinates)
                        self._rune_rows[c] = self.marker
                    self._combobox.configure(values=[str(c) for c in self._rune_rows.keys()])
                    self._combobox.set(str(self.coordinates))
                else:
                    self.add_clicked()
            case State.RUNES_ROW:
                self.coords[self.state] = list(self._rune_rows.keys())
                for marker in self._rune_rows.values():
                    self.canvas.delete(marker)
                self.marker = None
                self._rune_rows.clear()

                self._set_state(State.RUNE_SLOT_1)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_1:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_SLOT_2)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_2:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_SLOT_3)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_3:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_SLOT_4)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_4:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_SLOT_5)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_5:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_SLOT_6)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_6:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None
                self.imgs[self.state] = self.screenshot
                self.canvas.delete(self.canvas_screenshot)
                self.canvas_screenshot = None

                self._set_state(State.RUNE_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.RUNE_SCREEN:
                self.imgs[self.state] = self.screenshot

                self._set_state(State.POWER_UP)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.POWER_UP:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.SELL)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.SELL:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_NAME)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_NAME:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_MAIN)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_MAIN:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_INNATE)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_INNATE:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_SUBS)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_SUBS:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.RUNE_QUALITY)
                self._set_canvas_state(CanvasState.ROI)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_QUALITY:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None
                self.imgs[self.state] = self.screenshot
                self.canvas.delete(self.canvas_screenshot)
                self.canvas_screenshot = None

                self._set_state(State.POWER_UP_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.POWER_UP_SCREEN:
                self.imgs[self.state] = self.screenshot

                self._set_state(State.UPGRADE)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UPGRADE:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.UP_9)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UP_9:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.UP_12)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UP_12:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self._set_state(State.CLOSE)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.CLOSE:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None
                self.imgs[self.state] = self.screenshot
                self.canvas.delete(self.canvas_screenshot)
                self.canvas_screenshot = None

                self._set_state(State.UP_RESULT_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.UP_RESULT_SCREEN:
                self.imgs[self.state] = self.screenshot

                self._set_state(State.OK)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.OK:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None
                self.imgs[self.state] = self.screenshot
                self.canvas.delete(self.canvas_screenshot)
                self.canvas_screenshot = None

                self._set_state(State.SELL_CONFIRM_SCREEN)
                self._set_canvas_state(CanvasState.SCREENSHOT)

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.SELL_CONFIRM_SCREEN:
                self.imgs[self.state] = self.screenshot

                self._set_state(State.YES)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.YES:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None
                self.imgs[self.state] = self.screenshot
                self.canvas.delete(self.canvas_screenshot)
                self.canvas_screenshot = None

                self._set_state(State.SELL_CONFIRM_SCREEN2)
                self._set_canvas_state(CanvasState.SCREENSHOT)

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.SELL_CONFIRM_SCREEN2:
                self.imgs[self.state] = self.screenshot

                self._set_state(State.YES2)
                self._set_canvas_state(CanvasState.BUTTON)

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.YES2:
                self.coords[self.state] = self.coordinates

                print(self.coords)
                with open("json-dump.json", "w") as file:
                    data = json.dumps(self.coords, indent=2)
                    file.write(data)
            case _:
                print("How?")
        self.label.config(text=self.state)

    def on_combobox_selected(self, _) -> None:
        selected = ast.literal_eval(self._combobox.get())
        self.marker = self._rune_rows[selected]

    def add_clicked(self) -> None:
        self.coordinates = (5, 5)
        self.marker = self.draw_circle(*self.coordinates)
        self._rune_rows[self.coordinates] = self.marker
        self._combobox.configure(values=[str(c) for c in self._rune_rows.keys()])
        self._combobox.set(str(self.coordinates))

    def delete_clicked(self) -> None:
        if len(self._rune_rows) <= 1:
            return

        selected = ast.literal_eval(self._combobox.get())
        self.marker = self._rune_rows[selected]
        del self._rune_rows[selected]
        self.canvas.delete(self.marker)

        new_selected, self.marker = list(self._rune_rows.items())[0]
        self._combobox.configure(values=[str(c) for c in self._rune_rows.keys()])
        self._combobox.set(str(new_selected))

    def _update_rune_rows(self) -> None:
        if self.state != State.RUNES_ROW:
            return

        selected = ast.literal_eval(self._combobox.get())
        del self._rune_rows[selected]
        self._rune_rows[self.coordinates] = self.marker
        self._combobox.configure(values=[str(c) for c in self._rune_rows.keys()])
        self._combobox.set(str(self.coordinates))

    def on_mouse_click(self, event):
        x, y = event.x, event.y
        if self.canvas_state == CanvasState.ROI:
            if self.marker is not None:
                self.canvas.delete(self.marker)
            self.start_coords = (x, y)
            self.coordinates = (x, y, x, y)
            self.marker = self.canvas.create_rectangle(*self.coordinates)
        elif self.canvas_state == CanvasState.BUTTON:
            if self.marker is not None:
                self.canvas.delete(self.marker)
            self.coordinates = (x, y)
            self.marker = self.draw_circle(*self.coordinates)
            self._update_rune_rows()

    def draw_circle(self, x, y):
        r = 5
        return self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

    def on_mouse_drag(self, event):
        if self.canvas_state == CanvasState.ROI:
            sx, sy = self.start_coords
            x, y = event.x, event.y
            if self.marker is not None:
                self.canvas.delete(self.marker)
            self.coordinates = (sx, sy, x, y)
            self.marker = self.canvas.create_rectangle(*self.coordinates)

    def _set_canvas_state(self, state: CanvasState) -> None:
        if state == CanvasState.SCREENSHOT:
            self.builder.get_object("screenshot")["state"] = "normal"
        else:
            self.builder.get_object("screenshot")["state"] = "disabled"
        self.canvas_state = state

    def _set_state(self, state: State) -> None:
        if state == State.RUNES_ROW:
            self._combobox["state"] = "readonly"
            self.builder.get_object("add")["state"] = "normal"
            self.builder.get_object("delete")["state"] = "normal"
        else:
            self._combobox["state"] = "disabled"
            self._combobox.set("")
            self.builder.get_object("add")["state"] = "disabled"
            self.builder.get_object("delete")["state"] = "disabled"
        self.state = state


if __name__ == '__main__':
    marker = ScreenMarker()
    marker.run()

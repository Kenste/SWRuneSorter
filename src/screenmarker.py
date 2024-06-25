from enum import StrEnum

import pygubu
from PIL import ImageGrab, ImageTk

import json


class CanvasState(StrEnum):
    ROI = "ROI"
    BUTTON = "BUTTON"
    SCREENSHOT = "SCREENSHOT"


class State(StrEnum):
    INITIAL_SCREEN = "Initial Screen"
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
    YES = "yes"
    SELL_CONFIRM_SCREEN2 = "Sell Confirm 6* Legend Screen"
    YES2 = "yes 6* Legend"



class ScreenMarker:
    def __init__(self):
        self.builder = pygubu.Builder()
        self.builder.add_from_file("../resources/screenmarker.ui")
        self.mainwindow = self.builder.get_object("mainframe")
        self.canvas = self.builder.get_object("canvas")
        self.label = self.builder.get_object("promptLabel")

        self.canvas_screenshot = None
        self.screenshot = None
        self.marker = None
        self.canvas_state = CanvasState.SCREENSHOT
        self.state = State.INITIAL_SCREEN
        self.label.config(text=self.state)

        self.imgs = {}
        self.coordinates = ()
        self.coords = {}

        self.builder.connect_callbacks(self)
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

    def run(self) -> None:
        self.mainwindow.mainloop()

    def screenshotClicked(self) -> None:
        if self.canvas_state != CanvasState.SCREENSHOT:
            return

        if self.canvas_screenshot is not None:
            self.canvas.delete(self.canvas_screenshot)
        img = ImageGrab.grab()
        self.screenshot = ImageTk.PhotoImage(img)
        self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
        self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())

    def previousClicked(self) -> None:
        match self.state:
            case State.INITIAL_SCREEN:
                # Do nothing, as there is no prior state
                pass
            case State.RUNE_SLOT_1:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.INITIAL_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT
            case State.RUNE_SLOT_2:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_1
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_3:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_2
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_4:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_3
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_5:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_4
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_6:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None
                self.imgs[self.state] = self.screenshot

                self.state = State.RUNE_SLOT_5
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SCREEN:
                self.imgs[self.state] = self.screenshot

                self.state = State.RUNE_SLOT_6
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.POWER_UP:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT
            case State.SELL:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.POWER_UP
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_NAME:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.SELL
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_MAIN:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_NAME
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_INNATE:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_MAIN
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_SUBS:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_INNATE
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_QUALITY:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SUBS
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.POWER_UP_SCREEN:
                self.imgs[self.state] = self.screenshot

                self.state = State.RUNE_QUALITY
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.UPGRADE:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.POWER_UP_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT
            case State.UP_9:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.UPGRADE
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UP_12:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.UP_9
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.CLOSE:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.UP_12
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UP_RESULT_SCREEN:
                self.imgs[self.state] = self.screenshot

                self.state = State.CLOSE
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.OK:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.UP_RESULT_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT
            case State.SELL_CONFIRM_SCREEN:
                self.imgs[self.state] = self.screenshot

                self.state = State.OK
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.YES:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.SELL_CONFIRM_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT
            case State.SELL_CONFIRM_SCREEN2:
                self.imgs[self.state] = self.screenshot

                self.state = State.YES
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.YES2:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.SELL_CONFIRM_SCREEN2
                self.canvas_state = CanvasState.SCREENSHOT
            case _:
                print("How?")
        self.label.config(text=self.state)

    def nextClicked(self) -> None:
        match self.state:
            case State.INITIAL_SCREEN:
                # save current state
                self.imgs[self.state] = self.screenshot

                # prepare next state
                self.state = State.RUNE_SLOT_1
                self.canvas_state = CanvasState.BUTTON

                # load next state if already visited
                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_1:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_2
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_2:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_3
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_3:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_4
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_4:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_5
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.RUNE_SLOT_5:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SLOT_6
                self.canvas_state = CanvasState.BUTTON

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

                self.state = State.RUNE_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.RUNE_SCREEN:
                self.imgs[self.state] = self.screenshot

                self.state = State.POWER_UP
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.POWER_UP:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.SELL
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.SELL:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_NAME
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_NAME:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_MAIN
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_MAIN:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_INNATE
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_INNATE:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_SUBS
                self.canvas_state = CanvasState.ROI

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.canvas.create_rectangle(*self.coordinates)
            case State.RUNE_SUBS:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.RUNE_QUALITY
                self.canvas_state = CanvasState.ROI

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

                self.state = State.POWER_UP_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.POWER_UP_SCREEN:
                self.imgs[self.state] = self.screenshot

                self.state = State.UPGRADE
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UPGRADE:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.UP_9
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UP_9:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.UP_12
                self.canvas_state = CanvasState.BUTTON

                if self.state in self.coords:
                    self.coordinates = self.coords[self.state]
                    self.marker = self.draw_circle(*self.coords[self.state])
            case State.UP_12:
                self.coords[self.state] = self.coordinates
                self.canvas.delete(self.marker)
                self.marker = None

                self.state = State.CLOSE
                self.canvas_state = CanvasState.BUTTON

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

                self.state = State.UP_RESULT_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.UP_RESULT_SCREEN:
                self.imgs[self.state] = self.screenshot

                self.state = State.OK
                self.canvas_state = CanvasState.BUTTON

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

                self.state = State.SELL_CONFIRM_SCREEN
                self.canvas_state = CanvasState.SCREENSHOT

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.SELL_CONFIRM_SCREEN:
                self.imgs[self.state] = self.screenshot

                self.state = State.YES
                self.canvas_state = CanvasState.BUTTON

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

                self.state = State.SELL_CONFIRM_SCREEN2
                self.canvas_state = CanvasState.SCREENSHOT

                if self.state in self.imgs:
                    self.screenshot = self.imgs[self.state]
                    self.canvas_screenshot = self.canvas.create_image(0, 0, image=self.screenshot, anchor="nw")
                    self.canvas.configure(width=self.screenshot.width(), height=self.screenshot.height())
            case State.SELL_CONFIRM_SCREEN2:
                self.imgs[self.state] = self.screenshot

                self.state = State.YES2
                self.canvas_state = CanvasState.BUTTON

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
        print("on_combobox_selected not yet implemented")

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
            # self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

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


if __name__ == '__main__':
    marker = ScreenMarker()
    marker.run()

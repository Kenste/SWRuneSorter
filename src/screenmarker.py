import pygubu


class ScreenMarker:
    def __init__(self):
        self.builder = pygubu.Builder()
        self.builder.add_from_file("../resources/screenmarker.ui")
        self.mainwindow = self.builder.get_object("mainframe")

        self.builder.connect_callbacks(self)

    def run(self) -> None:
        self.mainwindow.mainloop()

    def screenshotClicked(self) -> None:
        print("screenshotClicked not yet implemented")

    def previousClicked(self) -> None:
        print("previousClicked not yet implemented")

    def nextClicked(self) -> None:
        print("nextClicked not yet implemented")

    def on_combobox_selected(self, _) -> None:
        print("on_combobox_selected not yet implemented")


if __name__ == '__main__':
    marker = ScreenMarker()
    marker.run()

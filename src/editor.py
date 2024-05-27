import pygubu
import logging


class Editor:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file("../resources/json editor.ui")
        self.mainwindow = builder.get_object("editorWindow")
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def add_profile_clicked(self):
        # TODO: missing implementation
        logging.error(f"add_profile_clicked not yet implemented!")

    def save_json_clicked(self):
        # TODO: missing implementation
        logging.error(f"save_json_clicked not yet implemented!")

    def load_json_clicked(self):
        # TODO: missing implementation
        logging.error(f"load_json_clicked not yet implemented!")

    def validate_float_entry(self, new_value):
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def on_combobox_selected(self):
        # TODO: missing implementation
        logging.error(f"on_combobox_selected not yet implemented!")


if __name__ == '__main__':
    editor = Editor()
    editor.run()

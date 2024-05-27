import pygubu


class Editor:
    def __init__(self):
        self.builder = builder = pygubu.Builder()
        builder.add_from_file("../resources/json editor.ui")
        self.mainwindow = builder.get_object("editorWindow")
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    editor = Editor()
    editor.run()

from tkinter import StringVar


class FloatVar(StringVar):
    def __init__(self):
        super().__init__()
        self._on_change_function = None
        self.trace("w", lambda a, b, c: self._on_value_change())

    def _on_value_change(self) -> None:
        if self._on_change_function is not None:
            self._on_change_function(self)

    def float_value(self) -> float:
        """
        Returns the float value of this FloatVar or 1 by default.
        :return: the stored float value or 1
        """
        value = self.get()
        if value == "":
            return 1.
        return float(value)

    def set_on_change_function(self, f) -> None:
        """
        Sets the callback function to call when the value has changed.
        The function has to expect one parameter, which will be the (this) instance of the FloatVar calling the callback.
        :param f: the callback function
        """
        self._on_change_function = f

    def __hash__(self):
        return id(self)

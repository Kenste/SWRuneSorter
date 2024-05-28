import logging
from tkinter import filedialog, StringVar, messagebox

import pygubu

import runescorer.scorer as scorer
from runescorer.constants import Stat, sub_upgrade_range
from runescorer.weight import WeightProfile
from util import json_helper
from util.floatvar import FloatVar

stat_weight_components = [
    ("ATKEntry1", "ATKLabel1", Stat.ATK),
    ("ATKPEntry1", "ATKPLabel1", Stat.ATK_P),
    ("DEFEntry1", "DEFLabel1", Stat.DEF),
    ("DEFPEntry1", "DEFPLabel1", Stat.DEF_P),
    ("HPEntry1", "HPLabel1", Stat.HP),
    ("HPPEntry1", "HPPLabel1", Stat.HP_P),
    ("SPDEntry1", "SPDLabel1", Stat.SPD),
    ("CRateEntry1", "CRateLabel1", Stat.CRate),
    ("CDmgEntry1", "CDmgLabel1", Stat.CDmg),
    ("RESEntry1", "RESLabel1", Stat.RES),
    ("ACCEntry1", "ACCLabel1", Stat.ACC),
]

innate_weight_components = [
    ("ATKEntry2", "ATKLabel2", Stat.ATK),
    ("ATKPEntry2", "ATKPLabel2", Stat.ATK_P),
    ("DEFEntry2", "DEFLabel2", Stat.DEF),
    ("DEFPEntry2", "DEFPLabel2", Stat.DEF_P),
    ("HPEntry2", "HPLabel2", Stat.HP),
    ("HPPEntry2", "HPPLabel2", Stat.HP_P),
    ("SPDEntry2", "SPDLabel2", Stat.SPD),
    ("CRateEntry2", "CRateLabel2", Stat.CRate),
    ("CDmgEntry2", "CDmgLabel2", Stat.CDmg),
    ("RESEntry2", "RESLabel2", Stat.RES),
    ("ACCEntry2", "ACCLabel2", Stat.ACC),
]


class Editor:
    def __init__(self):
        self.profiles = {}
        self.current_profile = None

        self.builder = pygubu.Builder()
        self.builder.add_from_file("../resources/json editor.ui")
        self.mainwindow = self.builder.get_object("editorWindow")

        self.combobox = self.builder.get_object("box")
        self.name_var = StringVar()
        self.name_var.trace("w", self._name_var_changed)
        self.name_entry = self.builder.get_object("nameEntry")
        self.name_entry.config(textvariable=self.name_var)

        self.builder.connect_callbacks(self)

        self.triple_var = FloatVar()
        self.triple_entry = self.builder.get_object("tripleEntry")
        self.quad_var = FloatVar()
        self.quad_entry = self.builder.get_object("quadEntry")
        self.component_map_stat = {}
        self.component_map_innate = {}
        self.init_float_vars()

    def run(self) -> None:
        self.mainwindow.mainloop()

    def add_profile_clicked(self) -> None:
        logging.info("Creating new weight profile with default values")
        stat_weights = {}
        innate_weights = {}
        for stat in Stat:
            stat_weights[stat] = 1
            innate_weights[stat] = 1
        # Find unique available name
        name = "Name"
        i = 1
        while name in self.profiles.keys():
            if name + str(i) not in self.profiles.keys():
                name += str(i)
            i += 1

        profile = WeightProfile(name, stat_weights, innate_weights, 1, 1)
        scorer.add_profile(profile)
        self.current_profile = profile
        self._update_profile_list()
        self._map_profile_values_to_entries()

    def save_json_clicked(self) -> None:
        logging.info("Selecting JSON file to save to...")
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            logging.info("No file selected")
            return

        logging.info("Saving file")
        json_helper.profiles_to_json(file_path, scorer.get_profiles())

    def load_json_clicked(self) -> None:
        logging.info("Selecting JSON file to parse...")
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            logging.info("NO file selected")
            return

        logging.info("Parsing JSON file")
        profiles = json_helper.weight_profiles_from_json(file_path)
        for profile in profiles:
            scorer.add_profile(profile)
        self.current_profile = scorer.get_profiles()[0]
        self._update_profile_list()
        self._map_profile_values_to_entries()

    def validate_float_entry(self, new_value: str) -> bool:
        if new_value == "":
            return True
        try:
            float(new_value)
            return True
        except ValueError:
            return False

    def on_combobox_selected(self, _) -> None:
        self.current_profile = self.profiles[self.combobox.get()]
        logging.info(f"Selected profile '{self.current_profile.name}'")
        self._map_profile_values_to_entries()

    def _update_profile_list(self) -> None:
        logging.info("Updating combobox values!")
        self.profiles.clear()
        for profile in scorer.get_profiles():
            self.profiles[profile.name] = profile
        self.combobox.configure(values=self.profiles.keys())
        self.combobox.set(self.current_profile.name)

    def _name_var_changed(self, a, b, c) -> None:
        name = self.name_var.get()
        if name != self.current_profile.name and name in self.profiles.keys():
            # TODO: improve the annoying clarification that the name cannot be used
            messagebox.showerror("Invalid Name",
                                 f"The entered name '{name}' cannot be used. The name has to be unique!")
            return

        if self.current_profile is None:
            return

        self.current_profile.name = name
        self._update_profile_list()

    def _map_profile_values_to_entries(self):
        self.name_entry["state"] = "normal"
        self.name_var.set(self.current_profile.name)

        self.triple_entry["state"] = "normal"
        self.triple_var.set(self.current_profile.get_triple_scale())

        self.quad_entry["state"] = "normal"
        self.quad_var.set(self.current_profile.get_quad_scale())

        for var, (entry, _, stat) in self.component_map_stat.items():
            entry["state"] = "normal"
            var.set(self.current_profile.get_stat_weight(stat))
        for var, (entry, _, stat) in self.component_map_innate.items():
            entry["state"] = "normal"
            var.set(self.current_profile.get_innate_weight(stat))

    def _on_change_helper(self, var):
        val = var.float_value()
        if var in self.component_map_stat:
            _, label, stat = self.component_map_stat[var]
            self.current_profile.set_stat_weight(stat, val)
        else:
            _, label, stat = self.component_map_innate[var]
            self.current_profile.set_innate_weight(stat, val)
        max_roll = sub_upgrade_range.get(stat)[1]
        label.config(text=f"= {max_roll * val}")

    def init_float_vars(self):
        self.triple_entry.config(textvariable=self.triple_var)
        self.triple_var.set_on_change_function(lambda var: self.current_profile.set_triple_scale(var.float_value()))

        self.quad_entry.config(textvariable=self.quad_var)
        self.quad_var.set_on_change_function(lambda var: self.current_profile.set_quad_scale(var.float_value()))

        for entryID, labelID, stat in stat_weight_components:
            var = FloatVar()
            entry = self.builder.get_object(entryID)
            entry.config(textvariable=var)
            label = self.builder.get_object(labelID)
            self.component_map_stat[var] = (entry, label, stat)
            var.set_on_change_function(lambda var: self._on_change_helper(var))

        for entryID, labelID, stat in innate_weight_components:
            var = FloatVar()
            entry = self.builder.get_object(entryID)
            entry.config(textvariable=var)
            label = self.builder.get_object(labelID)
            self.component_map_innate[var] = (entry, label, stat)
            var.set_on_change_function(lambda var: self._on_change_helper(var))


if __name__ == '__main__':
    editor = Editor()
    editor.run()

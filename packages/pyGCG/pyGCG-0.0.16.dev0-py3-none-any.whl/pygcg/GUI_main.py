import customtkinter as ctk
from pathlib import Path
import tomlkit
from astropy.table import QTable
from .tabs.spectrum import SpecFrame
from .tabs.beams import BeamFrame
from .windows.settings import SettingsWindow
from .windows.comments import CommentsWindow
import numpy as np

class GCG(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Geometry
        # self.geometry("1280x720")
        self.geometry("1366x768")
        self.minsize(1280, 720)
        # self.attributes("-zoomed", True)
        self.title("GLASS-JWST Classification GUI")

        self.initialise_configuration()
        self.settings_window = None
        self.comments_window = None

        # Key bindings
        self.protocol("WM_DELETE_WINDOW", self.quit_gracefully)
        self.bind("<Control-q>", self.quit_gracefully)
        self.bind("<Left>", self.prev_gal_button_callback)
        self.bind("<Right>", self.next_gal_button_callback)

        # configure grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Setup bottom navigation buttons
        self.open_settings_button = ctk.CTkButton(
            self,
            text="Settings",
            command=self.open_settings_callback,
        )
        self.open_settings_button.grid(
            row=1,
            column=1,
            padx=20,
            pady=20,
            sticky="ew",
        )

        self.prev_gal_button = ctk.CTkButton(
            self,
            text="Previous",
            command=self.prev_gal_button_callback,
        )
        self.prev_gal_button.grid(
            row=1,
            column=0,
            padx=20,
            pady=20,
        )
        self.next_gal_button = ctk.CTkButton(
            self,
            text="Next",
            command=self.next_gal_button_callback,
        )
        self.next_gal_button.grid(
            row=1,
            column=5,
            padx=20,
            pady=20,
        )
        self.comments_button = ctk.CTkButton(
            self,
            text="Comments",
            command=self.gal_comments_button_callback,
        )
        self.comments_button.grid(
            row=1,
            column=4,
            padx=20,
            pady=20,
            sticky="ew",
        )

        self.id_list = np.array(
            sorted(
                [
                    f.stem[-8:-3]
                    for f in (
                        Path(self.full_config["files"]["extractions_dir"])
                        .expanduser()
                        .resolve()
                    ).glob(f"*.1D.fits")
                ]
            )
        )

        self.current_gal_data = {}

        # self.current_gal_entry = ctk.CTkEntry(
        #     self,
        #     text="Save Galaxy",
        #     command=self.save_gal_button_callback,
        # )
        # self.save_gal_button.grid(
        #     row=1,
        #     column=3,
        #     padx=20,
        #     pady=20,
        #     # sticky="news",
        # )
        self.current_gal_id = ctk.StringVar(
            master=self,
            value=self.id_list[-6],
        )
        self.current_gal_label = ctk.CTkLabel(
            self,
            text="Current ID:",
        )
        self.current_gal_label.grid(
            row=1,
            column=2,
            padx=(20, 5),
            pady=20,
            sticky="e",
        )
        self.current_gal_entry = ctk.CTkEntry(
            self,
            textvariable=self.current_gal_id,
        )
        self.current_gal_entry.grid(
            row=1,
            column=3,
            padx=(5, 20),
            pady=20,
            sticky="w",
        )
        self.current_gal_entry.bind(
            "<Return>",
            self.change_gal_id,
        )

        self.main_tabs = MyTabView(
            master=self,
            # tab_names=["Beam view", "Spec view"],
            tab_names=["Spec view", "Beam view"],
            command=self.main_tabs_update,
            # expose_bind_fns=[self._test_pr
            # int_e, self._test_print_e]
        )
        self.main_tabs.grid(
            row=0, column=0, padx=20, pady=0, columnspan=6, sticky="news"
        )

        # self.current_gal_id = 3927
        # self.current_gal_id = 1864
        # self.current_gal_id = 1494
        # self.current_gal_id = 1338

        self.muse_spec_frame = SpecFrame(
            self.main_tabs.tab("Spec view"), self.current_gal_id.get()
        )
        # self.muse_spec_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.muse_spec_frame.pack(fill="both", expand=1)

        self.full_beam_frame = BeamFrame(
            self.main_tabs.tab("Beam view"), self.current_gal_id.get()
        )
        # self.muse_spec_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.full_beam_frame.pack(fill="both", expand=1)

        # print (dir(self.main_tabs.tab("Spec view")))

    def initialise_configuration(self):
        try:
            with open(Path(__file__).parent / "base_config.toml", "rt") as fp:
                self.base_config = tomlkit.load(fp)
                assert self.base_config["files"]["full_config_path"]
        except:
            self.base_config = self.write_base_config()

        try:
            with open(
                Path(self.base_config["files"]["full_config_path"])
                .expanduser()
                .resolve(),
                "rt",
            ) as fp:
                self.full_config = tomlkit.load(fp)
                self.write_full_config(self.full_config)

        except FileNotFoundError:
            print(
                "Configuration file not found at the specified location. Creating new config from defaults."
            )
            self.full_config = self.write_full_config(self.base_config)

        ctk.set_appearance_mode(
            self.full_config["appearance"]["appearance_mode"].lower()
        )
        ctk.set_default_color_theme(self.full_config["appearance"]["theme"].lower())

    def write_base_config(self):
        doc = tomlkit.document()
        doc.add(
            tomlkit.comment(
                "This is the base configuration file, which stores the settings used previously."
            )
        )
        doc.add(tomlkit.nl())
        doc.add("title", "Base Configuration")

        files = tomlkit.table()
        files.add("full_config_path", str(Path(__file__).parent / "base_config.toml"))
        files["full_config_path"].comment(
            "The location of the primary configuration file."
        )

        doc.add("files", files)

        with open(files["full_config_path"], mode="wt", encoding="utf-8") as fp:
            tomlkit.dump(doc, fp)

        return doc

    def write_full_config(self, doc):
        # Files
        try:
            files = doc["files"]
        except:
            files_tab = tomlkit.table()
            doc.add("files", files_tab)
            files = doc["files"]

        try:
            files["temp_dir"]
        except:
            files.add("temp_dir", "~/.pyGCG_temp")
            files["temp_dir"].comment(
                "The directory in which temporary files are stored."
            )
        Path(files["temp_dir"]).expanduser().resolve().mkdir(
            exist_ok=True, parents=True
        )

        try:
            files["extractions_dir"]
        except:
            files.add("extractions_dir", "")
            files["extractions_dir"].comment(
                "The directory in which NIRISS extractions are stored."
            )

        try:
            files["prep_dir"]
        except:
            files.add("prep_dir", "")
            files["prep_dir"].comment(
                "The directory containing the segmentation map and direct images."
            )

        try:
            files["cube_path"]
        except:
            files.add("cube_path", "")
            files["cube_path"].comment(
                "[optional] The file path of the corresponding MUSE datacube."
            )

        try:
            files["cat_path"]
        except Exception as e:
            print(e)
            self.cat = None
            files.add("cat_path", "")
            files["cat_path"].comment(
                "[optional] The file path of the NIRISS catalogue (FINISH DESCRIPTION LATER)."
            )
        try:
            self.cat = QTable.read(Path(files["cat_path"]).expanduser().resolve())
        except:
            self.cat = None

        # Appearance
        try:
            appearance = doc["appearance"]
        except:
            appearance_tab = tomlkit.table()
            doc.add("appearance", appearance_tab)
            appearance = doc["appearance"]

        try:
            appearance["appearance_mode"]
        except:
            appearance.add("appearance_mode", "system")
            appearance["appearance_mode"].comment("System (default), light, or dark.")

        try:
            appearance["theme"]
        except:
            appearance.add("theme", "blue")
            appearance["theme"].comment(
                "Blue (default), dark-blue, or green. The CustomTKinter color theme. "
                + "Can also point to the location of a custom .json file describing the desired theme."
            )

        # Lines
        try:
            lines = doc["lines"]
        except:
            lines_tab = tomlkit.table()
            lines_tab.add(
                tomlkit.comment(
                    "These tables define the lines shown in the redshift tab."
                )
            )
            lines_tab.add(tomlkit.nl())
            doc.add(tomlkit.nl())
            doc.add("lines", lines_tab)
            lines = doc["lines"]

        try:
            emission = lines["emission"]
        except:
            lines.add("emission", tomlkit.table().indent(4))
            emission = lines["emission"]
            emission.add(tomlkit.comment("These are the emission lines."))
            emission.add(tomlkit.nl())
            # appearance["appearance_mode"].comment("System (default), light, or dark.")

        em_lines = {
            "Lyman_alpha": {
                "latex_name": r"Ly$\alpha$",
                "centre": 1215.24,
            },
            "CIV_1549": {
                "latex_name": r"C IV",
                "centre": 1549.48,
            },
            "H_delta": {
                "latex_name": r"H$\delta$",
                "centre": 4102.89,
            },
            "OIII_4364": {
                "latex_name": r"OIII",
                "centre": 4364.436,
            },
            "H_gamma": {
                "latex_name": r"H$\gamma$",
                "centre": 4341.68,
            },
            "H_beta": {
                "latex_name": r"H$\beta$",
                "centre": 4862.68,
            },
            "NII_6550": {
                "latex_name": r"NII",
                "centre": 6549.86,
            },
            "H_alpha": {
                "latex_name": r"H$\alpha$",
                "centre": 6564.61,
            },
            "NII_6585": {
                "latex_name": r"NII",
                "centre": 6585.27,
            },
            "PaE": {
                "latex_name": r"Pa-$\eta$",
                "centre": 9548.6,
            },
            "PaD": {
                "latex_name": r"Pa-$\delta$",
                "centre": 10052.1,
            },
            "PaG": {
                "latex_name": r"Pa-$\gamma$",
                "centre": 10941.1,
            },
            "PaB": {
                "latex_name": r"Pa-$\beta$",
                "centre": 12821.6,
            },
            "PaA": {
                "latex_name": r"Pa-$\alpha$",
                "centre": 18756.1,
            },
            "SII_6718": {
                "latex_name": r"SII",
                "centre": 6718.29,
            },
            "SII_6733": {
                "latex_name": r"SII",
                "centre": 6732.67,
            },
            "SIII_9069": {
                "latex_name": r"SIII",
                "centre": 9068.6,
            },
            "HeI_10830": {
                "latex_name": r"HeI",
                "centre": 10830.3398,
            },
            "OIII_4960": {
                "latex_name": r"OIII",
                "centre": 4960.295,
            },
            "OIII_5008": {
                "latex_name": r"OIII",
                "centre": 5008.240,
            },
        }

        for line_name, line_data in em_lines.items():
            try:
                emission[line_name]
                for key in line_data.keys():
                    emission[line_name][key]
            except:
                emission.add(line_name, tomlkit.table().indent(8))
                for key, value in line_data.items():
                    emission[line_name].add(key, value)
                emission.add(tomlkit.nl())

        try:
            absorption = lines["absorption"]
        except:
            lines.add("absorption", tomlkit.table().indent(4))
            absorption = lines["absorption"]
            absorption.add(tomlkit.comment("These are the absorption lines."))
            absorption.add(tomlkit.nl())
            # appearance["appearance_mode"].comment("System (default), light, or dark.")

        ab_lines = {
            "K_3935": {
                "latex_name": r"K",
                "centre": 3934.777,
            },
            "H_3970": {
                "latex_name": r"H",
                "centre": 3969.588,
            },
            "G_4306": {
                "latex_name": r"G",
                "centre": 4305.61,
            },
            "Mg_5177": {
                "latex_name": r"Mg",
                "centre": 5176.7,
            },
            "Na_5896": {
                "latex_name": r"Na",
                "centre": 5895.6,
            },
            "Ca_8500": {
                "latex_name": r"CaII",
                "centre": 8500.36,
            },
            "Ca_8544": {
                "latex_name": r"CaII",
                "centre": 8544.44,
            },
            "Ca_8564": {
                "latex_name": r"CaII",
                "centre": 8564.52,
            },
        }

        for line_name, line_data in ab_lines.items():
            try:
                absorption[line_name]
                for key in line_data.keys():
                    absorption[line_name][key]
            except:
                absorption.add(line_name, tomlkit.table().indent(8))
                for key, value in line_data.items():
                    absorption[line_name].add(key, value)
                absorption.add(tomlkit.nl())
        # try:
        #     emission["Halpha"]
        # except:
        #     emission.add("Halpha", "test")
        #     # appearance["theme"].comment(
        #     #     "Blue (default), dark-blue, or green. The CustomTKinter color theme. "
        #     #     + "Can also point to the location of a custom .json file describing the desired theme."
        #     # )

        # print (doc)
        # print (self.base_config["files"]["full_config_path"])

        with open(
            Path(self.base_config["files"]["full_config_path"]).expanduser().resolve(),
            mode="wt",
            encoding="utf-8",
        ) as fp:
            tomlkit.dump(doc, fp)

        return doc

    def open_settings_callback(self):
        if self.settings_window is None or not self.settings_window.winfo_exists():
            self.settings_window = SettingsWindow(
                self
            )  # create window if its None or destroyed
        else:
            self.settings_window.focus()

    def gal_comments_button_callback(self):
        # print("Comments button clicked!")

        if self.comments_window is None or not self.comments_window.winfo_exists():
            self.comments_window = CommentsWindow(
                self
            )  # create window if its None or destroyed
        else:
            self.comments_window.focus()

    def prev_gal_button_callback(self, event=None):
        if self.main_tabs.get() == "Beam view":
            current_PA_idx = self.full_beam_frame.PA_menu.cget("values").index(self.full_beam_frame.PA_menu.get())
            if current_PA_idx==0:
                current_gal_idx = (self.id_list == f"{self.current_gal_id.get():0>5}").nonzero()[0]
                self.current_gal_id.set(self.id_list[current_gal_idx - 1][0])
                self.main_tabs.set("Spec view")
                self.change_gal_id()
                # self.muse_spec_frame.update_plot()
            elif current_PA_idx==1:
                self.full_beam_frame.PA = self.full_beam_frame.PA_menu.cget("values")[0]
                self.full_beam_frame.PA_menu.set(self.full_beam_frame.PA)
                self.full_beam_frame.update_grid()
            elif current_PA_idx==2:
                self.full_beam_frame.PA = self.full_beam_frame.PA_menu.cget("values")[1]
                self.full_beam_frame.PA_menu.set(self.full_beam_frame.PA)
                self.full_beam_frame.update_grid()
        elif self.main_tabs.get() == "Spec view":
                self.main_tabs.set("Beam view")
                self.full_beam_frame.PA = self.full_beam_frame.PA_menu.cget("values")[1]
                self.full_beam_frame.PA_menu.set(self.full_beam_frame.PA)
                self.change_gal_id()
                # self.full_beam_frame.update_grid()

    def next_gal_button_callback(self, event=None):

        if self.main_tabs.get() == "Beam view":
            current_PA_idx = self.full_beam_frame.PA_menu.cget("values").index(self.full_beam_frame.PA_menu.get())
            if current_PA_idx==0:
                self.full_beam_frame.PA = self.full_beam_frame.PA_menu.cget("values")[1]
                self.full_beam_frame.PA_menu.set(self.full_beam_frame.PA)
                self.full_beam_frame.update_grid(force_update=True)
            elif current_PA_idx==1 or current_PA_idx==2:
                self.main_tabs.set("Spec view")
                self.muse_spec_frame.update_plot()
        elif self.main_tabs.get() == "Spec view":
            current_gal_idx = (self.id_list == f"{self.current_gal_id.get():0>5}").nonzero()[0]
            self.current_gal_id.set(self.id_list[current_gal_idx + 1][0])
            self.main_tabs.set("Beam view")
            self.full_beam_frame.PA = self.full_beam_frame.PA_menu.cget("values")[0]
            self.full_beam_frame.PA_menu.set(self.full_beam_frame.PA)
            self.change_gal_id()
            # self.full_beam_frame.update_grid()
                # self.full_beam_frame.PA = self.full_beam_frame.PA_menu.cget("values")[1]
                # self.full_beam_frame.PA_menu.set(self.full_beam_frame.PA)
                # self.full_beam_frame.update_grid(force_update=True)


    def change_gal_id(self, event=None):
        # print (event)
        # self.current_gal_id.set(str(int(self.current_gal_id.get())+1))
        # self.current_gal_id += relative_change
        # print(self.current_gal_id)
        ### This is where the logic for loading/updating the tables will go
        self.current_gal_data = {}
        self.main_tabs_update()

    def main_tabs_update(self):
        if self.main_tabs.get() == "Spec view":
            self.muse_spec_frame.update_plot()
        if self.main_tabs.get() == "Beam view":
            self.full_beam_frame.update_grid()

    def quit_gracefully(self, event=None):
        # Put some lines here to save current output
        self.write_full_config(self.full_config)
        # quit()
        self.quit()

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, tab_names, expose_bind_fns=None, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        for i, name in enumerate(tab_names):
            self.add(name)
            try:
                self.tab(name).bind("<<TabChanged>>", expose_bind_fns[i])
            # print ("success")
            except:
                pass

def run_app():
    app = GCG()
    app.mainloop()
    app.withdraw()
    # app.destroy()
    # del app

# if __name__ == "__main__":
#     run_app()

# PyCube (redshift visualisation)
# Marz (MUSE redshift fits)
# Goel Noiret (noinet)
# Bergamini (multiple images)

# Reset redshift to default
# Rearrange layout to focus on single PA at a time
# RGB image and segmentation map viewer

# Add coordinate entry in addition to id
# COmpare redshift - scan wide range with grizli vs photoz
# Talk to Xin/GUido about modelling
# Magnitude limits
# Save individual beams from grizli?
# Add PaE vs [SIII]
# Look at low redshift cluster members - flag up emission/absorption
# Attempt extraction of stripped/jellyfish galaxies
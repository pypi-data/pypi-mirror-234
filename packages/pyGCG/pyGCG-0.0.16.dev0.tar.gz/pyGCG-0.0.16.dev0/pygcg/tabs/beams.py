import customtkinter as ctk
import tkinter as tk
from matplotlib.figure import Figure
import matplotlib.colors as colors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from pathlib import Path
import astropy.io.fits as pf
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
from tqdm import tqdm
import numpy as np
from astropy.table import Table

from astropy.visualization import (
    MinMaxInterval,
    SqrtStretch,
    ImageNormalize,
    LinearStretch,
    LogStretch,
    ManualInterval,
    PercentileInterval,
)


class BeamFrame(ctk.CTkFrame):
    def __init__(self, master, gal_id, **kwargs):
        super().__init__(master, **kwargs)

        self.cmap = "plasma"
        self.PA = "PA 1"
        self.stretch = "Square root"
        self.limits = "grizli default"

        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="ew",
        )

        PA_label = ctk.CTkLabel(self.settings_frame, text="Grism PA:")
        PA_label.grid(row=0, column=0, padx=(20, 5), pady=20, sticky="e")
        self.PA_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            values=["PA 1", "PA 2", "Stack"],
            command=self.change_PA,
        )
        self.PA_menu.grid(row=0, column=1, padx=(5, 20), pady=20, sticky="w")

        self._root().bind("<Up>", self.arrow_change_PA)
        self._root().bind("<Down>", self.arrow_change_PA)

        cmap_label = ctk.CTkLabel(self.settings_frame, text="Colourmap:")
        cmap_label.grid(row=0, column=2, padx=(20, 5), pady=20, sticky="e")
        self.cmap_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            values=[
                "plasma",
                "plasma_r",
                "viridis",
                "viridis_r",
                "jet",
                "binary",
                "binary_r",
            ],
            command=self.change_cmap,
        )
        self.cmap_menu.grid(row=0, column=3, padx=(5, 20), pady=20, sticky="w")

        stretch_label = ctk.CTkLabel(self.settings_frame, text="Image stretch:")
        stretch_label.grid(row=0, column=4, padx=(20, 5), pady=20, sticky="e")
        self.stretch_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            values=["Linear", "Square root", "Logarithmic"],
            command=self.change_stretch,
        )
        self.stretch_menu.set("Square root")
        self.stretch_menu.grid(row=0, column=5, padx=(5, 20), pady=20, sticky="w")

        limits_label = ctk.CTkLabel(self.settings_frame, text="Colourmap limits:")
        limits_label.grid(row=0, column=6, padx=(20, 5), pady=20, sticky="e")
        self.limits_menu = ctk.CTkOptionMenu(
            self.settings_frame,
            values=[
                "grizli default",
                "Min-max",
                "99.9%",
                "99.5%",
                "99%",
                "98%",
                "95%",
                "90%",
            ],
            command=self.change_limits,
        )
        self.limits_menu.grid(row=0, column=7, padx=(5, 20), pady=20, sticky="w")

        self.gal_id = int(gal_id)
        try:
            self.file_path = [
                *(
                    Path(self._root().full_config["files"]["extractions_dir"])
                    .expanduser()
                    .resolve()
                ).glob(f"*{int(gal_id):0>5}.stack.fits")
            ][0]
            self.generate_grid()
        except:
            self.file_path = None

        # if not hasattr(self, "gal_id"):

    def change_PA(self, event=None):
        print(self.PA_menu.cget("values"))
        self.PA = event
        self.update_grid(force_update=True)

    def arrow_change_PA(self, event=None):
        if self._root().main_tabs.get() == "Beam view":
            current_idx = self.PA_menu.cget("values").index(self.PA_menu.get())
            if event.keysym == "Down":
                new_idx = (current_idx + 1) % len(self.PA_menu.cget("values"))
            elif event.keysym == "Up":
                new_idx = (current_idx - 1) % len(self.PA_menu.cget("values"))
            self.PA = self.PA_menu.cget("values")[new_idx]
            self.PA_menu.set(self.PA)
            self.update_grid(force_update=True)

    def change_cmap(self, event=None):
        # print (event)
        self.cmap = event
        self.update_grid(force_update=True)

    def change_stretch(self, event=None):
        self.stretch = event
        self.update_grid(force_update=True)

    def change_limits(self, event=None):
        self.limits = event
        self.update_grid(force_update=True)

    def update_grid(self, force_update=False):
        if self.gal_id == int(self._root().current_gal_id.get()) and not force_update:
            pass
        else:
            #     print("No need to panic.")
            # else:
            self.gal_id = int(self._root().current_gal_id.get())
            self.file_path = [
                *(
                    Path(self._root().full_config["files"]["extractions_dir"])
                    .expanduser()
                    .resolve()
                ).glob(f"*{self.gal_id:0>5}.stack.fits")
            ][0]
            with pf.open(self.file_path) as hdul:
                header = hdul[0].header
                n_grism = header["NGRISM"]
                n_pa = np.nanmax(
                    [
                        header[f"N{header[f'GRISM{n:0>3}']}"]
                        for n in range(1, n_grism + 1)
                    ]
                )
                self.beam_frame_list = []
                # row = 0
                extver_list = []
                # for row, col in np.ndindex(n_pa, n_grism):
                for i in range(n_grism):
                    try:
                        grism_name = header[f"GRISM{i+1:0>3}"]
                        if self.PA == "PA 1":
                            pa = "," + str(header[f"{grism_name}01"])
                        elif self.PA == "PA 2":
                            pa = "," + str(header[f"{grism_name}02"])
                        elif self.PA == "Stack":
                            pa = ""
                        extver = grism_name + pa
                    except:
                        extver = "none"
                    extver_list.append(extver)
                # self.beam_single_PA_frame = SinglePABeamFrame(self, extvers = extver_list)
                self.beam_single_PA_frame.update_plots(extvers=extver_list)

            # self.grid_rowconfigure(1, weight=1)
            # self.grid_columnconfigure(0, weight=1)
        #         header = hdul[0].header
        #         n_grism = header["NGRISM"]
        #         n_pa = np.nanmax(
        #             [
        #                 header[f"N{header[f'GRISM{n:0>3}']}"]
        #                 for n in range(1, n_grism + 1)
        #             ]
        #         )

        # # for n in range(1,header["NGRISM"]+1):
        # #     print (n)
        # #     print (header[f"GRISM{n:0>3}"])
        # #     print (header[f"N{header[f'GRISM{n:0>3}']}"])
        # for idx, beam_sub_frame in enumerate(self.beam_frame_list):
        #     # print (beam_sub_frame.ext, beam_sub_frame.extver)
        #     beam_sub_frame.ext = self.ext
        #     beam_sub_frame.cmap = self.cmap
        #     beam_sub_frame.stretch = self.stretch
        #     beam_sub_frame.limits = self.limits
        #     beam_sub_frame.update_plots()
        # # for row, col in np.ndindex(n_pa+1, n_grism):
        # #     flat_idx = np.ravel_multi_index((row, col), (n_pa+1, n_grism))
        # #     print (flat_idx)
        # # print ("sort this out")

    def generate_grid(self):
        with pf.open(self.file_path) as hdul:
            header = hdul[0].header
            n_grism = header["NGRISM"]
            n_pa = np.nanmax(
                [header[f"N{header[f'GRISM{n:0>3}']}"] for n in range(1, n_grism + 1)]
            )
            self.beam_frame_list = []
            # for
            # This is where I'll set which pa is being used
            row = 0
            extver_list = []
            # for row, col in np.ndindex(n_pa, n_grism):
            for i in range(n_grism):
                grism_name = header[f"GRISM{i+1:0>3}"]
                pa = "," + str(header[f"{grism_name}{row+1:0>2}"])
                extver = grism_name + pa
                extver_list.append(extver)
            self.beam_single_PA_frame = SinglePABeamFrame(self, extvers=extver_list)
            self.beam_single_PA_frame.grid(row=1, column=0, sticky="news")

            self.grid_rowconfigure(1, weight=1)
            self.grid_columnconfigure(0, weight=1)


# class BeamSubFrame(ctk.CTkFrame):
#     def __init__(
#         self,
#         master,
#         gal_id,
#         extver,
#         ext="SCI",
#         cmap="plasma",
#         stretch="Logarithmic",
#         limits="grizli_default",
#         **kwargs,
#     ):
#         super().__init__(master, **kwargs)

#         self.gal_id = gal_id
#         self.extver = extver
#         self.ext = ext
#         self.cmap = cmap
#         self.stretch = stretch
#         self.limits = limits
#         # print (self)
#         self.rowconfigure(0, weight=1)
#         self.rowconfigure(1, weight=0)
#         self.columnconfigure(1, weight=1)

#         self.label = ctk.CTkLabel(self, text="Contamination:")
#         self.label.grid(row=1, column=0, padx=10, pady=(10, 10), sticky="e")

#         self.cont_value = ctk.StringVar(value="None")  # set initial value
#         self.cont_menu = ctk.CTkOptionMenu(
#             self,
#             values=["None", "Mild", "Strong", "Incomplete trace"],
#             command=self.optionmenu_callback,
#             variable=self.cont_value,
#         )
#         self.cont_menu.grid(row=1, column=1, sticky="w")

#         self.file_path = [
#             *(
#                 Path(self._root().full_config["files"]["extractions_dir"])
#                 .expanduser()
#                 .resolve()
#             ).glob(f"*{gal_id:0>5}.stack.fits")
#         ][0]

#         self.update_plots()

#     def optionmenu_callback(choice):
#         print("optionmenu dropdown clicked:", choice)

#     def update_plots(self):
#         if not hasattr(self, "fig_axes"):
#             # self.pad_frame = tk.Frame(self, width=200, height=200, borderwidth=0, background="")
#             # self.pad_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")#, padx=10, pady=20)

#             # self.plot_frame = tk.Frame(
#             #     self,
#             #     bg = "blue",
#             #     width = 300,
#             #     height = 300,
#             #     borderwidth=0,
#             # )
#             # self.plot_frame.rowconfigure(0,weight=1)
#             # self.plot_frame.columnconfigure(0,weight=1)
#             # calls function to fix the aspect ratio
#             # self.set_aspect(self.plot_frame, self.pad_frame, aspect_ratio=5)
#             self.fig = Figure(
#                 constrained_layout=True
#                 # , figsize=(2,1))
#                 ,
#                 figsize=(3, 1),
#             )
#             # print (self.master.winfo_height()/2)
#             # print (self.master.winfo_width()/3)
#             # self.fig.set_figsize(5,1)
#             # print (self.fig.get_size_inches())
#             self.pyplot_canvas = FigureCanvasTkAgg(
#                 figure=self.fig,
#                 master=self,
#             )

#             if not hasattr(self, "plotted_images"):
#                 self.plotted_images = dict()

#             # with pf.open(self.file_path) as hdul:
#             #     # print (hdul["SCI","F115W"])
#             #     shape_sci = hdul.info(output=False)[
#             #         hdul.index_of((self.ext, self.extver))
#             #     ][5][0]
#             #     shape_kernel = hdul.info(output=False)[
#             #         hdul.index_of(("KERNEL", self.extver))
#             #     ][5][0]
#             #     # idx_kernel = hdul.index_of(("KERNEL",self.extver))
#             #     # print (hdul.info(output=False))
#             #     # print (hdul.info(output=False)[idx_sci])
#             #     # print (shape_sci)
#             #     # print (hdul["SCI",self.extver].data.shape)

#             # self.fig.
#             self.fig_axes = self.fig.subplots(
#                 1,
#                 2,
#                 sharey=True,
#                 # aspect="auto",
#                 # width_ratios=[1,shape_sci/shape_kernel],
#                 # width_ratios=[0.5,1]
#                 width_ratios=[1 / 3, 1],
#             )

#             if self.stretch.lower() == "linear":
#                 self.stretch_fn = LinearStretch
#             elif self.stretch.lower() == "square root":
#                 self.stretch_fn = SqrtStretch
#             elif self.stretch.lower() == "logarithmic":
#                 self.stretch_fn = LogStretch

#             self.plot_kernel()
#             self.plot_beam()
#             self.fig.canvas.draw_idle()

#             self.fig.canvas.get_tk_widget().grid(
#                 row=0, column=0, columnspan=2, sticky="news"
#             )
#             # self.fig.canvas.get_tk_widget().pack()
#             # print (self.fig.canvas.get_tk_widget())
#             # print (self.fig.get_size_inches())
#             # print (self.fig_axes[0].get_aspect())
#         else:
#             # if self.gal_id != self._root().current_gal_id.get() or not hasattr(
#             #     self, "pyplot_canvas"
#             # ):
#             self.gal_id = self._root().current_gal_id.get()

#             if self.stretch.lower() == "linear":
#                 self.stretch_fn = LinearStretch
#             elif self.stretch.lower() == "square root":
#                 self.stretch_fn = SqrtStretch
#             elif self.stretch.lower() == "logarithmic":
#                 self.stretch_fn = LogStretch

#             self.file_path = [
#                 *(
#                     Path(self._root().full_config["files"]["extractions_dir"])
#                     .expanduser()
#                     .resolve()
#                 ).glob(f"*{self.gal_id:0>5}.stack.fits")
#             ][0]

#             self.plot_kernel()
#             self.plot_beam()
#             self.fig.canvas.draw_idle()

#             self.fig.canvas.get_tk_widget().grid(
#                 row=0, column=0, columnspan=2, sticky="news"
#             )

#             self.update()

#     def plot_kernel(self):
#         try:
#             self.plotted_images["kernel"].remove()
#             del self.plotted_images["kernel"]
#         except:
#             pass
#         with pf.open(self.file_path) as hdul:
#             try:
#                 # print (hdul["SCI","F115W"])
#                 # print (hdul.info())
#                 data = hdul["KERNEL", self.extver].data
#                 # if hasattr(self.plotted_images, "kernel"):
#                 #     print (self.plotted_images["kernel"])
#                 #     self.plotted_images["kernel"].remove()

#                 if self.limits == "grizli default":
#                     vmax_kern = 1.1 * np.percentile(data, 99.5)
#                     interval = ManualInterval(vmin=-0.1 * vmax_kern, vmax=vmax_kern)

#                 norm = ImageNormalize(
#                     data,
#                     #  interval=MinMaxInterval(),
#                     stretch=self.stretch_fn(),
#                 )
#                 self.plotted_images["kernel"] = self.fig_axes[0].imshow(
#                     data,
#                     origin="lower",
#                     cmap=self.cmap,
#                     # aspect="auto"
#                     norm=norm,
#                 )
#                 self.fig_axes[0].set_xticklabels("")
#                 self.fig_axes[0].set_yticklabels("")
#                 self.fig_axes[0].tick_params(direction="in")
#             except Exception as e:
#                 print(e)
#                 pass

#     def plot_beam(self):
#         try:
#             self.plotted_images["beam"].remove()
#             del self.plotted_images["beam"]
#         except:
#             pass
#         with pf.open(self.file_path) as hdul:
#             try:
#                 # print (hdul["SCI","F115W"])
#                 # print (hdul.info())
#                 if self.ext == "RESIDUALS":
#                     data = hdul["SCI", self.extver].data
#                     m = hdul["MODEL", self.extver].data
#                 else:
#                     data = hdul[self.ext, self.extver].data
#                     m = 0

#                 if self.limits == "grizli default":
#                     # print ("oh boy")
#                     wht_i = hdul["WHT", self.extver]
#                     clip = wht_i.data > 0
#                     if clip.sum() == 0:
#                         clip = np.isfinite(wht_i.data)

#                     avg_rms = 1 / np.median(np.sqrt(wht_i.data[clip]))
#                     vmax = np.maximum(1.1 * np.percentile(data[clip], 98), 5 * avg_rms)
#                     vmin = -0.1 * vmax
#                     interval = ManualInterval(vmin=vmin, vmax=vmax)

#                 norm = ImageNormalize(
#                     data,
#                     interval=interval,
#                     stretch=self.stretch_fn(),
#                 )
#                 self.plotted_images["beam"] = self.fig_axes[1].imshow(
#                     data - m,
#                     origin="lower",
#                     cmap=self.cmap,
#                     aspect="auto",
#                     norm=norm,
#                 )
#                 self.fig_axes[1].tick_params(direction="in")
#                 # self.fig_axes[0].plot([1,2],[3,4])
#                 # self.update()
#                 # self.fig_axes.imshow(
#                 #     data
#                 # )
#                 # self.fig_axes[0].plot([1,2],[3,4])
#                 # self.update()
#                 # print
#             except:
#                 pass


class SinglePABeamFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        extvers,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.pad_frame = ctk.CTkFrame(self)  # , fg_color="red")
        self.pad_frame.grid(row=1, column=0, sticky="news")
        self.canvas_frame = ctk.CTkFrame(self.pad_frame)  # , fg_color="blue")
        self.canvas_frame.grid(row=0, column=0, sticky="news")
        self.canvas_frame.rowconfigure(0, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)

        self.fig = Figure(
            constrained_layout=True,
        )
        self.pyplot_canvas = FigureCanvasTkAgg(
            figure=self.fig,
            master=self.canvas_frame,
        )

        self.extvers = extvers
        widths = [1 / 3, 1] * len(self.extvers)
        self.fig_axes = self.fig.subplots(
            4,
            2 * len(self.extvers),
            sharey=True,
            width_ratios=widths,
        )

        self.quality_frame = MultiQualityFrame(self.canvas_frame, values=self.extvers)
        self.quality_frame.grid(row=1, column=0, sticky="ew")

        self.PA_plot_label = ctk.CTkLabel(self, text="Placeholder")
        self.PA_plot_label.grid(row=0, column=0, sticky="ew")

        self.set_aspect()
        self.plotted_images = dict()
        self.update_plots()

    def set_aspect(self, aspect_ratio=3):
        # a function which places a frame within a containing frame, and
        # then forces the inner frame to keep a specific aspect ratio

        def enforce_aspect_ratio(event):
            # when the pad window resizes, fit the content into it,
            # either by fixing the width or the height and then
            # adjusting the height or width based on the aspect ratio.

            other_heights = (
                self.quality_frame.winfo_height()
            )  # + self.PA_plot_label.winfo_height()
            # start by using the width as the controlling dimension
            desired_width = event.width
            desired_height = int(event.width / aspect_ratio) + other_heights

            # other_heights = 0
            # print (event.height)
            # print ("orig_desired", desired_height)
            # print ("other", other_heights)
            # if the window is too tall to fit, use the height as
            # the controlling dimension
            if desired_height > event.height:
                desired_height = event.height
                # print ("new desired", desired_height)
                desired_width = int((event.height - other_heights) * aspect_ratio)

            # place the window, giving it an explicit size
            self.canvas_frame.place(
                in_=self.pad_frame,
                x=0,
                y=0,
                relwidth=desired_width / event.width,
                relheight=desired_height / event.height,
            )

        self.pad_frame.bind("<Configure>", enforce_aspect_ratio)

    # def optionmenu_callback(choice):
    #     print("optionmenu dropdown clicked:", choice)

    def update_plots(self, extvers=None):
        
        # self.quality_frame.get()

        if extvers != None and extvers != self.extvers:
            # print ("Wrong!")
            # print (extvers)
            # print (self.extvers)
            try:
                # for old_ext in ["SCI", "CONTAM", "MODEL", "RESIDUALS"]:
                #     for old_ver in self.extvers:
                #         print (self.plotted_images[old_ext+old_ver])
                for current_key in self.plotted_images.keys():
                    for plot_name in self.plotted_images[current_key].keys():
                        self.plotted_images[current_key][plot_name].remove()
                self.plotted_images = dict()
            except:
                pass
            
            self.extvers = extvers
            self.quality_frame.reload_values(new_values=self.extvers)
        # print (self.extvers)

        # print(self.extvers)
        self.pa_var = None
        for e in self.extvers:
            try:
                self.pa_var = e.split(",")[1]
                break
            except:
                pass
        if self.pa_var is None:
            self.PA_plot_label.configure(
                text="Stack of all grism pointings (Contamination map not available)"
            )
            self.pa_var="Stack"
        else:
            self.PA_plot_label.configure(text=f"Current PA = {self.pa_var}deg")

        self.master.gal_id = self._root().current_gal_id.get()

        if self.master.stretch.lower() == "linear":
            self.stretch_fn = LinearStretch
        elif self.master.stretch.lower() == "square root":
            self.stretch_fn = SqrtStretch
        elif self.master.stretch.lower() == "logarithmic":
            self.stretch_fn = LogStretch
        for j, name in enumerate(["SCI", "CONTAM", "MODEL", "RESIDUALS"]):
            for i, ver in enumerate(self.extvers):
                if name + ver not in self.plotted_images.keys():
                    self.plotted_images[name + ver] = dict()
                self.plot_kernel(self.fig_axes[j, 2 * i], name, ver)
                # print (name)
                self.plot_beam(self.fig_axes[j, (2 * i) + 1], name, ver)
        self.fig.canvas.draw_idle()

        # self.fig.canvas.get_tk_widget().pack(fill="both", expand=1)
        # print (self.fig.canvas.get_tk_widget())
        self.fig.canvas.get_tk_widget().grid(row=0, column=0, sticky="news")

        self.update()

    def plot_kernel(self, ax, ext, extver):
        try:
            self.plotted_images[ext + extver]["kernel"].remove()
            del self.plotted_images[ext + extver]["kernel"]
        except:
            pass
        with pf.open(self.master.file_path) as hdul:
            try:
                data = hdul["KERNEL", extver].data

                if self.master.limits == "grizli default":
                    vmax_kern = 1.1 * np.percentile(data, 99.5)
                    interval = ManualInterval(vmin=-0.1 * vmax_kern, vmax=vmax_kern)
                elif self.master.limits == "Min-max":
                    interval = MinMaxInterval()
                else:
                    interval = PercentileInterval(
                        float(self.master.limits.replace("%", ""))
                    )

                norm = ImageNormalize(
                    data,
                    interval=interval,
                    stretch=self.stretch_fn(),
                )
                self.plotted_images[ext + extver]["kernel"] = ax.imshow(
                    data,
                    origin="lower",
                    cmap=self.master.cmap,
                    # aspect="auto"
                    norm=norm,
                )
                ax.set_xticklabels("")
                ax.set_yticklabels("")
                ax.tick_params(direction="in")
                if ax in self.fig_axes[:, 0]:
                    ax.set_ylabel(ext)
            except Exception as e:
                print(e)
                pass

    def plot_beam(self, ax, ext, extver):
        try:
            self.plotted_images[ext + extver]["beam"].remove()
            del self.plotted_images[ext + extver]["beam"]
        except Exception as e:
            # print ("Error here", e)
            pass
        with pf.open(self.master.file_path) as hdul:
            try:
                # print (hdul["SCI","F115W"])
                # print (hdul.info())
                if ext == "RESIDUALS":
                    data = hdul["SCI", extver].data
                    m = hdul["MODEL", extver].data
                else:
                    data = hdul[ext, extver].data
                    m = 0

                header = hdul["SCI", extver].header
                # wavelengths = ((np.arange(data.shape[1]) + 1.0) - header["CRPIX1"]) * header["CD1_1"] + header["CRVAL1"]
                # print (wavelengths)
                extent = [header["WMIN"], header["WMAX"], 0, data.shape[0]]

                if self.master.limits == "grizli default":
                    wht_i = hdul["WHT", extver]
                    clip = wht_i.data > 0
                    if clip.sum() == 0:
                        clip = np.isfinite(wht_i.data)

                    avg_rms = 1 / np.median(np.sqrt(wht_i.data[clip]))
                    vmax = np.maximum(1.1 * np.percentile(data[clip], 98), 5 * avg_rms)
                    vmin = -0.1 * vmax
                    interval = ManualInterval(vmin=vmin, vmax=vmax)
                elif self.master.limits == "Min-max":
                    interval = MinMaxInterval()
                else:
                    interval = PercentileInterval(
                        float(self.master.limits.replace("%", ""))
                    )

                norm = ImageNormalize(
                    data,
                    interval=interval,
                    stretch=self.stretch_fn(),
                )
                self.plotted_images[ext + extver]["beam"] = ax.imshow(
                    data - m,
                    origin="lower",
                    cmap=self.master.cmap,
                    aspect="auto",
                    norm=norm,
                    extent=extent,
                )
                ax.tick_params(direction="in")

                if ax not in self.fig_axes[-1]:
                    ax.set_xticklabels("")
                    ax.set_yticklabels("")
                else:
                    ax.set_xlabel(r"$\lambda$ ($\mu$m) - " + extver.split(",")[0])
            except Exception as e:
                print(e)
                pass


class MultiQualityFrame(ctk.CTkFrame):
    def __init__(self, master, values, **kwargs):

        super().__init__(master, **kwargs)
        self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.values = values
        self.contamination_menus = []
        self.coverage_menus = []

        for i, value in enumerate(self.values):
            label = ctk.CTkLabel(self, text="Beam Contamination")
            label.grid(row=0, column=2 * i, padx=10, pady=(10, 0), sticky="e")
            cont_menu = ctk.CTkOptionMenu(
                self,
                values=["None", "Mild", "Strong"],
                # command
            )
            cont_menu.grid(row=0, column=2 * i + 1, padx=10, pady=(10, 0), sticky="w")
            self.contamination_menus.append(cont_menu)

            label = ctk.CTkLabel(self, text="Beam Coverage")
            label.grid(row=1, column=2 * i, padx=10, pady=(10, 10), sticky="e")
            cov_menu = ctk.CTkOptionMenu(
                self,
                values=["Full", "Incomplete", "No data"],
            )
            cov_menu.grid(row=1, column=2 * i + 1, padx=10, pady=(10, 10), sticky="w")
            self.coverage_menus.append(cov_menu)


    def reload_values(self, new_values):

        print (new_values, self.values)


    def get(self):
        
        # self._root().current_gal_data[master.master.master.pa_var] = "test"
        print (self._root().current_gal_data)
        for v, cont, cov in zip(self.values, self.contamination_menus, self.coverage_menus):
            # print (v, cont.get(), cov.get())
            if v not in self._root().current_gal_data.keys():
                self._root().current_gal_data[v] = {}
            self._root().current_gal_data[v]["contamination"] = cont.get()
            self._root().current_gal_data[v]["coverage"] = cov.get()
        # print ([c.get() for c in self.coverage_menus])
        print (self._root().current_gal_data)
        # checked_checkboxes = []
        # for checkbox in self.checkboxes:
        #     if checkbox.get() == 1:
        #         checked_checkboxes.append(checkbox.cget("text"))
        # return checked_checkboxes

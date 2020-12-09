import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import font as tkfont
from tkinter.ttk  import *
import tkinter_app.example_plots as illum_plot
import tkinter_app.examples_tristimulus_byMCLO as calXYZ
import colour
from idlelib import sidebar
from tkinter.filedialog import askopenfilename
# import examples_temperature_plots_A_n_D as illum_plot

class APP_Test(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family = 'times', size = 18, weight = "bold")
        self.labelframe_font = tkfont.Font(family = 'times', size = 12, slant = "italic")
        self.content_font = tkfont.Font(family = 'times', size = 12)
        self.hint_font = tkfont.Font(family = 'times', size = 12, slant = "italic")
        
        self.title("ADVMCTT by Jimbo(M108660006)")
        self.geometry("360x240")
        self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ColourTemperature, Tristimulus):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = tk.Label(self, text="Menu of Choices", font=controller.title_font)
        self.title.pack(side="top", fill="x", pady=30)

        # ---------- Go To Colour Temperature ----------
        self.btn_ct_plot = tk.Button(self, text="Plot Colour Temperature", width = 20,
                                     command=lambda: controller.show_frame("ColourTemperature"))
        self.btn_ct_plot.pack()
        # ---------- Go To Tristimulus ----------
        self.btn_tristimulus = tk.Button(self, text="Calulate Tristimulus Values", width = 20,
                                    command=lambda: controller.show_frame("Tristimulus"))
        self.btn_tristimulus.pack()
        
class ColourTemperature(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # ---------- Label Frame ----------
        self.labelframe = tk.LabelFrame(self, labelanchor="nw", width = 280,
                                        font = controller.labelframe_font,
                                        text='Colour Temperature and Correlated Colour Temperature Plots')
        self.labelframe.pack(pady = 40)
        # ---------- Combo Box ----------
        self.var = StringVar()       
        self.cb = Combobox(self.labelframe,textvariable=self.var, font = controller.content_font )                # 建立Combobox
        self.cb["value"] = ("CIE 1931", "CIE 1960", "Blackbody")            # 設定選項內容
        self.cb.current(0)                                              # 設定預設選項
        self.cb.grid(row = 0, column = 0, columnspan = 2, 
                     pady = 20, padx = 10)
        # ---------- Print Button --------
        self.btn_plot = tk.Button(self.labelframe, text = "Print",
                                  command = self.__printSelection) # 建立按鈕
        self.btn_plot.grid(row = 1, column = 0, padx = 50)
        # ---------- Back Button ----------
        self.btn_back = tk.Button(self.labelframe, text="Back",
                                  command=lambda: controller.show_frame("StartPage"))
        self.btn_back.grid(row = 1, column = 1, padx = 50)
        # ---------- Bottom Space ---------- 
        self.label = tk.Label(self.labelframe)
        self.label.grid(row = 2, column = 0, columnspan = 2, pady = 5)
        
    def __printSelection(self):                               # 列印選項
        print(self.var.get())
        messageboxChoice = self.var.get()
        tkinter.messagebox.showinfo(message = self.var.get())
        
        plot1 = illum_plot.illuminamisInDiagram()
        if (messageboxChoice == "CIE 1931"):
            plot1.plot_in_chromaticity_diagram_CIE1931()
        elif (messageboxChoice == "CIE 1960"):
            plot1.plot_in_chromaticity_diagram_CIE1960()
        elif (messageboxChoice == "Blackbody"):
            plot1.plot_blackbody_colors()

class Tristimulus(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # ---------- Label Frame ----------
        self.labelframe = tk.LabelFrame(self, labelanchor="nw",
                                        font = controller.labelframe_font,
                                        text='Calulate Tristimulus Values')
        self.labelframe.pack(pady = 20, padx = 5)
       
        self.num_spec = 36#31    # setting num
        calXYZ1 = calXYZ.CalulateTristimulusValues()
        
        
        specs = [0] * self.num_spec # Create a list hold the sample's SR for test
        
        # ==================== Spectral Start ====================
        
        # ---------- Spectral Start Label ----------
        self.label_spec_start = tk.Label(self.labelframe, text = 'Input Start of Spectral :')
        self.label_spec_start.grid(row = 1, column = 0, pady = 10, sticky = E)
        
        # ---------- Spectral Start Entry ----------
        self.entry_spec_start = tk.Entry(self.labelframe, width = 5)
        self.entry_spec_start.grid(row = 1, column = 1, pady = 10, sticky = W)
        self.entry_spec_start.insert(0, '370')
        # ---------- Spectral Start Hint ----------
        self.label_spec_hint = tk.Label(self.labelframe, text = '(ex: 370)', fg = 'gray',
                                        font = controller.hint_font)
        self.label_spec_hint.grid(row = 1, column = 2, pady = 10, sticky = W)
        # ---------- Spectral Right Space ----------
        self.label_spec_space = tk.Label(self.labelframe, width = 2)
        self.label_spec_space.grid(row = 1, column = 3, pady = 10)
        
        # ==================== Interval ==================== 
        
        # ---------- Interval Label ----------
        self.label_interval = tk.Label(self.labelframe, text = 'Input Interval of Spectral :')
        self.label_interval.grid(row = 2, column = 0, sticky = E)
        
        # ---------- Interval Entry ----------
        self.entry_interval = tk.Entry(self.labelframe, width = 5)
        self.entry_interval.grid(row = 2, column = 1, sticky = W)
        self.entry_interval.insert(0, '5')
        # ---------- Interval Hint ----------
        self.label_interval_hint = tk.Label(self.labelframe, text = '(ex: 5)', fg = 'gray',
                                        font = controller.hint_font)
        self.label_interval_hint.grid(row = 2, column = 2, sticky = W)
        # ---------- Interval Right Space ----------
        self.label_interval_space = tk.Label(self.labelframe, width = 2)
        self.label_interval_space.grid(row = 2, column = 3)
        
        # ==================== File ====================
        
        # ---------- File Name ----------
        self.label_filename = tk.Label(self.labelframe, borderwidth = 2, relief = 'sunken',
                                       width = 15, text = 'colorchecker24.txt')
        self.label_filename.grid(row = 3, column = 0, pady = 10, sticky = E)
        # ---------- Ask Open File Name ----------
        self.btn_openfile = tk.Button(self.labelframe, text = "Open File",
                                      command =  self.__askOpenFileName)
        self.btn_openfile.grid(row = 3, column = 1, columnspan = 3, pady = 10, sticky = W)
        
        # ==================== Button ====================
        
        # ---------- Calulate Button --------
        self.btn_cal = tk.Button(self.labelframe, text = "Calulate",
                                 command = self.__printCalulate) # 建立按鈕
        self.btn_cal.grid(row = 4, column = 0, padx = 50)
        # ---------- Back Button ----------
        self.btn_back = tk.Button(self.labelframe, text="Back",
                                  command=lambda: controller.show_frame("StartPage"))
        self.btn_back.grid(row = 4, column = 1, columnspan = 3, padx = 50)
        # ---------- Bottom Space ---------- 
        self.label = tk.Label(self.labelframe)
        self.label.grid(row = 5, column = 0, columnspan = 4, pady = 2)
 
    def __printCalulate(self):
        print("test")
        
        
    def __askOpenFileName(self):
        filename = askopenfilename()
        label_filename = tk.Label(self.labelframe, borderwidth = 2, relief = 'sunken',
                                  width = 15, text = filename.split('/')[-1])
        label_filename.grid(row = 3, column = 0, pady = 10, sticky = E)
        
        
    
if __name__ == "__main__":
    app = APP_Test()
    app.mainloop()





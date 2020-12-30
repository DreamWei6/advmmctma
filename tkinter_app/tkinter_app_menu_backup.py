import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import font as tkfont
from tkinter.ttk  import *
import tkinter_app.example_plots as illum_plot
# import tkinter_app.examples_tristimulus_byMCLO as calXYZ

from tkinter.filedialog import askopenfilename
from colorimetry.examples_correction import sample_sd_data
# import examples_temperature_plots_A_n_D as illum_plot

class APP_Test(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family = 'times', size = 18, weight = "bold")
        self.labelframe_font = tkfont.Font(family = 'times', size = 12, slant = "italic")
        self.content_font = tkfont.Font(family = 'times', size = 12)
        self.hint_font = tkfont.Font(family = 'times', size = 12, slant = "italic")
        
        self.title("ADVMMCTMA by Jimbo(M108660006)")
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

        ''' ---------- Go To Colour Temperature ---------- '''
        self.btn_ct_plot = tk.Button(self, text="Plot Colour Temperature", width = 20,
                                     command=lambda: controller.show_frame("ColourTemperature"))
        self.btn_ct_plot.pack()
        ''' ---------- Go To Tristimulus ---------- '''
        self.btn_tristimulus = tk.Button(self, text="Calulate Tristimulus Values", width = 20,
                                    command=lambda: controller.show_frame("Tristimulus"))
        self.btn_tristimulus.pack()
        
class ColourTemperature(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ''' ---------- Label Frame ---------- '''
        self.labelframe = tk.LabelFrame(self, labelanchor="nw", width = 280,
                                        font = controller.labelframe_font,
                                        text='Colour Temperature and Correlated Colour Temperature Plots')
        self.labelframe.pack(pady = 40)
        ''' ---------- Combo Box ---------- '''
        self.var = tk.StringVar()       
        self.cb = Combobox(self.labelframe,textvariable=self.var, font = controller.content_font )                # 建立Combobox
        self.cb["value"] = ("CIE 1931", "CIE 1960", "Blackbody")            # 設定選項內容
        self.cb.current(0)                                              # 設定預設選項
        self.cb.grid(row = 0, column = 0, columnspan = 2, 
                     pady = 20, padx = 10)
        ''' ---------- Print Button -------- '''
        self.btn_plot = tk.Button(self.labelframe, text = "Print",
                                  command = self.__printSelection) # 建立按鈕
        self.btn_plot.grid(row = 1, column = 0, padx = 50)
        ''' ---------- Back Button ---------- '''
        self.btn_back = tk.Button(self.labelframe, text="Back",
                                  command=lambda: controller.show_frame("StartPage"))
        self.btn_back.grid(row = 1, column = 1, padx = 50)
        ''' ---------- Bottom Space ---------- ''' 
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
        
        self.spec = []
        ''' ---------- Label Frame ---------- '''
        self.labelframe = tk.LabelFrame(self, labelanchor="nw",
                                        font = controller.labelframe_font,
                                        text='Calculate Tristimulus Values')
        self.labelframe.pack(pady = 10, padx = 5)
       
#         calXYZ1 = calXYZ.CalulateTristimulusValues()
        
        
        ''' ==================== File ==================== '''
        
        ''' ---------- File Name ---------- '''
        self.label_filename = tk.Label(self.labelframe, borderwidth = 2, relief = 'sunken',
                                       width = 15, text = 'colorchecker24.txt')
        self.label_filename.grid(row = 1, column = 0, pady = 20, sticky = E)
        ''' ---------- Ask Open File Name ---------- '''
        self.btn_openfile = tk.Button(self.labelframe, text = "Open File",
                                      command =  self.__askOpenFileName)
        self.btn_openfile.grid(row = 1, column = 1, columnspan = 3, pady = 20, sticky = W)
        
        
        ''' ==================== Spectral Start ==================== '''
        
        var1 = tk.StringVar()
        ''' ---------- Spectral Start Label ---------- '''
        self.label_spec_start = tk.Label(self.labelframe, text = 'Input Start of Spectral :')
        self.label_spec_start.grid(row = 2, column = 0, sticky = E)
        ''' ---------- Spectral Start Entry ---------- '''
        self.entry_spec_start = tk.Entry(self.labelframe, width = 5, textvariable = var1)
        self.entry_spec_start.grid(row = 2, column = 1, sticky = W)
        self.entry_spec_start.insert(0, '370')
        ''' ---------- Spectral Start Hint ---------- '''
        self.label_spec_hint = tk.Label(self.labelframe, text = '(ex: 370)', fg = 'gray',
                                        font = controller.hint_font)
        self.label_spec_hint.grid(row = 2, column = 2, sticky = W)
        ''' ---------- Spectral Right Space ---------- '''
        self.label_spec_space = tk.Label(self.labelframe, width = 2)
        self.label_spec_space.grid(row = 2, column = 3)
        
        ''' ==================== Interval ==================== '''
         
        var2 = tk.StringVar()
        ''' ---------- Interval Label ---------- '''
        self.label_interval = tk.Label(self.labelframe, text = 'Input Interval of Spectral :')
        self.label_interval.grid(row = 3, column = 0, sticky = E, pady = 10)
        ''' ---------- Interval Entry ---------- '''
        self.entry_interval = tk.Entry(self.labelframe, width = 5, textvariable = var2)
        self.entry_interval.grid(row = 3, column = 1, sticky = W)
        self.entry_interval.insert(0, '5')
        ''' ---------- Interval Hint ---------- '''
        self.label_interval_hint = tk.Label(self.labelframe, text = '(ex: 5)', fg = 'gray',
                                        font = controller.hint_font)
        self.label_interval_hint.grid(row = 3, column = 2, sticky = W)
        ''' ---------- Interval Right Space ---------- '''
        self.label_interval_space = tk.Label(self.labelframe, width = 2)
        self.label_interval_space.grid(row = 3, column = 3)
        
        ''' ==================== Button ==================== '''
        
        ''' ---------- Calulate Button -------- '''
        self.btn_cal = tk.Button(self.labelframe, text = "Calulate",
                                 command = lambda:self.__printCalulate(var1.get(), var2.get()))
        self.btn_cal.grid(row = 4, column = 0, padx = 50, pady = 2)
        ''' ---------- Back Button ---------- '''
        self.btn_back = tk.Button(self.labelframe, text = "Back",
                                  command=lambda: controller.show_frame("StartPage"))
        self.btn_back.grid(row = 4, column = 1, columnspan = 3, padx = 50, pady = 2)
        ''' ---------- Bottom Space ----------'''
        self.label = tk.Label(self.labelframe)
        self.label.grid(row = 5, column = 0, columnspan = 4, pady = 1)
 
    def __printCalulate(self, spectral_var, interval_var):
        for index in range(len(self.specs)):
            self.specs[index] = int(spectral_var) + int(interval_var) * index
        sample_sd_data = {self.specs[i]: self.sample_sr_data[i] for i in range(len(self.sample_sr_data))}
        print(sample_sd_data)
        self.__createWindow(sample_sd_data)
        
        
    def __askOpenFileName(self):
        self.filename = askopenfilename()
        label_filename = tk.Label(self.labelframe, borderwidth = 2, relief = 'sunken',
                                  width = 15, text = self.filename.split('/')[-1])
        data = ''
        if self.filename != '':
            with open(self.filename, 'r') as f:
                data += f.read()
                
            self.sample_sr_data = data.split('\n')
            NUM_SPEC = len(data.split('\n'))
#             print(NUM_SPEC)
            self.specs = [0] * NUM_SPEC
            if '\t' in self.sample_sr_data[0]:
                for index in range(len(self.specs)):
                    self.specs[index] = int(self.sample_sr_data[index].split('\t')[0])  
                    self.sample_sr_data[index] = float(self.sample_sr_data[index].split('\t')[1])  
                self.entry_spec_start.delete(0, END)
                self.entry_spec_start.insert(0, self.specs[0])
                self.entry_spec_start["state"] = 'readonly'
                self.entry_interval.delete(0, END)
                self.entry_interval.insert(0, int(self.specs[1]) - int(self.specs[0]))
                self.entry_interval["state"] = 'readonly'
            else:
                for index in range(len(self.specs)):
                    self.sample_sr_data[index] = float(self.sample_sr_data[index])
                self.entry_spec_start["state"] = 'normal'
                self.entry_interval["state"] = 'normal'
                
#             print(self.specs)
        label_filename.grid(row = 1, column = 0, pady = 10, sticky = E)
        
    def __createWindow(self, sample_sd_data):
        self.xyz_window = tk.Toplevel(self)
        self.xyz_window.title("CIE XYZ")
        self.xyz_window.geometry("200x150")
        self.xyz_window.resizable(False, False)
        
        ''' ==================== Calculate Result ==================== '''
        top_space = Label(self.xyz_window, text = '')
        top_space.grid(row = 0, column = 0, columnspan = 3)
        
        x_label = Label(self.xyz_window, text = 'X :', anchor = E)
        x_label.grid(row = 1, column = 0, ipadx = 20, pady = 2)
        x_entry = Entry(self.xyz_window, width = 8)
        x_entry.grid(row = 1, column = 1, pady = 2, columnspan = 2)
        x_entry.insert(0, sample_sd_data)
        
        y_label = Label(self.xyz_window, text = 'Y :', anchor = E)
        y_label.grid(row = 2, column = 0, ipadx = 20, pady = 2)
        y_entry = Entry(self.xyz_window, width = 8)
        y_entry.grid(row = 2, column = 1, pady = 2, columnspan = 2)
        
        z_label = Label(self.xyz_window, text = 'Z :', anchor = E)
        z_label.grid(row = 3, column = 0, ipadx = 20, pady = 2)
        z_entry = Entry(self.xyz_window, width = 8)
        z_entry.grid(row = 3, column = 1, pady = 2, columnspan = 2)
        
        exit_btn = Button(self.xyz_window, text = 'exit', width = 3, command = self.__exit)
        exit_btn.grid(row = 4, column = 1, columnspan = 2)
         
    def __exit(self):
        self.xyz_window.destroy()
        
if __name__ == "__main__":
    app = APP_Test()
    app.mainloop()





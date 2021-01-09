import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import font as tkfont
from tkinter.ttk  import *
import tkinter_app.example_plots as illum_plot
# import tkinter_app.examples_tristimulus_byMCLO as calXYZ
import csv

from tkinter.filedialog import askopenfilename
from colorimetry.examples_correction import sample_sd_data
# import examples_temperature_plots_A_n_D as illum_plot
from colormath import color_conversions
from colormath import color_objects
from colormath.color_objects import *
from fileinput import input



class APP_Test(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family = 'times', size = 32, weight = "bold")
        self.menu_btn_font = tkfont.Font(family = 'Courier', size = 20)
        self.labelframe_font = tkfont.Font(family = 'times', size = 16, slant = "italic")
        self.content_font = tkfont.Font(family = 'times', size = 12)
        self.button_font = tkfont.Font(family = 'Courier', size = 16)
        self.label_font = tkfont.Font(family = 'Courier', size = 12)
        self.label_big_font = tkfont.Font(family = 'Courier', size = 16)
        
        self.title("ADVMMCTMA by Jimbo(M108660006)")
        self.geometry("480x360")
        self.resizable(False, False)

        
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ColourTemperature, Tristimulus, ColorSpaceCalculator):
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
        self.btn_ct_plot = tk.Button(self, text = "Plot Colour Temperature", width = 25,
                                     font = self.controller.menu_btn_font, height = 2,
                                     command=lambda: controller.show_frame("ColourTemperature"))
        self.btn_ct_plot.pack(pady = 5)
        ''' ---------- Go To Tristimulus ---------- '''
        self.btn_tristimulus = tk.Button(self, text = "Calulate Tristimulus Values", width = 25,
                                         font = self.controller.menu_btn_font, height = 2,
                                         command=lambda: controller.show_frame("Tristimulus"))
        self.btn_tristimulus.pack(pady = 5)
        ''' ---------- Go To Color Space Calculator ---------- '''
        self.btn_cs_cal = tk.Button(self, text = "Color Space Calculator", width = 25,
                                         font = self.controller.menu_btn_font, height = 2,
                                         command=lambda: controller.show_frame("ColorSpaceCalculator"))
        self.btn_cs_cal.pack(pady = 5)
        
class ColourTemperature(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ''' ---------- Label Frame ---------- '''
        self.labelframe = tk.LabelFrame(self, labelanchor="nw",
                                        font = controller.labelframe_font,
                                        text='Colour Temperature and Correlated Colour Temperature Plots')
        self.labelframe.pack(pady = 80)
        ''' ---------- Combo Box ---------- '''
        self.var = tk.StringVar()       
        self.cb = Combobox(self.labelframe,textvariable=self.var, font = controller.menu_btn_font )                # 建立Combobox
        self.cb["value"] = ("CIE 1931", "CIE 1960", "Blackbody")            # 設定選項內容
        self.cb.current(0)                                              # 設定預設選項
        self.cb.grid(row = 0, column = 0, columnspan = 2, 
                     pady = 30, padx = 60)
        ''' ---------- Print Button -------- '''
        self.btn_plot = tk.Button(self.labelframe, text = "Print", font = controller.button_font,
                                  command = self.__printSelection, width = 6, height = 2) # 建立按鈕
        self.btn_plot.grid(row = 1, column = 0, padx = 50)
        ''' ---------- Back Button ---------- '''
        self.btn_back = tk.Button(self.labelframe, text="Back", font = controller.button_font,
                                  command=lambda: controller.show_frame("StartPage"), width = 6, height = 2)
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
        self.labelframe.pack(pady = 10, padx = 10, ipady = 20, ipadx = 8)
       
#         calXYZ1 = calXYZ.CalulateTristimulusValues()
        
        
        ''' ==================== File ==================== '''
        
        ''' ---------- File Name ---------- '''
        self.label_filename = tk.Label(self.labelframe, borderwidth = 2, relief = 'sunken',
                                       font = controller.label_big_font, height = 2,
                                       width = 16, text = 'CC_NO1.csv')
        self.label_filename.grid(row = 1, column = 0, columnspan = 3, pady = 20, sticky = E)
        ''' ---------- Ask Open File Name ---------- '''
        self.btn_openfile = tk.Button(self.labelframe, text = "Open File", font = controller.button_font,
                                      command =  self.__askOpenFileName, width = 8, height = 2)
        self.btn_openfile.grid(row = 1, column = 3, pady = 20, sticky = W)
        
        ''' ==================== Spectral Info ===================='''
        self.spec_labelframe = tk.LabelFrame(self.labelframe, labelanchor = 'n',
                                             font = controller.labelframe_font,
                                             text='Spectral Infomation') 
        self.spec_labelframe.grid(row = 2, column = 0, columnspan = 2, ipadx = 8, ipady = 3, pady = 20)
        ''' -------------------- Spectral Range --------------------'''
         
        self.var1 = tk.StringVar()
        ''' ---------- Spectral Start Label ---------- '''
        self.label_spec_range = tk.Label(self.spec_labelframe, text = f' {"Range" : <8} :', font = self.controller.label_font)
        self.label_spec_range.grid(row = 0, column = 0, padx = 4)
        ''' ---------- Spectral Start Entry ---------- '''
        self.entry_spec_range = tk.Entry(self.spec_labelframe, width = 8, textvariable = self.var1, font = self.controller.label_font)
        self.entry_spec_range.grid(row = 0, column = 1)
        self.entry_spec_range['state'] = 'readonly'
          
        ''' ==================== Interval ==================== '''
          
        self.var2 = tk.StringVar()
        ''' ---------- Interval Label ---------- '''
        self.label_interval = tk.Label(self.spec_labelframe, text = f' {"Interval" : <8} :', font = self.controller.label_font)
        self.label_interval.grid(row = 1, column = 0, padx = 4)
        ''' ---------- Interval Entry ---------- '''
        self.entry_interval = tk.Entry(self.spec_labelframe, width = 8, textvariable = self.var2, font = self.controller.label_font)
        self.entry_interval.grid(row = 1, column = 1)
        self.entry_interval['state'] = 'readonly'

        ''' ==================== Number Of Set ==================== '''
        
        self.var3 = tk.StringVar()
        ''' ---------- Number Label ---------- '''
        self.label_number =  tk.Label(self.spec_labelframe, text = f' {"Number" : <8} :', font = self.controller.label_font)
        self.label_number.grid(row = 2, column = 0, padx = 4)
        ''' ---------- Number Entry ---------- '''
        self.entry_number = tk.Entry(self.spec_labelframe, width = 8, textvariable = self.var3, font = self.controller.label_font)
        self.entry_number.grid(row = 2, column = 1)
        self.entry_number['state'] = 'readonly'
        
        ''' ==================== Parameter Setting ===================='''
        self.param_labelframe = tk.LabelFrame(self.labelframe, labelanchor = 'n',
                                             font = controller.labelframe_font,
                                             text='Spectral Infomation') 
        self.param_labelframe.grid(row = 2, column = 2, columnspan = 2, ipadx = 8, ipady = 3)
        ''' ---------- Illuminant Label ---------- '''
        self.illuminant_label =  tk.Label(self.param_labelframe, text = f'  {"Illuminant" : <10} :', font = self.controller.label_font, anchor = 'e')
        self.illuminant_label.grid(row = 0, column = 0)
        
        ''' ---------- Illuminant Combo Box ---------- '''
        self.illuminant_cb = Combobox(self.param_labelframe, 
                                      font = controller.label_font, width = 8, state = 'normal')
        self.illuminant_cb["values"] = ("D50", "D65")
        self.illuminant_cb.current(0)
        self.illuminant_cb['state'] = 'readonly'
        self.illuminant_cb.grid(row = 0, column = 1) 
        
        ''' ---------- Observer Label ---------- '''
        self.observer_label =  tk.Label(self.param_labelframe, text = f'  {"Observer" : <10} :', font = self.controller.label_font, anchor = 'e')
        self.observer_label.grid(row = 1, column = 0)
        ''' ---------- Observer RadioButton ---------- '''
        self.degree_select = tk.StringVar()
        self.select2degree = tk.Radiobutton(self.param_labelframe, text = f'{"2-degree":<10}', font = self.controller.label_font,   
                                       variable = self.degree_select, value = '2')
        self.select2degree.grid(row = 1, column = 1)
        self.select10degree = tk.Radiobutton(self.param_labelframe, text = f'{"10-degree":<10}', font = self.controller.label_font, 
                                       variable = self.degree_select, value = '10')
        self.select10degree.grid(row = 2, column = 1)
        self.degree_select.set('2')
        
        ''' ==================== Button ==================== '''
        
        ''' ---------- Calulate Button -------- '''
        self.btn_cal = tk.Button(self.labelframe, text = "Calculate", font = controller.button_font,
                                 command = lambda:self.__loadData(), 
                                 width = 8, height = 2)
        self.btn_cal.grid(row = 4, column = 0, columnspan = 2, padx = 50, pady = 2)
        ''' ---------- Back Button ---------- '''
        self.btn_back = tk.Button(self.labelframe, text = "Back", font = controller.button_font,
                                  command=lambda: controller.show_frame("StartPage"),
                                  width = 6, height = 2)
        self.btn_back.grid(row = 4, column = 2, columnspan = 2, padx = 50, pady = 2)
        ''' ---------- Bottom Space ----------'''
        self.label = tk.Label(self.labelframe)
        self.label.grid(row = 5, column = 0, columnspan = 4, pady = 1)
        
 
    def __loadData(self):
        '''
        for index in range(len(self.specs)):
            self.specs[index] = int(spectral_var) + int(interval_var) * index
        sample_sd_data = {self.specs[i]: self.sample_sr_data[i] for i in range(len(self.sample_sr_data))}
        print(sample_sd_data)
        self.__createWindow(sample_sd_data)
        '''
        source = [int(x) for x in range(340, 840) if x % 10 == 0]
        self.sample_sd_data_list = []
        for i in range(int(self.var3.get())):
            self.sample_sd_data_list.append([])
        j = 0
        for d in self.data:
            if  int(d[0]) % 10 == 0:
                for s in range(j, len(source)):
                    if source[s] == int(d[0]):
                        for a in range(len(self.sample_sd_data_list)):
                            self.sample_sd_data_list[a].append(float(d[1].split(',')[a]))
                        j = s + 1
                        break
                    else:
                        for a in range(len(self.sample_sd_data_list)):
                            self.sample_sd_data_list[a].append(0)
        print(len(source), len(self.sample_sd_data_list[0]))
        for i in range(len(source) - len(self.sample_sd_data_list[0])):
            for a in range(len(self.sample_sd_data_list)):
                self.sample_sd_data_list[a].append(0)
        print(len(source), len(self.sample_sd_data_list[0]))
        print(self.sample_sd_data_list)
        
        if self.entry_spec_range.get() and self.entry_interval.get() and self.entry_number.get() and self.illuminant_cb.get() and self.degree_select.get():
            print(self.degree_select.get(), self.illuminant_cb.get().lower())
        else:
            messagebox.showwarning(title = 'Value Error', message = 'Confirm whether you choose a file')
        self.__createWindow(self.sample_sd_data_list)
        
        
    def __askOpenFileName(self):
        self.filename = askopenfilename()
        
        self.label_filename["text"] = self.filename.split('/')[-1]
        file_type = self.filename.split('.')[-1]
        self.data = []
        if self.filename != '':
            if file_type == 'txt':
                print('txt')
                try:
                    with open(self.filename, 'r', encoding = 'utf-16', errors = 'ignore') as f:
                        rows = f.readlines()
                except UnicodeError:
                    with open(self.filename, 'r', encoding = 'utf-8', errors = 'ignore') as f:
                        rows = f.readlines()
                for row in rows:
                    row_split = row.split('\t')
                    d = [row_split[0]]
                    d.append(','.join(str(row_split[i]) for i in range(1, len(row_split))))
                    self.data.append(d)
                    print(d)
            elif file_type == 'csv':
                print('csv')
                with open(self.filename, newline='') as csvfile:
                    rows = csv.reader(csvfile)
                    for row in rows:
                        d = [row[0]]
                        d.append(','.join(str(row[i]) for i in range(1, len(row))))
                        #print(d)
                        self.data.append(d)
        
        self.spec_range = self.data[0][0] + '~' + self.data[-1][0]
        self.entry_spec_range["state"] = "normal"
        self.entry_spec_range.delete(0, END)
        self.entry_spec_range.insert(0, self.spec_range)
        self.entry_spec_range["state"] = "readonly"
        
        self.spec_interval = int(self.data[1][0]) - int(self.data[0][0])
        self.entry_interval["state"] = "normal"
        self.entry_interval.delete(0, END)
        self.entry_interval.insert(0, self.spec_interval)
        self.entry_interval["state"] = "readonly"
        
        self.spec_number = len(self.data[0][1].split(','))
        self.entry_number["state"] = "normal"
        self.entry_number.delete(0, END)
        self.entry_number.insert(0, self.spec_number)
        self.entry_number["state"] = "readonly"

        
    def __createWindow(self, sample_sd_data_list):
        self.page_index = 0
        xyz = self.__calculate(sample_sd_data_list[self.page_index])
        
        self.xyz_window = tk.Toplevel(self)
        self.xyz_window.title("CIE XYZ")
        self.xyz_window.geometry("250x150")
        self.xyz_window.resizable(False, False)
        
        ''' ==================== Calculate Result ==================== '''
        self.xyz_combobox = Combobox(self.xyz_window, width = 3, state = 'readonly', 
                                     values = [str(i) for i in range(1, int(self.var3.get()) + 1)]) 
        self.xyz_combobox.current(0)
        self.xyz_combobox.bind('<<ComboboxSelected>>', self.__changeByIndex)
        self.xyz_combobox.grid(row = 0, column = 1, sticky = W)
            
        self.top_content = Label(self.xyz_window, text = '/ ' + self.var3.get())
        self.top_content.grid(row = 0, column = 1, sticky = E)
        
        self.x_label = Label(self.xyz_window, text = 'X :', anchor = E)
        self.x_label.grid(row = 1, column = 0, ipadx = 35, pady = 2)
        self.x_entry = Entry(self.xyz_window, width = 8, font = self.controller.label_font)
        self.x_entry.grid(row = 1, column = 1, pady = 2, columnspan = 2, sticky = W)
        self.x_entry["state"] = "normal"
        self.x_entry.insert(0, xyz[0].strip("x:"))
        self.x_entry["state"] = "readonly"
        
        self.y_label = Label(self.xyz_window, text = 'Y :', anchor = E)
        self.y_label.grid(row = 2, column = 0, ipadx = 35, pady = 2)
        self.y_entry = Entry(self.xyz_window, width = 8, font = self.controller.label_font)
        self.y_entry.grid(row = 2, column = 1, pady = 2, columnspan = 2, sticky = W)
        self.y_entry["state"] = "normal"
        self.y_entry.insert(0, xyz[1].strip("y:"))
        self.y_entry["state"] = "readonly"
        
        self.z_label = Label(self.xyz_window, text = 'Z :', anchor = E)
        self.z_label.grid(row = 3, column = 0, ipadx = 35, pady = 2)
        self.z_entry = Entry(self.xyz_window, width = 8, font = self.controller.label_font)
        self.z_entry.grid(row = 3, column = 1, pady = 2, columnspan = 2, sticky = W)
        self.z_entry["state"] = "normal"
        self.z_entry.insert(0, xyz[2].strip("z:"))
        self.z_entry["state"] = "readonly"
        
        self.prev_btn = Button(self.xyz_window, text = 'prev', width = 3, command = lambda: self.__changeByBtn('p'))
        self.prev_btn.grid(row = 4, column = 0, padx = 4)
        self.exit_btn = Button(self.xyz_window, text = 'exit', width = 3, command = self.__exit)
        self.exit_btn.grid(row = 4, column = 1, padx = 4)
        self.next_btn = Button(self.xyz_window, text = 'next', width = 3, command = lambda: self.__changeByBtn('n'))
        self.next_btn.grid(row = 4, column = 2, padx = 3)
        self.prev_btn.grid_forget()
        if str(self.page_index + 1) == self.var3.get():
            self.next_btn.grid_forget() 
         
    def __calculate(self, sample_sd_data):
        spectral = color_objects.SpectralColor(*sample_sd_data, 
                                               observer=self.degree_select.get(), 
                                               illuminant=self.illuminant_cb.get().lower())
        xyz = color_conversions.convert_color(spectral, XYZColor)
        myxyz = str(xyz).strip(")").replace(' ','').split("xyz_")[1:]
#         print(xyz)
        rgb = color_conversions.convert_color(xyz, sRGBColor)
        print(rgb)
        return myxyz
    
    def __changeByIndex(self, event):
        self.page_index = int(self.xyz_combobox.get()) - 1
        
        if self.page_index == 0:
            self.prev_btn.grid_forget()
        else :
            self.prev_btn.grid(row = 4, column = 0, padx = 4)
            
        if str(self.page_index + 1) == self.var3.get():
            self.next_btn.grid_forget()
        else :
            self.next_btn.grid(row = 4, column = 2, padx = 4)
            
        sample_sd_data = self.sample_sd_data_list[self.page_index]
        xyz = self.__calculate(sample_sd_data)
        self.x_entry["state"] = "normal"
        self.x_entry.delete(0, END)
        self.x_entry.insert(0, xyz[0].strip("x:"))
        self.x_entry["state"] = "readonly"
        
        self.y_entry["state"] = "normal"
        self.y_entry.delete(0, END)
        self.y_entry.insert(0, xyz[1].strip("y:"))
        self.y_entry["state"] = "readonly"
        
        self.z_entry["state"] = "normal"
        self.z_entry.delete(0, END)
        self.z_entry.insert(0, xyz[2].strip("z:"))
        self.z_entry["state"] = "readonly"
        
    def __changeByBtn(self, state):
        
        if state == 'p':
            self.page_index -= 1
        elif state == 'n':
            self.page_index += 1

        self.xyz_combobox.current(self.page_index)
        
        if self.page_index == 0:
            self.prev_btn.grid_forget()
        else :
            self.prev_btn.grid(row = 4, column = 0, padx = 4)
            
        if str(self.page_index + 1) == self.var3.get():
            self.next_btn.grid_forget()
        else :
            self.next_btn.grid(row = 4, column = 2, padx = 4)
            
        sample_sd_data = self.sample_sd_data_list[self.page_index]
        xyz = self.__calculate(sample_sd_data)
        self.x_entry["state"] = "normal"
        self.x_entry.delete(0, END)
        self.x_entry.insert(0, xyz[0].strip("x:"))
        self.x_entry["state"] = "readonly"
        
        self.y_entry["state"] = "normal"
        self.y_entry.delete(0, END)
        self.y_entry.insert(0, xyz[1].strip("y:"))
        self.y_entry["state"] = "readonly"
        
        self.z_entry["state"] = "normal"
        self.z_entry.delete(0, END)
        self.z_entry.insert(0, xyz[2].strip("z:"))
        self.z_entry["state"] = "readonly"
    
    def __exit(self):
        self.xyz_window.destroy()

        
if __name__ == "__main__":
    app = APP_Test()
    app.mainloop()





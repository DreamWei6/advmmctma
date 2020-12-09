import tkinter as tk
import tkinter.messagebox
from tkinter import *
from tkinter import font as tkfont
from tkinter.ttk  import *
import tkinter_app.example_plots as illum_plot
import tkinter_app.examples_tristimulus_byMCLO as calXYZ
import colour
# import examples_temperature_plots_A_n_D as illum_plot

class APP_Test:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("menu of choices")                                # 視窗標題
        self.root.geometry("400x480")    
        
        # ---------- Label Frame Plots ----------
        self.lf_plots = tkinter.LabelFrame(self.root, font=('times',12), labelanchor="nw", width = 300,
                                           text='Colour Temperature and Correlated Colour Temperature Plots')
        self.lf_plots.pack(pady = 20)
        
        self.var = StringVar()       
        self.cb = Combobox(self.lf_plots,textvariable=self.var, font=('times'))                # 建立Combobox
        self.cb["value"] = ("CIE 1931", "CIE 1960", "Blackbody")            # 設定選項內容
        self.cb.current(0)                                              # 設定預設選項
        self.cb.pack(pady = 10, padx = 10)
        
        self.btn = tkinter.Button(self.lf_plots,text="Print",command=self.__printSelection) # 建立按鈕
        self.btn.pack(pady=10,anchor=S,side=BOTTOM)
        # ---------- End Label Frame Plots ----------
        
        # ---------- Label Frame ----------
        self.lf_cal = tkinter.LabelFrame(self.root,font=('times',12), width = 300,
                                           text='Calulate Tristimulus Values')
        self.lf_cal.pack(pady = 20)
       
        self.num_spec = 36#31    # setting num
        
        
        self.btn2 = tkinter.Button(self.lf_cal,text="Calulate",command=self.__printSelection) # 建立按鈕
        self.btn2.pack(pady=10,anchor=S,side=BOTTOM)
 
        
        # ---------- End Label Frame ----------
        
         
        self.root.mainloop()

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
    
    
if __name__ == "__main__":
    app = APP_Test()





# ch13_9.py
import tkinter 
from tkinter import *
from tkinter.ttk  import *
import tkinter_app.example_plots as illum_plot

    
class APP_Test:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("menu of choices")                                # 視窗標題
        self.root.geometry("300x120")                    
        
        self.var = StringVar()       
        self.cb = Combobox(self.root,textvariable=self.var)                # 建立Combobox
        self.cb["value"] = ("Python","Java","C#","C")            # 設定選項內容
        self.cb.current(0)                                       # 設定預設選項
        self.cb.pack(pady=10)
        
        btn = Button(self.root,text="Print",command=self.__printSelection) # 建立按鈕
        btn.pack(pady=10,anchor=S,side=BOTTOM)
        
        self.root.mainloop()


    def __printSelection(self):                               # 列印選項
        print(self.var.get())

if __name__ == "__main__":
    app_test = APP_Test()






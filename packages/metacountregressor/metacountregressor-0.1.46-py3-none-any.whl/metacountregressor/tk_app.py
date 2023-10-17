import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
import sys, argparse
import pandas as pd
import os
import webbrowser
from pathlib import Path
import numpy as np
import re
from string import ascii_lowercase


def convert_df_columns_to_binary_and_wide(df, exclude_column):
    columns = list(df.columns)
    columns.remove('ID')
    columns_to_convert = [col for col in columns if col != exclude_column]
    df = pd.get_dummies(df, columns=columns_to_convert, drop_first=True)
    print(df)
    return df

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class App(object):
    def __init__(self):
        self.algorithm = 'select decisions'
        self.is_multi = 0
        self.y = 'FSI'
        self.normal_pars = list()
        self.random_pars = list()
        self.random_pars_dist = list()
        self.count = 0
        self.data = 'n'
        self.model = 'simulated annealing'
        self.zi_variables = list()
        self.betas = None
        self.max_iteration_limit  = 2000
        self.max_time_limit = 2000
        self.population_size = 25
        self.test_set_size = 0.2
        self.specify = None
        self.x_data = None
        self.all_data = None
        self.offset = None
        self.swap_sa = 0.2
        self.step_sa = 20
        self.forced_variables = list()
        self.complexity_level = 3
      
        self.CR_R = 0.3
        self.ADJ_INDX =1
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        try:
            from tkdesigner.designer import Designer
        except ModuleNotFoundError:
            raise RuntimeError("Couldn't add tkdesigner to the PATH.")
        # Path to asset files for this GUI window.
        ASSETS_PATH = Path(__file__).resolve().parent / "assets"
        # Required in order to add data files to Windows executable
        path = getattr(sys, '_MEIPASS', os.getcwd())
        os.chdir(path)
        global output_path
        output_path = "C:/Users/n9471103/.vscode/code_files/HS_BIC/Ex-16-3variables.csv"
        output_path = 'C:/Users/n9471103/source/repos/HS_BIC/Ex-16-3variables.csv'
        self.output_path1 = output_path
        
        print(output_path)
        shift_y = 35
        def show_data(click):
            self.y = self.all_data[click]
            print(self.y)
            
        
        def select_show(event):
            event.widget.show()
            print(event.widget.get)
            selection = event.widget.curselection()
            print(selection)
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                print('You selected item %d: "%s"' % (index, data))
                self.normal_pars.append(data)
                idx = event.widget.get(0, tk.END).index(data)
            else:
                print("")
        def select_show2(event):
            selection = event.widget.curselection()
            #print(selection)
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                self.random_pars.append(data)
            else:
                print("")
        def select_show3(event):
            selection = event.widget.curselection()
            print(selection)
            if selection:
                index = selection[0]
                data = event.widget.get(index)
                self.random_pars_dist.append(data)
        def show(click):
            if self.algorithm == 'select decisions':
                if click != 'select decisions':
                    size_alg_entry.place(x=490.0, y=137 + 25 - 81+shift_y, width=321.0, height=yaxish)
                    size_alg_entry.focus()
                    iterations_entry.place(x=490.0, y=137 + 25+shift_y, width=321.0, height=yaxish)
                    max_time_entry.place(x=490.0, y=218 + 25+shift_y, width=321.0, height=yaxish)
            self.algorithm =click
            #clears text
            size_alg_entry.delete(0, tk.END)
            iterations_entry.delete(0, tk.END)
            max_time_entry.delete(0, tk.END)
            if self.algorithm == 'harmony search':
                
                size_alg_entry.insert(0, '50')
                iterations_entry.insert(0, '10000')
                max_time_entry.insert(0, '3600')
                canvas.itemconfig(txt_enter1, text = 'Enter Hamony Memory Size')
                canvas.itemconfig(txt_enter2, text='Enter Number of Iterations')
                canvas.itemconfig(txt_enter3, text='Maximum Runtime')
            elif self.algorithm == 'simulated annealing':
                size_alg_entry.insert(0, '25')
                iterations_entry.insert(0, '10000')
                max_time_entry.insert(0, '3600')
                canvas.itemconfig(txt_enter1, text='Enter Number of Initial Solutions')
                canvas.itemconfig(txt_enter2, text='Enter Number of Iterations')
                canvas.itemconfig(txt_enter3, text='Maximum Runtime')
            elif self.algorithm == 'differential evolution':
                size_alg_entry.insert(0, '50')
                iterations_entry.insert(0, '10000')
                max_time_entry.insert(0, '3600')
                canvas.itemconfig(txt_enter1, text='Enter Populaion Size')
                canvas.itemconfig(txt_enter2, text='Enter Number of Iterations')
                canvas.itemconfig(txt_enter3, text='Maximum Runtime')
            elif self.algorithm == 'select decisions':
                canvas.itemconfig(txt_enter1, text='')
                canvas.itemconfig(txt_enter2, text='')
                canvas.itemconfig(txt_enter3, text='')
                size_alg_entry.place_forget()
                iterations_entry.place_forget()
                max_time_entry.place_forget()
                
        
        def show_wide(click):
            if click == 'binary_wide':
                self.is_wide = 1
            else:
                self.is_wide = 0    
            print('change this later')
        
        
        def show_2(click):
            print('click is', click)
            if click == 'single':
                self.is_multi =0
                print('no multi')
            else:
                print('yes multi')
                self.is_multi = 1
                
                root = tk.Tk()
                root.title('Test Set Percentage')
                root.geometry('500x300') 
 
                l = tk.Label(root, bg='white', fg='black', width=20, text='empty')
                l.pack()
 
                def print_selection(v):
                    l.config(text='you have selected ' + v)
                    self.test_set_size = float(v)

                s = tk.Scale(root, label='Enter the size of your test set', from_=0, to=1, orient=tk.HORIZONTAL, length=200, showvalue=0,tickinterval=2, resolution=0.01, command=print_selection)
                s.pack()
        def show_3(click):
            if click == 'fixed':
                self.complexity_level = 2
            elif click == 'random parameters':
                self.complexity_level = 3
            else:
                self.complexity_level = 4                 
                
            
        
        def btn_clicked_sa():
            if self.specify is not None:
                def close_and_destroy():
                    self.y = choicesn.get()
                    window.destroy()
                    window.quit()
                
                def define_offset():
                    tkinter.messagebox.showinfo('how to use', 'Select the variables to use within the offset and attach appropriate coeffients and expresions around it ie ("/" and "*") note the whole expression will be logged afterwards to create the offset')
                    window2 = tk.Tk()
                  
                    def send_to_display(text):
                        
                        disp_calcul.insert(0, text)
                        
                        print(1)    
                    def send_to_display2():
                        if len(disp_calcul.get()) == 0:
                            disp_calcul.insert(0, lstbox.get(lstbox.curselection()))
                        else:
                            disp_calcul.insert(len(disp_calcul.get()), "*"+lstbox.get(lstbox.curselection()))
                            
                    def done_d():
                        a = [i for i in ascii_lowercase]
                        var = {}
                        a = disp_calcul.get()
                        b = re.findall(r"(\b\w*[\.]?\w+\b|[\(\)\+\*\-\/])", a)
                        c = ""
                        
                        
                        
                        for ii, i in enumerate(b):
                            if i not in ["*", "/", "+", "-"]:
                                if re.match(r'^-?\d+(?:\.\d+)$', i) is None:
                                    print(i, 'and ', ii)
                                    if isfloat(i):
                                        var[str(ii)] = i
                                        c += str(i)
                                    else:    
                                        var[i] = self.x_data[i]
                                        c += str(i)
                                else:
                                    var[str(ii)] = i
                                    c += str(i)
                            else:
                                c += i 
                                
  
   
                        
                        formula = c
                        offset = eval(formula, var)
                        print(offset)  
                        self.offset = np.log(offset)      
                        window2.destroy()
                        window2.quit()
                        
                        

                            
                    
                    disp_calcul = tk.Entry(window2, readonlybackground="yellow")
                    
                    
                    tk.Label(window2, text = 'Offset Expression',  bg="#3A7FF6", fg="white", font = ("Georgia")).grid(column = 0, row = 0, sticky='nesw')
                    disp_calcul.grid(column=0, row=1, columnspan=5, sticky='nesw')
                    lab1 = tk.Label(window2, text = 'Enter Coefficients for the Expression',  bg="#3A7FF6", fg="white", font = ("Georgia"))
                    lab1.grid(column=0, row =2, sticky='nesw')
                    coeff_entry = tk.Entry(window2)
                    coeff_entry.grid(column = 0, row = 3, sticky='nesw')
                    send_to_btn = tk.Button(window2, font = ("Georgia"), text = 'Add', command=lambda:send_to_display(coeff_entry.get()))
                    send_to_btn.grid(column = 1, row = 3, sticky='nesw')
                    
                    
                    lab = tk.Label(window2, text = 'select variable/s for offset expression',  bg="#3A7FF6", fg="white", font = ("Georgia"))
                    option_mdl = tk.StringVar(window2)
                    option_mdl.set(data)
                    
                    
                    lstbox = tk.Listbox(window2, listvariable=option_mdl, selectmode=tk.SINGLE)
                    lstbox.grid(column=5, row =2, sticky='nesw')
                    send_to_btn2 = tk.Button(window2, font = ("Georgia"), text = 'Use', command=send_to_display2)
                    send_to_btn2.grid(column=5, row =3, sticky='nesw')
                    
                    
                    lstboxy.grid(column=5, row=1, sticky='nesw')
                    lab.grid(column=5, row =0, sticky='nesw')
                    done = tk.Button(window2, text = 'Done', command = done_d, font = ("Georgia"))
                    done.grid(column=3, row = 5, sticky='nesw')
                    window2.mainloop()
                    
                    
                def delete_item(case):
                    def option_changed():
                        #self.random_pars_dist = values_contaner
                        for val in values_contaner:
                            i = val.get()
                            self.random_pars_dist.append(i)
                            print('the val is ', i)
                        window2.destroy()
                    if case == 'normal':
                        selected_item = lstbox.curselection()
                        for item in selected_item[::-1]:
                            lstbox.delete(item)
                            print(self.normal_pars)
                            self.normal_pars.insert(0, data[item])
                    elif case == 'random':
                        selected_item = rdm_bix.curselection()
                        window2 = tk.Tk()
                        values_contaner = []
                        for i, item in enumerate(selected_item[::-1]):
                            rdm_bix.delete(item)
                            option_rdm_tr = ['normal', 'lindley', 'triangular', 'uniform']
                            self.random_pars.append(data[selected_item[i]])
                            values = tk.StringVar(window2)
                            values.set(option_rdm_tr[0])
                            values_contaner.append(values)
                            tk.Label(window2,  bg="#3A7FF6", fg="white", font = ("Georgia"), text='select the distribution for '+str(data[selected_item[i]])).grid(column=0, row=i, sticky='nesw')
                            rdm_tran_box = tk.OptionMenu(window2, values, *option_rdm_tr)
                            rdm_tran_box.grid(row=i, column=1, sticky='nesw')
                            button = tk.Button(window2, font = ("Georgia"), text='select', width=5, height=1,
                                               command=option_changed)
                            button.grid(row=len(option_rdm_tr) + 1, column=1, sticky='nesw')
                    elif case == 'forced':    
                        selected_item = listboxnew.curselection()
                        for item in selected_item[::-1]:
                            listboxnew.delete(item)
                            print(self.forced_variables)
                            self.forced_variables.insert(0, data[item])
                        
                    
                    
                    elif case == 'model':
                        selected_item = mdl_box.get(mdl_box.curselection())
                        print(selected_item)
                        self.model = selected_item
                    else:
                        selected_item = case.curselection()
                        print(selected_item)
                        for item in selected_item[::-1]:
                            #.delete(item)
                            print(item)
                            self.random_pars_dist.append(item)
                df = pd.read_csv(output_path)
                self.x_data =df
                data = list(df.columns)
                print(data)
                lisst = window.grid_slaves()
                for l in lisst:
                    l.destroy()
                lisst = window.place_slaves()
                for l in lisst:
                    l.destroy()
                #canvas.pack_forget()
                values = tk.StringVar()
                values.set(data)
                choicesn = tk.StringVar(window)
                option_chcn = data
                choicesn.set(data[0])
                tk.Label(window, text='Choose the prediction',  bg="#3A7FF6", fg="white", font = ("Georgia")).grid(row=0, column=0, sticky='nesw')
                lstboxy = tk.OptionMenu(window, choicesn, *option_chcn, command = show_data)
                lstboxy.grid(column=0, row=1, sticky='nesw')
                tk.Label(window, text = 'Choose the predictors',  bg="#3A7FF6", fg="white", font = ("Georgia")).grid(row = 0, column = 1,  sticky='nesw')
                lstbox = tk.Listbox(window, listvariable=values, selectmode=tk.MULTIPLE)
                lstbox.grid(column=1, row=1, sticky='nesw')
                # Create a button to remove the selected items in the list
                tk.Button(window, text="Select",   font = ("Georgia"), command= lambda:delete_item('normal')).grid(column=1, row = 2, sticky='nesw')
                option_rdm = tk.StringVar(window)
                option_rdm.set(data)
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Choose the random predictors').grid(row = 0, column = 2,  sticky='nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Choose the zero inflated terms').grid(row = 0, column = 3,  sticky='nesw')
                rdm_bix = tk.Listbox(window, listvariable=option_rdm, selectmode=tk.MULTIPLE)
                #rdm_bix.bind('<<ListboxSelect>>', select_show2)
                rdm_bix.grid(row =1, column =2, sticky='nesw')
                tk.Button(window, text="Select", font = ("Georgia"), command=lambda:delete_item('random')).grid(column=2, row=2, sticky='nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Choose the model').grid(row=0, column =4, sticky='nesw')
                option_mdl = tk.StringVar(window)
                option_mdl.set(['Poisson', 'NB', 'COMP'])
                mdl_box = tk.Listbox(window, listvariable = option_mdl, selectmode=tk.SINGLE)
                mdl_box.grid(row = 1, column =4, sticky='nesw')
                tk.Button(window, text="Select",  font = ("Georgia"), command=lambda: delete_item('model')).grid(column=4, row=2,  sticky='nesw')
               
                tk.Label(window, text = 'Define the offset',  bg="#3A7FF6", fg="white", font = ("Georgia")).grid(row=0, column =5, sticky='nesw')
                Define_Offset_Btn = tk.Button(window, text='Define Offset',  bg="#3A7FF6", fg="white", font = ("Georgia"), command = define_offset).grid(row =1, column = 5, sticky = 'nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Select the variables to force into the model').grid(row=3, column =3, sticky='nesw')
                expVals = tk.StringVar(window)
                expVals.set(data)
                newchoices = data #TODO what does this do
                
                listboxnew = tk.Listbox(window, listvariable=expVals, selectmode=tk.MULTIPLE)
                listboxnew.grid(column = 3, row = 4, sticky = 'nesw')
                tk.Button(window, text="Select",   font = ("Georgia"), command= lambda:delete_item('forced')).grid(column=3, row = 5, sticky='nesw')
                
                
                
                tk.Button(window, text="Run",   font = ("Georgia"), command=close_and_destroy).grid(column=7, row=1,  sticky='nesw')
            else:
                def close_and_destroy():
                    self.y = choicesn.get()
                    window.destroy()
                    window.quit()
                
                def define_offset():
                    tk.messagebox.showinfo('how to use', 'Select the variables to use within the offset and attach appropriate coeffients and expresions around it ie ("/" and "*") note the whole expression will be logged afterwards to create the offset')
                    window2 = tk.Tk()
                  
                    def send_to_display(text):
                        
                        disp_calcul.insert(0, text)
                        
                           
                    def send_to_display2():
                        if len(disp_calcul.get()) == 0:
                            disp_calcul.insert(0, lstbox.get(lstbox.curselection()))
                        else:
                            disp_calcul.insert(len(disp_calcul.get()), "*"+lstbox.get(lstbox.curselection()))
                            
                    def done_d():
                        a = [i for i in ascii_lowercase]
                        var = {}
                        a = disp_calcul.get()
                        b = re.findall(r"(\b\w*[\.]?\w+\b|[\(\)\+\*\-\/])", a)
                        c = ""
                        
                        
                        
                        for ii, i in enumerate(b):
                            if i not in ["*", "/", "+", "-"]:
                                if re.match(r'^-?\d+(?:\.\d+)$', i) is None:
                                    print(i, 'and ', ii)
                                    if isfloat(i):
                                        var[str(ii)] = i
                                        c += str(i)
                                    else:
                                        if not isinstance(self.x_data, pd.DataFrame):
                                            raise TypeError
                                        var[i] = self.x_data[i]
                                        c += str(i)
                                else:
                                    var[str(ii)] = i
                                    c += str(i)
                            else:
                                c += i 
                                
  
   
                        
                        formula = c
                        offset = eval(formula, var)
                        print(offset)  
                        self.offset = np.log(offset)      
                        window2.destroy()
                        window2.quit()
                        
                        

                            
                    
                    disp_calcul = tk.Entry(window2, readonlybackground="yellow")
                    
                    
                    tk.Label(window2, text = 'Offset Expression',  bg="#3A7FF6", fg="white", font = ("Georgia")).grid(column = 0, row = 0,  sticky='nesw')
                    disp_calcul.grid(column=0, row=1, columnspan=5, sticky='nesw')
                    lab1 = tk.Label(window2,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Enter Coefficients for the Expression')
                    lab1.grid(column=0, row =2,  sticky='nesw')
                    coeff_entry = tk.Entry(window2)
                    coeff_entry.grid(column = 0, row = 3,  sticky='nesw')
                    send_to_btn = tk.Button(window2,   font = ("Georgia"), text = 'Add', command=lambda:send_to_display(coeff_entry.get()))
                    send_to_btn.grid(column = 1, row = 3,  sticky='nesw')
                    
                    
                    lab = tk.Label(window2,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'select variable/s for offset expression')
                    option_mdl = tk.StringVar(window2)
                    option_mdl.set(data)
                    
                    
                    lstbox = tk.Listbox(window2, listvariable=option_mdl, selectmode=tk.SINGLE)
                    lstbox.grid(column=5, row =2,  sticky='nesw')
                    send_to_btn2 = tk.Button(window2,   font = ("Georgia"), text = 'Use', command=send_to_display2)
                    send_to_btn2.grid(column=5, row =3,  sticky='nesw')
                    
                    
                    lstboxy.grid(column=5, row=1,  sticky='nesw')
                    lab.grid(column=5, row =0, sticky='nesw')
                    done = tk.Button(window2,   font = ("Georgia"), text = 'Done', command = done_d)
                    done.grid(column=3, row = 5, sticky='nesw')
                    window2.mainloop()
                    
                    
                def delete_item(case):
                    def option_changed():
                        #self.random_pars_dist = values_contaner
                        for val in values_contaner:
                            i = val.get()
                            self.random_pars_dist.append(i)
                            print('the val is ', i)
                        window2.destroy()
                        
                    if case == 'normal':
                        selected_item = lstbox.curselection()
                        for item in selected_item[::-1]:
                            lstbox.delete(item)
                            print(self.normal_pars)
                            self.normal_pars.insert(0, data[item])
                    elif case == 'random':
                        selected_item = rdm_bix.curselection()
                        window2 = tk.Tk()
                        values_contaner = []
                        for i, item in enumerate(selected_item[::-1]):
                            rdm_bix.delete(item)
                            option_rdm_tr = ['normal', 'lindley', 'triangular', 'uniform']
                            self.random_pars.append(data[selected_item[i]])
                            values = tk.StringVar(window2)
                            values.set(option_rdm_tr[0])
                            values_contaner.append(values)
                            tk.Label(window2,  bg="#3A7FF6", fg="white", font = ("Georgia"), text='select the distribution for '+str(data[selected_item[i]])).grid(column=0, row=i, sticky='nesw')
                            rdm_tran_box = tk.OptionMenu(window2, values, *option_rdm_tr)
                            rdm_tran_box.grid(row=i, column=1, sticky='nesw')
                            button = tk.Button(window2,  font = ("Georgia"), text='select', width=5, height=1,
                                               command=option_changed)
                            button.grid(row=len(option_rdm_tr) + 1, column=1, sticky='nesw')
                    elif case == 'forced':
                        selected_item = listboxnew.curselection()
                        for item in selected_item[::-1]:
                            listboxnew.delete(item)
                            print(self.forced_variables)
                            self.forced_variables.insert(0, data[item])
                        

                    
                    
                    elif case == 'model':
                        selected_item = mdl_box.get(mdl_box.curselection())
                        print(selected_item)
                        self.model = selected_item
                    else:
                        selected_item = case.curselection()
                        print(selected_item)
                        for item in selected_item[::-1]:
                            #.delete(item)
                            print(item)
                            self.random_pars_dist.append(item)
                df = pd.read_csv(output_path)
                self.x_data =df
                data = list(df.columns)
                print(data)
                lisst = window.grid_slaves()
                for l in lisst:
                    l.destroy()
                lisst = window.place_slaves()
                for l in lisst:
                    l.destroy()
                #canvas.pack_forget()
                values = tk.StringVar()
                values.set(data)
                choicesn = tk.StringVar(window)
                option_chcn = data
                choicesn.set(data[0])
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text='Choose the prediction').grid(row=0, column=0, sticky='nesw')
                
                lstboxy = tk.OptionMenu(window, choicesn, *option_chcn, command = show_data)
                lstboxy.grid(column=0, row=1, sticky='nesw')
                
               
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Define the offset').grid(row=0, column =5, sticky='nesw')
                Define_Offset_Btn = tk.Button(window, font = ("Georgia"), text='Define Offset', command = define_offset).grid(row =1, column = 5, sticky = 'nesw')
                
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Select the variables to force into the model').grid(row=0, column =6, sticky='nesw')
                expVals = tk.StringVar(window)
                expVals.set(data)
                newchoices = data #TODO what does this do
                
                listboxnew = tk.Listbox(window, listvariable=expVals, selectmode=tk.MULTIPLE)
                listboxnew.grid(column = 6, row = 1, sticky = 'nesw')
                tk.Button(window, text="Select",   font = ("Georgia"), command= lambda:delete_item('forced')).grid(column=6, row = 2, sticky='nesw')
                
                
                
                
                tk.Button(window, font = ("Georgia"),  text="Run", command=close_and_destroy).grid(column=7, row=1,sticky='nesw')
                   
        
            
        def btn_clicked():
            sizeA = size_alg_entry.get()
            iteration_enter = iterations_entry.get()
            time_enter = max_time_entry.get()
            output_path = path_entry.get()
            output_path = output_path.strip()
            self.output_path1 = output_path
            
            if not sizeA:
                if self.algorithm != 'select decisions':
                    tk.messagebox.showerror(
                        title="Empty Fields!", message="Please enter a number.")
                    return
            else:
                sizeA = int(sizeA)
                try:
                    if sizeA <=0 or  not isinstance(sizeA, (int, float)):
                        tk.messagebox.showerror(
                            "Invalid CPU time!", "CPU runtime must be positive (seconds).")
                        return
                    else:
                        self.population_size = sizeA
                    
                except:
                    tk.messagebox.showerror(
                        "Invalid input!", "input must be a positive integer.")
                    return
                    
                
            if not iteration_enter:
                if self.algorithm != 'select decisions':
                    tk.messagebox.showerror(
                        title="Empty Fields!", message="Please enter a number of iterations.")
                    return
            if not time_enter:
                if self.algorithm != 'select decisions':
                    tk.messagebox.showerror(
                        title="Empty Fields!", message="Please enter a time in seconds.")
                    return
            if not output_path:
                tk.messagebox.showerror(
                    title="Invalid Path!", message="Please select a valid dataset.")
                return
            if time_enter:
                amount = int(time_enter)
                try:
                    if amount <=0 or  not isinstance(amount, (int, float)):
                        tk.messagebox.showerror(
                            "Invalid CPU time!", "CPU runtime must be positive (seconds).")
                        return
                    else:
                        self.max_time_limit = amount
                    
                except:
                    tk.messagebox.showerror(
                        "Invalid CPU time!", "CPU runtime must be a number (seconds).")
                    return
            if iteration_enter:
                iteration_enter = int(iteration_enter)
                try:
                    if iteration_enter <=0 or  not isinstance(iteration_enter, (int, float)):
                        tk.messagebox.showerror(
                            "Invalid CPU time!", "CPU runtime must be positive (seconds).")
                        return
                    else:
                        self.max_iteration_limit = iteration_enter
                    
                except:
                    tk.messagebox.showerror(
                        "Invalid number of iterations!", "iterations must be a number.")
                    return
                    
                
            if self.algorithm == 'harmonny search':
                #iteration_enter = iteration_enter.strip()
                output = Path(output_path + "/build").expanduser().resolve()
                if output.exists() and not output.is_dir():
                    tk.messagebox.showerror(
                        "Exists!",
                        f"{output} already exists and is not a directory.\n"
                        "Enter a valid output directory.")
                elif output.exists() and output.is_dir() and tuple(output.glob('*')):
                    response = tk.messagebox.askyesno(
                        "Continue?",
                        f"Directory {output} is not empty.\n"
                        "Do you want to continue and overwrite?")
                    if not response:
                        return
                tk.messagebox.showinfo(
                    "Success!", f"Project successfully generated for dataset found in {output}.")
            elif self.algorithm == 'select decisions':
                def close_and_destroy():
                    self.y = choicesn.get()
                    window.destroy()
                    window.quit()
                
                def input_coeffients(case):
                    inp = inputtxt.get(1.0, "end-1c")
                    inp = inp.split()
                    inp = [float(i) for i in inp]
                    inp = np.array(inp)
                    
                    self.betas = inp    
                    
                def delete_item(case):
                    def option_changed():
                        #self.random_pars_dist = values_contaner
                        for val in values_contaner:
                            i = val.get()
                            self.random_pars_dist.append(i)
                            print('the val is ', i)
                        window2.destroy()
                    if case == 'normal':
                        selected_item = lstbox.curselection()
                        for item in selected_item[::-1]:
                            lstbox.delete(item)
                            print(self.normal_pars)
                            self.normal_pars.insert(0, data[item])
                    elif case == 'random':
                        selected_item = rdm_bix.curselection()
                        window2 = tk.Tk()
                        values_contaner = []
                        for i, item in enumerate(selected_item[::-1]):
                            rdm_bix.delete(item)
                            option_rdm_tr = ['normal', 'lindley', 'triangular']
                            self.random_pars.append(data[selected_item[i]])
                            values = tk.StringVar(window2)
                            values.set(option_rdm_tr[0])
                            values_contaner.append(values)
                            tk.Label(window2,  bg="#3A7FF6", fg="white", font = ("Georgia"), text='select the distribution for '+str(data[selected_item[i]])).grid(column=0, row=i, sticky='nesw')
                            rdm_tran_box = tk.OptionMenu(window2, values, *option_rdm_tr)
                            rdm_tran_box.grid(row=i, column=1, sticky = 'nesw')
                            button = tk.Button(window2, font = ("Georgia"), text='select', width=5, height=1,
                                               command=option_changed)
                            button.grid(row=len(option_rdm_tr) + 1, column=1, sticky='nesw')
                    elif case == 'zi':
                        selected_item = zi_bix.curselection()
                        for item in selected_item[::-1]:
                            zi_bix.delete(item)
                            print(self.zi_variables)
                            self.zi_variables.insert(0, data[item])
                                
                    elif case == 'forced':    
                        selected_item = listboxnew.curselection()
                        for item in selected_item[::-1]:
                            listboxnew.delete(item)
                            print(self.forced_variables)
                            self.forced_variables.insert(0, data[item])
                        
                    
                    elif case == 'model':
                        selected_item = mdl_box.get(mdl_box.curselection())
                        print(selected_item)
                        self.model = selected_item
                    else:
                        selected_item = case.curselection()
                        print(selected_item)
                        for item in selected_item[::-1]:
                            #.delete(item)
                            print(item)
                            self.random_pars_dist.append(item)
                df = pd.read_csv(output_path)
                if self.is_wide:
                    df = convert_df_columns_to_binary_and_wide(df, "Death")
                self.all_data =df
                data = list(df.columns)
                print(data)
                lisst = window.grid_slaves()
                for l in lisst:
                    l.destroy()
                lisst = window.place_slaves()
                for l in lisst:
                    l.destroy()
                #canvas.pack_forget()
                values = tk.StringVar()
                values.set(data)
                choicesn = tk.StringVar(window)
                option_chcn = data
                choicesn.set(data[0])
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text='Choose the prediction').grid(row=0, column=0, sticky='nesw')
                lstboxy = tk.OptionMenu(window, choicesn, *option_chcn, command=show_data)
                lstboxy.grid(column=0, row=1, sticky='nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Choose the predictors').grid(row = 0, column = 1, sticky='nesw')
                lstbox = tk.Listbox(window, listvariable=values, selectmode=tk.MULTIPLE)
                lstbox.grid(column=1, row=1, sticky='nesw')
                # Create a button to remove the selected items in the list
                tk.Button(window, font = ("Georgia"), text="Select", command= lambda:delete_item('normal')).grid(column=1, row = 2, sticky='nesw')
                
                option_rdm = tk.StringVar(window)
                option_rdm.set(data)
                option_zi = tk.StringVar(window)
                option_zi.set(data)
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Choose the random predictors').grid(row = 0, column = 2)
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Choose the ZI terms').grid(row = 0, column = 3)
                rdm_bix = tk.Listbox(window, listvariable=option_rdm, selectmode=tk.MULTIPLE)
                zi_bix = tk.Listbox(window, listvariable=option_zi, selectmode=tk.MULTIPLE)
                #rdm_bix.bind('<<ListboxSelect>>', select_show2)
                rdm_bix.grid(row =1, column =2, sticky='nesw')
                zi_bix.grid(row = 1, column =3, sticky='nesw' )
                tk.Button(window, font = ("Georgia"), text="Select", command=lambda:delete_item('random')).grid(column=2, row=2, sticky = 'nesw')
                tk.Button(window, font = ("Georgia"), text="Select", command=lambda:delete_item('zi')).grid(column=3, row=2, sticky = 'nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Choose the model').grid(row=0, column =4, sticky='nesw')
                option_mdl = tk.StringVar(window)
                option_mdl.set(['Poisson', 'NB', 'COMP'])
                mdl_box = tk.Listbox(window, listvariable = option_mdl, selectmode=tk.SINGLE)
                mdl_box.grid(row = 1, column =4, sticky='nesw')
                tk.Button(window,   font = ("Georgia"), text="Select", command=lambda: delete_item('model')).grid(column=4, row=2)
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = 'Enter Coeffients').grid(row=0, column =5, sticky='nesw')
                inputtxt = tk.Text(window,
                   height = 5,
                   width = 20)
                #create a command that inputs the coefficients
                tk.Button(window,   font = ("Georgia"), text="Select", command=lambda: input_coeffients('this does nothing')).grid(column=5, row=2, sticky='nesw')
                inputtxt.grid(row = 1, column = 5, sticky='nesw')
                
                tk.Button(window,  font = ("Georgia"), text="Run", command=close_and_destroy).grid(column=6, row=1, sticky='nesw')
                
            elif self.algorithm == 'simulated annealing':
                lisst = window.grid_slaves()
                for l in lisst:
                    l.destroy()
                lisst = window.place_slaves()
                for l in lisst:
                    l.destroy()
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Swap Percentage").grid(row=0, sticky = 'nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Number of Temperature Steps").grid(row=1, sticky='nesw')
                
                def sel():
                    selection = "You selected the option " + str(var.get())
                    tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = selection).grid(column = 0, row = 5, sticky='nesw')
                    if int(var.get()) == 1:
                        self.specify = 1
                    else:
                        self.specify = None    

                e1 = tk.Entry(window)
                e1.insert(0, "0.05")
                e2 = tk.Entry(window)
                e2.insert(0, "20")
                
                
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = "Select if you want to to choose the starting point").grid(column = 0, row = 2, sticky='nesw')
                
                var = tk.IntVar()
                R1 = tk.Radiobutton(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Select Starting Model", variable=var, value=1,
                  command=sel)
                R1.grid(column = 0, row = 3, sticky = 'nesw')

                R2 = tk.Radiobutton(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Start From Scratch", variable=var, value=2,
                  command=sel)
                R2.grid(column = 0, row = 4, sticky = 'nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text='Select Maximum Level Complexity').grid(row=5, column=0, sticky='nesw')
                
                choices_multi = tk.StringVar(window)
        
                
                choiceComplexity = tk.StringVar(window)
                option_complex = ['fixed effects', 'random parameters', 'random parameters with correlations']
                choiceComplexity.set(option_complex[1])
                
                complexityBOX = tk.OptionMenu(window, choiceComplexity, *option_complex, command = show_3)
                complexityBOX.grid(row = 5, column =1)
                print(ASSETS_PATH)
                generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
                generate_btn = tk.Button(font = ("Georgia"), text = 'GO', command=btn_clicked_sa)
                generate_btn.place(x=557, y=401, width=180, height=55)
               
    
                

                e1.grid(row=0, column=1, sticky = 'nesw')
                e2.grid(row=1, column=1, sticky = 'nesw')
                self.swap_sa = float(e1.get())
                self.step_sa = int(e2.get())
            elif self.algorithm == 'differential evolution':
                def sel():
                    selection = "You selected the option " + str(var.get())
                    tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = selection).grid(column = 0, row = 5, sticky='nesw')
                    if int(var.get()) == 1:
                        self.specify = 1
                    else:
                        self.specify = None 
                lisst = window.grid_slaves()
                for l in lisst:
                    l.destroy()
                lisst = window.place_slaves()
                for l in lisst:
                    l.destroy()
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Crossover Rate").grid(row=0, sticky='nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Adjustment Index").grid(row=1, sticky='nesw')

                e1 = tk.Entry(window)
                e2 = tk.Entry(window)

                e1.grid(row=0, column=1, sticky = 'nesw')
                e2.grid(row=1, column=1, sticky = 'nesw')
                e1.insert(0, "0.2")
                e2.insert(0, "1")
                
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = "Select if you want to to choose the starting point").grid(column = 0, row = 2, sticky='nesw')
                
                var = tk.IntVar()
                R1 = tk.Radiobutton(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Select Starting Model", variable=var, value=1,
                  command=sel)
                R1.grid(column = 0, row = 3, sticky = 'nesw')

                R2 = tk.Radiobutton(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Start From Scratch", variable=var, value=2,
                  command=sel)
                R2.grid(column = 0, row = 4, sticky = 'nesw')
                print(ASSETS_PATH)
                generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
                generate_btn = tk.Button(font = ("Georgia"), text = 'GO', command=btn_clicked_sa)
                generate_btn.place(x=557, y=401, width=180, height=55)
                self.CR_R = float(e1.get())
                self.ADJ_INDX= int(e2.get())
                
            elif self.algorithm == 'harmony search':
                
                def sel():
                    selection = "You selected the option " + str(var.get())
                    tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = selection).grid(column = 0, row = 5, sticky = 'nesw')
                    if int(var.get()) == 1:
                        self.specify = 1
                    else:
                        self.specify = None 
                lisst = window.grid_slaves()
                for l in lisst:
                    l.destroy()
                lisst = window.place_slaves()
                for l in lisst:
                    l.destroy()
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Crossover Rate").grid(row=0, column = 0, sticky='nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Harmony Memory Consideration Rate").grid(row=1, column =0, sticky='nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Pitch Adjustment Rate").grid(row=2, column=0, sticky='nesw')
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Pitch Adjustment Index").grid(row=3, column =0, sticky='nesw')

                e1 = tk.Entry(window)
                e2 = tk.Entry(window)
                e3 = tk.Entry(window)
                e4 = tk.Entry(window)

                e1.grid(row=0, column=1, sticky = 'nesw')
                e2.grid(row=1, column=1, sticky = 'nesw')
                e3.grid(row = 2, column =1, sticky = 'nesw')
                e4.grid(row = 3, column = 1, sticky = 'nesw')
                e1.insert(0, "0.75")
                e2.insert(0, "0.75") #hmcr
                e3.insert(0, "0.5") #pitch adjustment rate
                e4.insert(0, "1") #pitch adjustment index
                
                tk.Label(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text = "Select if you want to to choose the starting point").grid(column = 0, row = 4)
                
                var = tk.IntVar()
                R1 = tk.Radiobutton(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Select Starting Model", variable=var, value=1,
                  command=sel)
                R1.grid(column = 0, row = 5, sticky = 'nesw')

                R2 = tk.Radiobutton(window,  bg="#3A7FF6", fg="white", font = ("Georgia"), text="Start From Scratch", variable=var, value=2,
                  command=sel)
                R2.grid(column = 0, row = 6, sticky = 'nesw')
                print(ASSETS_PATH)
                generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
                generate_btn = tk.Button(font = ("Georgia"), text = 'GO', command=btn_clicked_sa)
                generate_btn.place(x=557, y=401, width=180, height=55)
            else:
                print('1')    
                    
                    
                    
               
        def select_path():
            global output_path
            filetypes = (('text files', '*.txt'), ('excel files', '*.xlsx'), ('csv files', '*.csv'))
            output_path =  "C:/Users/n9471103/.vscode/code_files/HS_BIC/Ex-16-3variables.csv"
            output_path =  "C:/Users/n9471103/soure/repos/HS_BIC/Ex-16-3variables.csv"
            output_path = tk.filedialog.askopenfilename(title = 'Open Crash Data', initialdir = os.getcwd(), filetypes=filetypes)
                #askdirectory()
            path_entry.delete(0, tk.END)
            path_entry.insert(0, output_path)
            print(output_path)
        def know_more_clicked(event):
            instructions = (
                "https://github.com/zahern/HS_BIC")
            webbrowser.open_new_tab(instructions)
        def make_label(master, x, y, h, w, *args, **kwargs):
            f = tk.Frame(master, height=h, width=w)
            f.pack_propagate(0)  # don't shrink
            f.place(x=x, y=y)
            label = tk.Label(f, *args, **kwargs)
            label.pack(fill=tk.BOTH, expand=1)
            return label
        window = tk.Tk()
        logo = tk.PhotoImage(file=ASSETS_PATH / "iconbitmap.gif")
        window.call('wm', 'iconphoto', window._w, logo)
        window.title("Efficient Estimation of Data Count Models")
        #window.geometry("862x519")
        window.minsize(width=862, height = 520)
        #window.geometry("%dx%d" % (self.window_width, self.window_height))
        window.configure(bg="#3A7FF6")
        canvas = tk.Canvas(
            window, bg="#3A7FF6", height=519, width=862,
            bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        
        canvas.create_rectangle(431, 0, 431 + 431+20, 0 + 519, fill="#FCFCFC", outline="")
        canvas.create_rectangle(40, 160, 40 + 60, 160 + 5 , fill="#FCFCFC", outline="red")
        text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
       
        size_alg_img = canvas.create_image(650.5, shift_y+167.5-81, image=text_box_bg)
       
        token_entry_img = canvas.create_image(650.5, shift_y+167.5, image=text_box_bg)
        URL_entry_img = canvas.create_image(650.5, shift_y+248.5, image=text_box_bg)
        filePath_entry_img = canvas.create_image(650.5, shift_y+329.5, image=text_box_bg)
        yaxish = 30
        size_alg_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
        size_alg_entry.place(x=490.0, y=137 + 25- 81+shift_y, width=321.0, height=yaxish)
        size_alg_entry.focus()
        iterations_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
        iterations_entry.place(x=490.0, y=137 + 25+shift_y, width=321.0, height=yaxish)
        iterations_entry.focus()
        max_time_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
        max_time_entry.place(x=490.0, y=218 + 25+shift_y, width=321.0, height=yaxish)
        path_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
        path_entry.place(x=490.0, y=299 + 25+shift_y, width=321.0, height=yaxish)
        path_entry.insert(0, "C:/Users/n9471103/source/repos/HS_BIC/Ex-16-3variables.csv") #todo: delete this
        
       
        output_path = "C:/Users/n9471103/source/repos/HS_BIC/Ex-16-3variables.csv"
        
        path_picker_img = tk.PhotoImage(file=ASSETS_PATH / "path_picker.png")
        path_picker_button = tk.Button(
            image=path_picker_img,
            text='',
            compound='center',
            fg='white',
            borderwidth=0,
            highlightthickness=0,
            command=select_path,
            relief='flat')
        path_picker_button.place(
            x=783, y=319+shift_y,
            width=24,
            height=22)
        title = tk.Label(
            text="Assisted Estimation of Data Count Models", bg="#3A7FF6", wraplength=400,
            justify="left",
            fg="white", font=("Arial-BoldMT", int(18.0)))
        title.place(x=27.0, y=20.0)
        
        info_text = tk.Label(
            text="This software can use a suite of optimisation algorithms. Harmony search, Simulated Annealing or Differential Evolution can be selected as the optimisation framework.\n\n"
                 "So far advanced models can predict crash counts for Negative Binomial, Poisson or Generalised Poisson. The optimsation algorithm selects the most appropriate specification. \n\n"
                 "Using this software the amount of decision variables can be controlled (cetrain explanatory variables, distributions and models can be exlcuded) which will enhance the estimation time.",
            bg="#3A7FF6", fg="white", wraplength=400, justify="left",
            font=("Georgia", int(13.0)))
       
        info_text.place(x=27.0, y=80.0)
        know_more = tk.Label(
            text="link to Github",
            bg="#3A7FF6", fg="white", cursor="hand2")
        know_more.place(x=27, y=460)
        know_more.bind('<Button-1>', know_more_clicked)
        generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
        generate_btn = tk.Button(
            image=generate_btn_img, borderwidth=0, highlightthickness=0,
            command=btn_clicked, relief="flat")
        generate_btn.place(x=557, y=401, width=180, height=55)
        
        
        txt_enter1 = canvas.create_text(
            490.0, 71+shift_y, text="First Choose an algorithm", fill="#515486",
            font=("Arial-BoldMT", int(13.0)), anchor="w")
        txt_enter2 = canvas.create_text(
            490.0, 156.0+shift_y, text=" ", fill="#515486",
            font=("Arial-BoldMT", int(13.0)), anchor="w")
        txt_enter3 = canvas.create_text(
            490.0, 234.5+shift_y, text=" ", fill="#515486",
            font=("Arial-BoldMT", int(13.0)), anchor="w")
        txt_enter4 = canvas.create_text(
            490.0, 315.5+shift_y, text="Select Dataset",
            fill="#515486", font=("Arial-BoldMT", int(13.0)), anchor="w")
        canvas.create_text(
            646.5, 428.5+shift_y, text="Generate",
            fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
        choices = tk.StringVar(window)
        choices_multi = tk.StringVar(window)
        option_chc = ["harmony search", "simulated annealing", "differential evolution", "select decisions"]
        multi_chc = ['single', 'multi']
        choices.set(option_chc[1])
        choices_multi.set(multi_chc[0])
        
        is_wide_chc = ['normal', 'binary_wide']
        choices_wide = tk.StringVar(window)
        choices_wide.set(is_wide_chc[0])
        w_wide = tk.OptionMenu(window, choices_wide, *is_wide_chc, command = show_wide)
        w_wide.config(font=("Georgia", int(12.0)))
        w = tk.OptionMenu(window, choices, *option_chc, command = show)
        w.config(font=("Georgia", int(12.0)))
        w2 = tk.OptionMenu(window, choices_multi, *multi_chc, command = show_2)
        w2.config(font=("Georgia", int(12.0)))
        x = 500
        y = 0
        y_spacing = 35
        wraplength = 150
        tk.Label(text="Choose an optimisation algorithm:", bg="white", fg="black", wraplength = wraplength, justify = 'left', font=("Georgia", int(10.0))).place(
            x=x, y=y)
        tk.Label(text="Choose single or multiobjective:", bg="white", fg="black", wraplength = wraplength, justify = 'left', font=("Georgia", int(10.0))).place(
            x=x, y=y+y_spacing)
        tk.Label(text="Choose normal or wide format for data:", bg="white", fg="black", wraplength = wraplength, justify = 'left', font=("Georgia", int(10.0))).place(
            x=x, y=y+2*y_spacing)
        
        
        w_wide.place(x = x+wraplength, y = y+2*y_spacing)
        w.place(x=x+wraplength, y=y)
        w2.place(x=x+wraplength, y=y+y_spacing)
        
        #window.resizable(False, False)
        
        CreateToolTip(w2, text = 'Single Objective is BIC.\n '
            'Multi Objective is: 1) In sample BIC, 2) Out of Sample MAE')
        window.mainloop()
# Press the green button in the gutter to run the script.
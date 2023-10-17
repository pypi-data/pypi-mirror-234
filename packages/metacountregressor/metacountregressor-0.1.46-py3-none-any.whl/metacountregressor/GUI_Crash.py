import webbrowser
import re
import sys
import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
from pathlib import Path

# Add tkdesigner to path
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

output_path = ""

def show(click):
    if click == "simulated annealing":
        b2 = tk.Button(window, text="YESSSS!!!")
        b2.pack()
    elif click == "differential evolution":
        a3 = tk.Label(window, text="Maybe")
        a3.pack()
    elif click == "harmony search":
        a3 = tk.Label(window, text="Maybe")
        a3.pack()


def btn_clicked():
    token = token_entry.get()
    URL = URL_entry.get()
    output_path = path_entry.get()
    output_path = output_path.strip()

    if not token:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter Token.")
        return
    if not URL:
        tk.messagebox.showerror(
            title="Empty Fields!", message="Please enter URL.")
        return
    if not output_path:
        tk.messagebox.showerror(
            title="Invalid Path!", message="Enter a valid output path.")
        return

    match = re.search(
        r'https://www.figma.com/file/([0-9A-Za-z]+)', URL.strip())
    if match is None:
        tk.messagebox.showerror(
            "Invalid URL!", "Please enter a valid file URL.")
        return

    file_key = match.group(1).strip()
    token = token.strip()
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

    designer = Designer(token, file_key, output)
    designer.design()

    tk.messagebox.showinfo(
        "Success!", f"Project successfully generated at {output}.")


def select_path():
    global output_path

    output_path = tk.filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(0, output_path)


def know_more_clicked(event):
    instructions = (
        "https://www.journals.elsevier.com/accident-analysis-and-prevention")
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
window.title("Tkinter Designer")

window.geometry("862x519")
window.configure(bg="#3A7FF6")


canvas = tk.Canvas(
    window, bg="#3A7FF6", height=519, width=862,
    bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(431, 0, 431 + 431, 0 + 519, fill="#FCFCFC", outline="")
canvas.create_rectangle(40, 160, 40 + 60, 160 + 5, fill="#FCFCFC", outline="")

text_box_bg = tk.PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
token_entry_img = canvas.create_image(650.5, 167.5, image=text_box_bg)
URL_entry_img = canvas.create_image(650.5, 248.5, image=text_box_bg)
filePath_entry_img = canvas.create_image(650.5, 329.5, image=text_box_bg)

token_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
token_entry.place(x=490.0, y=137+25, width=321.0, height=35)
token_entry.focus()

URL_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
URL_entry.place(x=490.0, y=218+25, width=321.0, height=35)

path_entry = tk.Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
path_entry.place(x=490.0, y=299+25, width=321.0, height=35)

path_picker_img = tk.PhotoImage(file = ASSETS_PATH / "path_picker.png")
path_picker_button = tk.Button(
    image = path_picker_img,
    text = '',
    compound = 'center',
    fg = 'white',
    borderwidth = 0,
    highlightthickness = 0,
    command = select_path,
    relief = 'flat')

path_picker_button.place(
    x = 783, y = 319,
    width = 24,
    height = 22)

canvas.create_text(
    490.0, 156.0, text="Token ID", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    490.0, 234.5, text="File URL", fill="#515486",
    font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    490.0, 315.5, text="Output Path",
    fill="#515486", font=("Arial-BoldMT", int(13.0)), anchor="w")
canvas.create_text(
    646.5, 428.5, text="Generate",
    fill="#FFFFFF", font=("Arial-BoldMT", int(13.0)))
canvas.create_text(
    580, 88.0, text="Choose Optimisation Specification",
    fill="#515486", font=("Arial-BoldMT", int(14.0)))

title = tk.Label(
    text="Welcome to the Advanced Crash Count Estimation Tool (ACCET)", bg="#3A7FF6", wraplength = 400, justify = "left",
    fg="white", font=("Arial-BoldMT", int(18.0)))
title.place(x=27.0, y=60.0)

info_text = tk.Label(
    text="ACCET uses a suite of optimisation algorithms. Harmony search, simulated annealing and differential evolution can be selected as the optimisation framework.\n\n"

    "So far advanced models can predict crash counts for NB, Poisson or Poisson-Lognormal methods. The optimsation algorithm selects the most appropriate",
    bg="#3A7FF6", fg="white", wraplength = 400, justify="left",
    font=("Georgia", int(14.0)))

info_text.place(x=27.0, y=160.0)

know_more = tk.Label(
    text="Click here for publications",
    bg="#3A7FF6", fg="white", cursor="hand2")
know_more.place(x=27, y=400)
know_more.bind('<Button-1>', know_more_clicked)

generate_btn_img = tk.PhotoImage(file=ASSETS_PATH / "generate.png")
generate_btn = tk.Button(
    image=generate_btn_img, borderwidth=0, highlightthickness=0,
    command=btn_clicked, relief="flat")
generate_btn.place(x=557, y=401, width=180, height=55)

choices = tk.StringVar(window)
option_chc = ["", "harmony search", "simulated annealing", "differential evolution",]
choices.set(option_chc[1])

w = ttk.OptionMenu(window, choices, *option_chc, command=show)
w.pack()
#width = 180, height =55, font = ("Arial-BoldMT", int(13.0)), command = show)
#w['values'] = ('harmony search', 'differential evolution', 'simulated annealing')
#w.grid(column=500, row=15)

# Shows february as a default value
#w.current(1)
#w.pack()
#w.place(x=490, y = 20, width=180, height =55)

window.resizable(False, False)
window.mainloop()
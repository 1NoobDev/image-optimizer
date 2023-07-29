import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import os
import ast
import webbrowser


def center_window(root):
    window_width = 350
    window_height = 250

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')

def optimize_image(image_path, output_path, quality=85):
    with Image.open(image_path) as img:
        img.save(output_path, quality=quality)

def optimize_images_from_files(files, output_directory, quality=85):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    progress_bar["maximum"] = len(files)

    for i, image_path in enumerate(files):
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_directory, filename)
        optimize_image(image_path, output_path, quality)
        progress_bar["value"] = i + 1
        root.update_idletasks()

def update_start_button_state():
    selected_files = ast.literal_eval(input_files.get())
    output_folder_selected = output_directory.get()
    if selected_files and all(file.lower().endswith(('.jpg', '.png')) for file in selected_files) and output_folder_selected:
        start_button.config(state=tk.NORMAL)
    else:
        start_button.config(state=tk.DISABLED)

def select_input_files():
    files_selected = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg;*.png")])
    input_files.set(files_selected)
    update_start_button_state()

def select_output_directory():
    folder_selected = filedialog.askdirectory()
    output_directory.set(folder_selected)
    update_start_button_state()

def open_output_folder():
    webbrowser.open(output_directory.get())

def start_optimization():
    open_folder_button.config(state=tk.DISABLED) # Disable the button during optimization
    status_label.config(text="In progress...")  
    progress_bar["value"] = 0 # Reset progress bar at the start of a new optimization
    root.update_idletasks()  

    quality_level = int(quality.get())
    selected_files = ast.literal_eval(input_files.get())
    optimize_images_from_files(selected_files, output_directory.get(), quality_level)
    
    status_label.config(text="Image Optimization Completed")  
    root.update_idletasks()
    open_folder_button.config(state=tk.NORMAL) # Enable the button after optimization

root = tk.Tk()
root.title('Image Optimizer')
center_window(root)

input_files = tk.StringVar()
output_directory = tk.StringVar()
quality = tk.StringVar(value="85")

root.grid_rowconfigure(0, pad=15)
root.grid_rowconfigure(1, pad=15)
root.grid_rowconfigure(2, pad=15)
root.grid_rowconfigure(3, pad=15)

root.grid_columnconfigure(0, pad=10)
root.grid_columnconfigure(1, pad=10)
root.grid_columnconfigure(2, pad=10)

input_label = tk.Label(root, text='Input Files:')
input_label.grid(row=0, column=0)
input_entry = tk.Entry(root, textvariable=input_files)
input_entry.grid(row=0, column=1, padx=10)
input_button = tk.Button(root, text='Browse', command=select_input_files)
input_button.grid(row=0, column=2)

output_label = tk.Label(root, text='Output Directory:')
output_label.grid(row=1, column=0)
output_entry = tk.Entry(root, textvariable=output_directory)
output_entry.grid(row=1, column=1, padx=10)
output_button = tk.Button(root, text='Browse', command=select_output_directory)
output_button.grid(row=1, column=2)

quality_label = tk.Label(root, text='Quality (0-100):')
quality_label.grid(row=2, column=0)
quality_entry = tk.Entry(root, textvariable=quality)
quality_entry.grid(row=2, column=1, padx=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

status_label = tk.Label(root, text='') 
status_label.grid(row=5, column=0, columnspan=3)

open_folder_button = tk.Button(root, text='Open Output Folder', command=open_output_folder, state=tk.DISABLED)
open_folder_button.grid(row=3, column=1)

start_button = tk.Button(root, text='Start Optimization', command=start_optimization, state=tk.DISABLED)
start_button.grid(row=3, column=0)

root.mainloop()

# MainGUI.py

import tkinter as tk
from tkinter import filedialog
import pandas as pd
from ChartDisplay import display_bar_chart, show_all_dataframes

class DataVisualizationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("数据可视化 GUI")

        self.left_frame = tk.Frame(self.master)
        self.left_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        self.right_frame = tk.Frame(self.master)
        self.right_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        self.dataframes = {}
        self.selected_dataframe = None

        self.create_widgets()

    def create_widgets(self):
        load_button = tk.Button(self.right_frame, text="加载文件", command=self.load_files)
        load_button.pack(side=tk.TOP, padx=10, pady=5)

        self.pmt_button = tk.Menubutton(self.right_frame, text="PMT", relief=tk.RAISED)
        self.pmt_button.pack(side=tk.TOP, padx=10, pady=5)
        self.pmt_button.menu = tk.Menu(self.pmt_button, tearoff=0)
        self.pmt_button["menu"] = self.pmt_button.menu

        self.pmt_button.menu.add_command(label="All", command=self.show_all_dataframes)

    def load_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")])
        if file_paths:
            for file_path in file_paths:
                file_name = file_path.split("/")[-1].split(".")[0]
                try:
                    df = pd.read_excel(file_path)
                    self.dataframes[file_name] = df
                except Exception as e:
                    print(f"Error loading file {file_name}: {e}")

            self.update_pmt_button_text()

    def update_pmt_button_text(self):
        for item in self.pmt_button.menu.winfo_children():
            if item.label != "All":
                item.destroy()

        if not self.dataframes:
            self.pmt_button.menu.add_command(label="PMT")
        else:
            for file_name in self.dataframes:
                self.pmt_button.menu.add_command(label=file_name, command=lambda name=file_name: self.select_dataframe(name))

    def select_dataframe(self, name):
        if name == "All":
            self.show_all_dataframes()
        else:
            self.selected_dataframe = self.dataframes.get(name)
            self.update_chart()

    def update_chart(self):
        display_bar_chart(self.left_frame, self.selected_dataframe)

    def show_all_dataframes(self):
        show_all_dataframes(self.left_frame, self.dataframes)

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizationApp(root)
    root.geometry("800x600")
    root.mainloop()

import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class DataVisualizationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("数据可视化 GUI")

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 12))
        style.map("TButton", foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '!disabled', 'gray'), ('active', 'black')])

        self.button_frame = tk.Frame(self.master)
        self.button_frame.place(relx=0, rely=0, anchor=tk.NW)

        self.chart_frame = tk.Frame(self.master)
        self.chart_frame.place(relx=0.1, rely=0.1, anchor=tk.NW)

        self.dataframes = {}
        self.selected_dataframe = None

        self.load_button_text = tk.StringVar()
        self.load_button_text.set("加载文件")

        self.create_widgets()

    def create_widgets(self):
        load_button = ttk.Button(self.button_frame, textvariable=self.load_button_text, command=self.load_files)
        load_button.pack(side=tk.TOP, padx=10, pady=5)

        self.pmt_combobox = ttk.Combobox(self.button_frame, state="readonly")
        self.pmt_combobox.set("请选择PMT文件")
        self.pmt_combobox.pack(side=tk.TOP, padx=10, pady=5)
        self.pmt_combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)

        # 创建 Figure 和 Axes 对象
        self.fig, self.ax = plt.subplots(figsize=(4, 3), tight_layout=True)

        # 创建 Canvas 对象，用于显示图表
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=10, pady=10)

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

            self.update_combobox_values()

    def update_combobox_values(self):
        combobox_values = list(self.dataframes.keys()) + ["All"]
        self.pmt_combobox["values"] = combobox_values

        self.load_button_text.set("文件已加载")

    def on_combobox_selected(self, event):
        selected_value = self.pmt_combobox.get()
        self.select_dataframe(selected_value)

    def select_dataframe(self, name):
        if name == "All":
            self.show_all_dataframes()
        else:
            self.selected_dataframe = self.dataframes.get(name)
            self.update_chart()

    def update_chart(self):
        self.ax.clear()

        if self.selected_dataframe is not None:
            complexity_data = self.selected_dataframe["复杂度"].iloc[-1]

            window_width = self.chart_frame.winfo_width()
            window_height = self.chart_frame.winfo_height()

            if len(self.dataframes) > 1:  # Multiple files
                index = np.arange(len(self.dataframes))
                self.ax.bar(index, complexity_data, align='center', color='skyblue', edgecolor='black', linewidth=1.5)
                self.ax.set_xticks([])  # 不显示横轴标签
            else:  # Single file
                bar_width = window_width / 4
                self.ax.bar([0], complexity_data, width=bar_width, align='center', color='skyblue', edgecolor='black', linewidth=1.5)

            self.ax.set_title("PMT", fontsize=14)
            self.ax.set_xlabel("", fontsize=12)
            self.ax.set_ylabel("", fontsize=12)
            self.ax.set_yticks(range(0, 250, 50), fontsize=10)

            # 重新绘制 Canvas
            self.canvas.draw()

    def show_all_dataframes(self):
        self.ax.clear()

        if not self.dataframes:
            return

        window_width = self.chart_frame.winfo_width()
        window_height = self.chart_frame.winfo_height()

        if len(self.dataframes) > 1:  # Multiple files
            for file_name, df in self.dataframes.items():
                complexity_data = df["复杂度"].iloc[-1]
                self.ax.bar(file_name, complexity_data, label=file_name, color='skyblue', edgecolor='black', linewidth=1.5)

            self.ax.set_title("PMT", fontsize=14)
            self.ax.set_xlabel("", fontsize=12)
            self.ax.set_ylabel("", fontsize=12)
            self.ax.legend()
            self.ax.set_yticks(range(0, 250, 50))
            self.ax.tick_params(axis='y', labelsize=10)
        else:  # Single file
            for file_name, df in self.dataframes.items():
                complexity_data = df["复杂度"].iloc[-1]
                bar_width = window_width / 4
                self.ax.bar([0], complexity_data, width=bar_width, align='center', color='skyblue', edgecolor='black', linewidth=1.5)

            self.ax.set_title("PMT", fontsize=14)
            self.ax.set_xlabel("", fontsize=12)
            self.ax.set_ylabel("", fontsize=12)
            self.ax.set_yticks(range(0, 250, 50), fontsize=10)

        # 重新绘制 Canvas
        self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizationApp(root)
    root.geometry("800x600")
    root.mainloop()

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

        self.style = ttk.Style()

        self.load_button_frame = ttk.Frame(self.master)
        self.load_button_frame.place(relx=0, rely=0, relwidth=0.1, relheight=0.05)

        self.pmt_button_frame = ttk.Frame(self.master)
        self.pmt_button_frame.place(relx=0, rely=0.06, relwidth=0.15, relheight=0.05)

        self.chart_frame = tk.Frame(self.master)
        self.chart_frame.place(relx=0.01, rely=0.1, relwidth=0.5, relheight=0.6)

        self.dataframes = {}
        self.selected_dataframe = None

        self.load_button_text = tk.StringVar()
        self.load_button_text.set("加载文件")

        self.pmt_button_text = tk.StringVar()
        self.pmt_button_text.set("请选择PMT文件")

        self.create_widgets()

        # 绑定窗口大小变化事件
        self.master.bind("<Configure>", self.on_window_resize)

    def create_widgets(self):
        load_button = ttk.Button(self.load_button_frame, textvariable=self.load_button_text, command=self.load_files)
        load_button.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        pmt_button = ttk.Button(self.pmt_button_frame, textvariable=self.pmt_button_text, command=self.select_pmt_files)
        pmt_button.place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.8)

        # 设置按钮字体大小为相应比例
        font_size = int(self.master.winfo_width() * 0.01)
        self.style.configure("TButton", font=('Helvetica', font_size))

        # 创建 Figure 和 Axes 对象
        self.fig, self.ax = plt.subplots(figsize=(3, 3), tight_layout=True)

        # 创建 Canvas 对象，用于显示图表
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(relx=0.01, rely=0.1, relwidth=0.8, relheight=0.8)

    def on_window_resize(self, event):
        # 窗口大小变化时调整按钮字体大小
        font_size = int(self.master.winfo_width() * 0.01)
        self.style.configure("TButton", font=('Helvetica', font_size))

    def load_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx;*.xls"), ("All files", "*.*")])
        if file_paths:
            for file_path in file_paths:
                file_name = file_path.split("/")[-1].split(".")[0]
                try:
                    df = pd.read_excel(file_path)
                    self.dataframes[file_name] = df
                except Exception as e:
                    print(f"加载文件时出错 {file_name}: {e}")

            self.update_combobox_values()

    def update_combobox_values(self):
        combobox_values = list(self.dataframes.keys()) + ["全部"]
        self.pmt_button_text.set("请选择PMT文件")
        self.load_button_text.set("文件已加载")

    def select_pmt_files(self):
        self.pmt_menu = tk.Menu(self.pmt_button_frame, tearoff=0)
        for file_name in self.dataframes.keys():
            self.pmt_menu.add_command(label=file_name, command=lambda name=file_name: self.select_pmt_file(name))
        self.pmt_menu.add_command(label="全部", command=lambda: self.select_pmt_file("全部"))
        self.pmt_button_text.set("请选择PMT文件")
        self.pmt_menu.post(self.pmt_button_frame.winfo_rootx(), self.pmt_button_frame.winfo_rooty() + self.pmt_button_frame.winfo_height())

    def select_pmt_file(self, name):
        self.selected_dataframe = None if name == "全部" else self.dataframes.get(name)
        self.update_chart()

    def update_chart(self):
        self.ax.clear()

        window_width = self.chart_frame.winfo_width()
        window_height = self.chart_frame.winfo_height()

        if self.selected_dataframe is not None:
            complexity_data = self.selected_dataframe["复杂度"].iloc[-1]

            if len(self.dataframes) > 1:  # 多个文件
                index = np.arange(len(self.dataframes))
                self.ax.bar(index, complexity_data, align='center', color='skyblue', edgecolor='black', linewidth=1.5)
                self.ax.set_xticks([])  # 不显示横轴标签
            else:  # 单个文件
                bar_width = window_width / 4
                self.ax.bar([0], complexity_data, width=bar_width, align='center', color='skyblue', edgecolor='black', linewidth=1.5)

            self.ax.set_title("PMT", fontsize=14)
            self.ax.set_xlabel("", fontsize=12)
            self.ax.set_ylabel("", fontsize=12)
            self.ax.tick_params(axis='y', labelsize=10)
            self.ax.set_yticks(range(0, 250, 50))

        elif not self.dataframes:
            return

        else:  # 显示全部文件
            for file_name, df in self.dataframes.items():
                complexity_data = df["复杂度"].iloc[-1]
                self.ax.bar(file_name, complexity_data, label=file_name, color='skyblue', edgecolor='black', linewidth=1.5)

            self.ax.set_title("PMT", fontsize=14)
            self.ax.set_xlabel("", fontsize=12)
            self.ax.set_ylabel("", fontsize=12)
            self.ax.legend()
            self.ax.set_yticks(range(0, 250, 50))
            self.ax.tick_params(axis='y', labelsize=10)

        # 重新绘制 Canvas
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizationApp(root)
    root.geometry("800x600")
    root.mainloop()

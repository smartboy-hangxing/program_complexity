import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("数据可视化 GUI")

        # 使用ttk模块中的主题样式
        style = tk.ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 12))
        style.map("TButton", foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', '!disabled', 'gray'), ('active', 'black')])

        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

        self.chart_frame = tk.Frame(self.master, width=self.master.winfo_width() / 2, height=self.master.winfo_height() * 2 / 5)
        self.chart_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)

        self.dataframes = {}
        self.selected_dataframe = None

        self.create_widgets()

    def create_widgets(self):
        # 使用ttk.Button替代Button以获得更好的外观
        load_button = tk.ttk.Button(self.button_frame, text="加载文件", command=self.load_files)
        load_button.pack(side=tk.TOP, padx=10, pady=5)

        # 使用ttk.Combobox代替Menubutton以获得更好的外观
        self.pmt_combobox = tk.ttk.Combobox(self.button_frame, values=["All"], state="readonly")
        self.pmt_combobox.set("All")
        self.pmt_combobox.pack(side=tk.TOP, padx=10, pady=5)
        self.pmt_combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)

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
        # 更新Combobox的值，包括"All"和数据框名称
        combobox_values = ["All"] + list(self.dataframes.keys())
        self.pmt_combobox["values"] = combobox_values

    def on_combobox_selected(self, event):
        # Combobox选项更改时的处理程序
        selected_value = self.pmt_combobox.get()
        self.select_dataframe(selected_value)

    def select_dataframe(self, name):
        if name == "All":
            self.show_all_dataframes()
        else:
            self.selected_dataframe = self.dataframes.get(name)
            self.update_chart()

    def update_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if self.selected_dataframe is not None:
            complexity_data = self.selected_dataframe["复杂度"].iloc[-1]

            window_width = self.master.winfo_width()
            window_height = self.master.winfo_height()

            figsize = (window_width / 2 / 100, window_height * 2 / 5 / 100)

            plt.figure(figsize=figsize)
            bar_width = window_width / 20
            plt.bar([0], complexity_data, width=bar_width, align='center', color='skyblue')

            plt.title("PMT", fontsize=14)
            plt.xlabel("Complexity", fontsize=12)
            plt.ylabel("", fontsize=12)
            plt.yticks(range(0, 250, 50), fontsize=10)

            canvas = FigureCanvasTkAgg(plt.gcf(), master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=10, pady=10)

    def show_all_dataframes(self):
        if not self.dataframes:
            return

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()

        figsize = (window_width / 2 / 100, window_height * 2 / 5 / 100)

        plt.figure(figsize=figsize)
        ax = plt.gca()

        for file_name, df in self.dataframes.items():
            complexity_data = df["复杂度"].iloc[-1]
            ax.bar(file_name, complexity_data, label=file_name)

        ax.set_title("PMT", fontsize=14)
        ax.set_xlabel("Complexity", fontsize=12)
        ax.set_ylabel("", fontsize=12)
        ax.legend()
        ax.set_yticks(range(0, 250, 50), fontsize=10)

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=10, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizationApp(root)
    root.geometry("800x600")
    root.mainloop()

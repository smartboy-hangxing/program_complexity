# ChartDisplay.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def display_bar_chart(left_frame, complexity_data):
    for widget in left_frame.winfo_children():
        widget.destroy()

    plt.figure(figsize=(6, 4))
    bar_width = left_frame.winfo_width() / 10  # 计算柱状图宽度为窗口宽度的1/10
    plt.bar([0], complexity_data, width=bar_width, align='center')

    plt.title("PMT")
    plt.xlabel("复杂度")
    plt.ylabel("")
    plt.yticks(range(0, 250, 50))  # 设置纵轴刻度

    canvas = FigureCanvasTkAgg(plt.gcf(), master=left_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=10, pady=10)

def show_all_dataframes(left_frame, dataframes):
    if not dataframes:
        return

    for widget in left_frame.winfo_children():
        widget.destroy()

    plt.figure(figsize=(6, 4))
    for file_name, df in dataframes.items():
        complexity_data = df["复杂度"].iloc[-1]
        plt.bar(file_name, complexity_data, label=file_name)

    plt.title("PMT")
    plt.xlabel("Complexity")
    plt.ylabel("")
    plt.legend()
    plt.yticks(range(0, 250, 50))

    canvas = FigureCanvasTkAgg(plt.gcf(), master=left_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=10, pady=10)

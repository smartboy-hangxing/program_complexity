import pandas as pd
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import layout
from datetime import datetime, timedelta

# 读取 Excel 数据
df = pd.read_excel('data.xlsx')

# 创建 ColumnDataSource
source = ColumnDataSource(data=dict(time=[], value=[]))

# 创建绘图工具
plot = figure(title='Dynamic Data Plot', height=300, width=800, x_axis_type='datetime')
line = plot.line('time', 'value', source=source, line_width=2)

# 更新数据的回调函数
def update():
    # 模拟实时数据更新，添加新的数据点
    new_data = dict(time=[datetime.now()], value=[df['Value'].iloc[curdoc().counter]])
    source.stream(new_data, rollover=100)  # 使用 rollover 控制显示的数据量
    curdoc().counter += 1

# 添加定时器，每100毫秒更新一次数据
curdoc().add_periodic_callback(update, 50)

# 设置 Bokeh 应用
curdoc().counter = 0  # 添加计数器
curdoc().title = 'Dynamic Plot Example'

# 设置布局
layout_ = layout([[plot]])

# 启动 Bokeh 应用
curdoc().add_root(layout_)

# import os
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import plotly.graph_objects as go
# from datetime import datetime
#
# def read_structure_file(file_path):
#     """读取结构文件并解析数据"""
#     structures = {}
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#         x_coord = int(lines[0].split()[0])  # 读取x坐标
#         n_structures = int(lines[0].split()[1])  # 读取结构数量
#         for i in range(1, n_structures + 1):
#             ymin, ymax, vmin, vmax = map(int, lines[i].split())
#             if x_coord not in structures:
#                 structures[x_coord] = []
#             structures[x_coord].append((ymin, ymax, vmin, vmax))
#     print(f"文件 {file_path} 已读取，结构数据：{structures}")
#     return structures
#
# def plot_structures(structures):
#     """使用Plotly绘制3D图形，并根据yv范围的重叠情况突出显示结构"""
#     if not structures:
#         print("没有结构数据可绘制。")
#         return
#     fig = go.Figure()
#     for x in sorted(structures.keys()):
#         for structure in structures[x]:
#             ymin, ymax, vmin, vmax = structure
#             # 判断当前结构是否有临近重叠
#             has_overlap = check_overlap(x, ymin, ymax, vmin, vmax, structures)
#             color = 'red' if not has_overlap else 'blue'
#             X = np.array([x, x, x, x, x+1, x+1, x+1, x+1])
#             Y = np.array([ymin, ymin, ymax, ymax, ymin, ymin, ymax, ymax])
#             Z = np.array([vmin, vmax, vmin, vmax, vmin, vmax, vmin, vmax])
#             fig.add_trace(go.Mesh3d(
#                 x=X, y=Y, z=Z,
#                 color=color,
#                 opacity=0.5,
#                 alphahull=0,
#                 hoverinfo='text',
#                 text=f"X: {x}<br>Y: {ymin}-{ymax}<br>V: {vmin}-{vmax}"
#             ))
#     fig.update_layout(scene=dict(
#         xaxis_title='X',
#         yaxis_title='Y',
#         zaxis_title='V'
#     ))
#
#     now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"/Users/naoj306/Desktop/find/fila_plot_{now}.html"  # 修改这里的路径
#     fig.write_html(filename)  # 保存为HTML
#     print(f"图形已保存为: {filename}")
#
# def check_overlap(x, ymin, ymax, vmin, vmax, structures):
#     """检查指定结构在x ± 5范围内是否有yv重叠"""
#     for xi in range(x-5, x+6):
#         if xi != x and xi in structures:
#             for (nymin, nymax, nvmin, nvmax) in structures[xi]:
#                 if not (ymax < nymin or ymin > nymax or vmax < nvmin or vmin > nvmax):
#                     return True
#     return False
#
# def analyze_structures(directory):
#     all_structures = {}
#     for filename in os.listdir(directory):
#         if filename.endswith(".txt"):
#             file_path = os.path.join(directory, filename)
#             structures = read_structure_file(file_path)
#             for x in structures:
#                 if x not in all_structures:
#                     all_structures[x] = []
#                 all_structures[x].extend(structures[x])
#     print(f"所有结构：{all_structures}")
#     plot_structures(all_structures)
#
# # 使用该函数
# analyze_structures('/Users/naoj306/Desktop/find/location/nonan_diff_1-99_3-3/')

# import os
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# from datetime import datetime
#
# def read_structure_file(file_path):
#     """从CSV文件读取并解析数据"""
#     df = pd.read_csv(file_path)
#     structures = {}
#     for _, row in df.iterrows():
#         x_coord = int(row['x channel'])
#         ymin = int(row['ymin'])
#         ymax = int(row['ymax'])
#         vmin = int(row['vmin'])
#         vmax = int(row['vmax'])
#         length = float(row['length'])
#         binary_class = int(row['class'])
#         if binary_class == 1:  # 只处理长度 > 15 的情况
#             if x_coord not in structures:
#                 structures[x_coord] = []
#             structures[x_coord].append((ymin, ymax, vmin, vmax, length))
#     return structures
#
# def plot_structures(structures):
#     if not structures:
#         print("没有结构数据可绘制。")
#         return
#     fig = go.Figure()
#     for x in sorted(structures.keys()):
#         for structure in structures[x]:
#             ymin, ymax, vmin, vmax, length = structure
#             # 根据颜色逻辑检查重叠
#             color = get_color(x, ymin, ymax, vmin, vmax, length, structures)
#             if color:  # 仅在有颜色时绘制（跳过长度 < 15 的情况）
#                 X = np.array([x, x, x, x, x+1, x+1, x+1, x+1])
#                 Y = np.array([ymin, ymin, ymax, ymax, ymin, ymin, ymax, ymax])
#                 Z = np.array([vmin, vmax, vmin, vmax, vmin, vmax, vmin, vmax])
#                 fig.add_trace(go.Mesh3d(
#                     x=X, y=Y, z=Z,
#                     color=color,
#                     opacity=0.5,
#                     alphahull=0,
#                     hoverinfo='text',
#                     text=f"X: {x}<br>Y: {ymin}-{ymax}<br>V: {vmin}-{vmax}"
#                 ))
#     fig.update_layout(scene=dict(
#         xaxis_title='X',
#         yaxis_title='Y',
#         zaxis_title='V'
#     ))
#     now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     filename = f"fila_plot_{now}.html"
#     fig.write_html(filename)  # 保存为HTML
#     print(f"图形已保存为: {filename}")
#
# def get_color(x, ymin, ymax, vmin, vmax, length, structures):
#     if length < 15:
#         return None  # 不显示长度 < 15 的结构
#     overlaps = check_overlap(x, ymin, ymax, vmin, vmax, structures)
#     if overlaps:
#         if all(len > 15 for _, _, _, _, len in overlaps):
#             return 'blue'
#         if all(len < 15 for _, _, _, _, len in overlaps):
#             return 'green'
#     return 'red'
#
# def check_overlap(x, ymin, ymax, vmin, vmax, structures):
#     overlaps = []
#     for xi in range(x-5, x+6):
#         if xi != x and xi in structures:
#             for (nymin, nymax, nvmin, nvmax, length) in structures[xi]:
#                 if not (ymax < nymin or ymin > nymax or vmax < nvmin or vmin > nvmax):
#                     overlaps.append((nymin, nymax, nvmin, nvmax, length))
#     return overlaps
#
# def analyze_structures(file_path):
#     structures = read_structure_file(file_path)
#     print(f"所有结构：{structures}")
#     plot_structures(structures)
#
# # 使用该函数
# file_path = '/Users/naoj306/Desktop/find/location/nonan_diff_1-99_3-3/location.csv'
# analyze_structures(file_path)

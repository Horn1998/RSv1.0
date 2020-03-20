from openpyxl import load_workbook
from Common.FileProcess.TXTFile import TXTFile
import json    #绘图
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图
#数据处理
workbook = load_workbook(u'data1.xlsx')    #找到需要xlsx文件的位置
booksheet = workbook.active                 #获取当前活跃的sheet,默认是第一个sheet
z_name = ['Municipal Waste Landfilled(%)','Municipal Waste Incinerated(%)', 'Municipal Waste Recycled(%)',	'Municipal Waste Composted(%)','	GDP of the country in the corresponding year',	'The total population in the corresponding year',	'Annual investment in environmental protection']
#获取sheet页的行数据
rows = booksheet.rows
for i in range(6, 7):
    answer = []
    for row in rows:
        line = [col.value for col in row]
        target = line[1].replace('W', '')
        target = target.replace('S','')
        target = target.replace('E','')
        target = target.replace('N','')
        target = target.replace('s','')
        target = target.replace('e','')
        target = target.replace('n','')
        target = target.replace('w','')

        target = target.replace('\'', '')
        target = target.replace('°', '.')

        target = target.replace('，', ',')
        target = (target + ',' + str(line[i + 5])).split(',')
        if len(target) == 3: answer.append([float(target[0].split('.')[0]),float(target[1].split('.')[0]),float(target[2])])

    with open("record.json","w") as f:
        json.dump(answer, f)
        print("加载入文件完成...")



    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 数据
    with open('record.json', 'r') as f:
        data = json.load(f)
    print(data)
    data = np.array(data)
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]

    # 绘制散点图
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.bar3d(x, y, z, dx=[6],dy=[6],dz=[6])

    # 添加坐标轴(顺序是Z, Y, X)
    ax.set_zlabel(z_name[i], fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('latitude', fontdict={'size': 15, 'color': 'red'})
    ax.set_xlabel('longitude', fontdict={'size': 15, 'color': 'red'})
    plt.show()

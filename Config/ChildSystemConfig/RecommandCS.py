from Common.LogProcess.Logger import Logger
import os
#数据路径， 数据列名（固定), 分隔符， 模型选择
RSConfig = ({
    'path': r'D:\Restart_RA\Recommand\测试数据\u.data',
    'line_format': 'user item rating',
    'sep': '\t',
    'type': 'MatrixFactorization',
    'reader': 'normal'
})
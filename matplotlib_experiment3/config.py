# config.py
import matplotlib.pyplot as plt
import matplotlib

# 全局配置
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 100
plt.rcParams['savefig.dpi'] = 300

# 颜色配置
COLORS = {  # 注意：这里应该是 COLORS，不是 GOLOBE
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#18A999',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'gray': '#6C757D'
}

# 图表样式
STYLE_CONFIG = {
    'figure.figsize': (10, 6),
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'legend.fontsize': 10
}

# 更新配置
plt.rcParams.update(STYLE_CONFIG)
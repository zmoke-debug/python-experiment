# task2_consumption.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

from config import COLORS

def load_consumption_data():
    """加载消费收入数据"""
    df = pd.read_csv('data/consumption_income.csv')
    print("消费收入数据加载成功！")
    print(df.head())
    
    # 计算增长率
    df['GDP_Growth'] = df['GDP_per_Capita'].pct_change() * 100
    df['Consumption_Growth'] = df['Consumption_per_Capita'].pct_change() * 100
    
    return df

def plot_dual_axis_comparison(df):
    """绘制双轴对比图"""
    fig, ax1 = plt.subplots(figsize=(14, 8))
    
    # 左侧Y轴：人均GDP和消费
    color1 = COLORS['primary']
    color2 = COLORS['secondary']
    
    ax1.set_xlabel('年份', fontsize=12)
    ax1.set_ylabel('金额 (元)', fontsize=12)
    
    # 绘制人均GDP
    line1 = ax1.plot(df['Year'], df['GDP_per_Capita'],
                    color=color1, linewidth=2.5,
                    marker='o', markersize=6,
                    label='人均国民收入')
    
    # 绘制人均消费
    line2 = ax1.plot(df['Year'], df['Consumption_per_Capita'],
                    color=color2, linewidth=2.5,
                    marker='s', markersize=6,
                    label='人均消费支出')
    
    ax1.tick_params(axis='y')
    ax1.set_xticks(df['Year'])
    ax1.set_xticklabels(df['Year'], rotation=45)
    ax1.grid(True, alpha=0.3, axis='both')
    
    # 右侧Y轴：消费率
    ax2 = ax1.twinx()
    color3 = COLORS['warning']
    
    ax2.set_ylabel('消费率 (%)', color=color3, fontsize=12)
    line3 = ax2.plot(df['Year'], df['Consumption_Rate'],
                    color=color3, linewidth=2,
                    linestyle='--', marker='^',
                    markersize=6, label='消费率')
    ax2.tick_params(axis='y', labelcolor=color3)
    
    # 合并图例
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=11)
    
    # 添加填充区域
    ax1.fill_between(df['Year'], df['GDP_per_Capita'], df['Consumption_per_Capita'],
                    alpha=0.2, color=COLORS['gray'], label='储蓄部分')
    
    # 添加标题
    plt.title('人均消费与人均国民收入对比分析 (2010-2023)', 
             fontsize=16, fontweight='bold', pad=20)
    
    # 添加数据表格
    table_data = []
    for _, row in df.iterrows():
        table_data.append([
            int(row['Year']),
            f"{row['GDP_per_Capita']:,.0f}",
            f"{row['Consumption_per_Capita']:,.0f}",
            f"{row['Consumption_Rate']:.1f}%"
        ])
    
    plt.table(cellText=table_data,
             colLabels=['年份', '人均收入', '人均消费', '消费率'],
             cellLoc='center',
             loc='bottom',
             bbox=[0.1, -0.4, 0.8, 0.3])
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.savefig('images/consumption_charts/dual_axis_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_regression_analysis(df):
    """绘制回归分析图"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. 主散点图与回归线
    x = df['GDP_per_Capita']
    y = df['Consumption_per_Capita']
    
    # 线性回归
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    regression_line = slope * x + intercept
    
    scatter1 = axes[0, 0].scatter(x, y, c=df['Year'], cmap='coolwarm', 
                                 s=120, alpha=0.8, edgecolors='black', linewidth=1)
    
    axes[0, 0].plot(x, regression_line, 'r--', linewidth=2.5,
                   label=f'y = {slope:.4f}x + {intercept:.1f}\nR² = {r_value**2:.4f}')
    
    axes[0, 0].set_title('人均收入 vs 人均消费（线性回归）', fontsize=14)
    axes[0, 0].set_xlabel('人均国民收入 (元)')
    axes[0, 0].set_ylabel('人均消费支出 (元)')
    axes[0, 0].legend(loc='upper left')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 添加颜色条
    cbar1 = plt.colorbar(scatter1, ax=axes[0, 0])
    cbar1.set_label('年份')
    
    # 2. 残差图
    residuals = y - regression_line
    
    axes[0, 1].scatter(x, residuals, color=COLORS['secondary'], s=80, alpha=0.7)
    axes[0, 1].axhline(y=0, color='red', linestyle='--', alpha=0.7)
    axes[0, 1].fill_between(x, 0, residuals, where=(residuals >= 0), 
                           alpha=0.2, color=COLORS['danger'], label='正残差')
    axes[0, 1].fill_between(x, 0, residuals, where=(residuals < 0), 
                           alpha=0.2, color=COLORS['success'], label='负残差')
    
    axes[0, 1].set_title('回归残差分析', fontsize=14)
    axes[0, 1].set_xlabel('人均国民收入 (元)')
    axes[0, 1].set_ylabel('残差')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. 增长率对比
    years_for_plot = df['Year'][1:]  # 去掉第一年（没有增长率）
    
    width = 0.35
    x_indices = np.arange(len(years_for_plot))
    
    bars1 = axes[1, 0].bar(x_indices - width/2, df['GDP_Growth'].dropna(),
                          width, label='GDP增长率', color=COLORS['primary'], alpha=0.7)
    bars2 = axes[1, 0].bar(x_indices + width/2, df['Consumption_Growth'].dropna(),
                          width, label='消费增长率', color=COLORS['secondary'], alpha=0.7)
    
    axes[1, 0].set_title('GDP与消费增长率对比', fontsize=14)
    axes[1, 0].set_xlabel('年份')
    axes[1, 0].set_ylabel('增长率 (%)')
    axes[1, 0].set_xticks(x_indices)
    axes[1, 0].set_xticklabels([int(year) for year in years_for_plot], rotation=45)
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # 添加数值标签
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width()/2., height + 0.1,
                           f'{height:.1f}', ha='center', va='bottom', fontsize=8)
    
    # 4. 消费率与城镇化关系
    scatter2 = axes[1, 1].scatter(df['Consumption_Rate'], df['Urbanization_Rate'],
                                 c=df['Year'], cmap='viridis', s=100, alpha=0.8)
    
    # 添加趋势线
    z = np.polyfit(df['Consumption_Rate'], df['Urbanization_Rate'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['Consumption_Rate'].min(), df['Consumption_Rate'].max(), 100)
    axes[1, 1].plot(x_line, p(x_line), 'r--', linewidth=2)
    
    axes[1, 1].set_title('消费率 vs 城镇化率', fontsize=14)
    axes[1, 1].set_xlabel('消费率 (%)')
    axes[1, 1].set_ylabel('城镇化率 (%)')
    axes[1, 1].grid(True, alpha=0.3)
    
    # 添加颜色条
    cbar2 = plt.colorbar(scatter2, ax=axes[1, 1])
    cbar2.set_label('年份')
    
    plt.suptitle('消费与收入关系深度分析', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/consumption_charts/regression_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_consumption_structure(df):
    """绘制消费结构图"""
    # 模拟消费结构数据（实际中这部分数据需要更详细）
    np.random.seed(42)
    
    # 创建消费结构数据
    categories = ['食品烟酒', '衣着', '居住', '生活用品', '交通通信', 
                  '教育文化', '医疗保健', '其他用品']
    
    n_years = len(df)
    n_categories = len(categories)
    
    # 生成基础比例（随时间变化）
    base_proportions = np.array([0.30, 0.08, 0.25, 0.05, 0.12, 0.10, 0.07, 0.03])
    
    # 生成趋势：食品比例下降，其他上升
    trends = np.zeros((n_years, n_categories))
    for i in range(n_years):
        trends[i] = base_proportions * (1 + np.random.normal(0, 0.05, n_categories))
        trends[i, 0] *= (1 - i * 0.01)  # 食品比例逐年下降
        trends[i, 2] *= (1 + i * 0.005)  # 居住比例逐年上升
        trends[i, 5] *= (1 + i * 0.008)  # 教育文化逐年上升
        trends[i] = trends[i] / trends[i].sum()  # 归一化
    
    # 转换为金额
    consumption_amounts = trends * df['Consumption_per_Capita'].values[:, np.newaxis]
    
    # 创建堆积面积图
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # 子图1：消费结构堆积面积图
    colors = plt.cm.Set3(np.linspace(0, 1, n_categories))
    
    bottom = np.zeros(n_years)
    for i in range(n_categories):
        axes[0].fill_between(df['Year'], bottom, bottom + consumption_amounts[:, i],
                            color=colors[i], alpha=0.8, label=categories[i])
        bottom += consumption_amounts[:, i]
    
    axes[0].set_title('人均消费支出结构变化 (2010-2023)', fontsize=14)
    axes[0].set_xlabel('年份')
    axes[0].set_ylabel('消费金额 (元)')
    axes[0].legend(loc='upper left', bbox_to_anchor=(1.02, 1))
    axes[0].grid(True, alpha=0.3)
    axes[0].set_xticks(df['Year'][::2])
    
    # 子图2：比例变化雷达图（首尾年份对比）
    ax_radar = axes[1]
    
    # 设置雷达图角度
    angles = np.linspace(0, 2 * np.pi, n_categories, endpoint=False).tolist()
    angles += angles[:1]  # 闭合
    
    # 2010年和2023年数据
    values_2010 = trends[0].tolist()
    values_2023 = trends[-1].tolist()
    
    values_2010 += values_2010[:1]
    values_2023 += values_2023[:1]
    
    # 绘制雷达图
    ax_radar = fig.add_subplot(212, polar=True)
    ax_radar.plot(angles, values_2010, 'o-', linewidth=2, label='2010年')
    ax_radar.fill(angles, values_2010, alpha=0.25)
    ax_radar.plot(angles, values_2023, 'o-', linewidth=2, label='2023年')
    ax_radar.fill(angles, values_2023, alpha=0.25)
    
    # 设置刻度标签
    ax_radar.set_xticks(angles[:-1])
    ax_radar.set_xticklabels(categories, fontsize=10)
    ax_radar.set_title('消费结构比例变化对比（雷达图）', fontsize=14, pad=20)
    ax_radar.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    ax_radar.grid(True)
    
    plt.tight_layout()
    plt.savefig('images/consumption_charts/consumption_structure.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """主函数"""
    print("=" * 60)
    print("实验任务二：人均消费与人均国民收入案例")
    print("=" * 60)
    
    # 加载数据
    df = load_consumption_data()
    
    # 创建输出目录
    os.makedirs('images/consumption_charts', exist_ok=True)
    
    # 绘制图表
    print("\n1. 绘制双轴对比图...")
    plot_dual_axis_comparison(df)
    
    print("\n2. 绘制回归分析图...")
    plot_regression_analysis(df)
    
    print("\n3. 绘制消费结构图...")
    plot_consumption_structure(df)
    
    print("\n所有图表已保存到 images/consumption_charts/ 目录")
    print("任务二完成！")

if __name__ == "__main__":
    main()
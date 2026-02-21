# task3_exam.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import os

from config import COLORS

def load_exam_data():
    """加载考试成绩数据"""
    df = pd.read_csv('data/exam_scores.csv')
    print("考试成绩数据加载成功！")
    print(f"数据形状: {df.shape}")
    
    print("\n数据预览:")
    print(df.head())
    
    print("\n基础统计信息:")
    print(df['Score'].describe())
    
    print("\n各班级统计:")
    print(df.groupby('Class')['Score'].describe())
    
    return df

def plot_comprehensive_histograms(df):
    """绘制综合直方图"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. 全体学生成绩直方图
    n_bins = 20
    n, bins, patches = axes[0, 0].hist(df['Score'], bins=n_bins,
                                      color=COLORS['primary'],
                                      edgecolor='black',
                                      alpha=0.7,
                                      density=False)
    
    # 添加正态分布曲线
    mu, std = df['Score'].mean(), df['Score'].std()
    x = np.linspace(df['Score'].min(), df['Score'].max(), 100)
    p = stats.norm.pdf(x, mu, std) * len(df) * (bins[1] - bins[0])
    axes[0, 0].plot(x, p, 'r--', linewidth=2.5, label='正态分布')
    
    # 添加统计线
    axes[0, 0].axvline(mu, color='green', linestyle='-', linewidth=2,
                      label=f'均值: {mu:.1f}')
    axes[0, 0].axvline(mu + std, color='orange', linestyle='--',
                      linewidth=1.5, alpha=0.7, label='±1标准差')
    axes[0, 0].axvline(mu - std, color='orange', linestyle='--',
                      linewidth=1.5, alpha=0.7)
    
    axes[0, 0].set_title('全体学生成绩分布', fontsize=14)
    axes[0, 0].set_xlabel('分数')
    axes[0, 0].set_ylabel('人数')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. 分班级直方图（叠加）
    classes = sorted(df['Class'].unique())
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['warning']]
    
    for cls, color in zip(classes, colors):
        class_scores = df[df['Class'] == cls]['Score']
        axes[0, 1].hist(class_scores, bins=15, alpha=0.5,
                       color=color, edgecolor='black',
                       label=f'班级{cls}', density=True)
    
    axes[0, 1].set_title('各班级成绩分布对比', fontsize=14)
    axes[0, 1].set_xlabel('分数')
    axes[0, 1].set_ylabel('密度')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. 累积分布函数
    sorted_scores = np.sort(df['Score'])
    y_vals = np.arange(len(sorted_scores)) / len(sorted_scores)
    
    axes[1, 0].plot(sorted_scores, y_vals, linewidth=2.5, color=COLORS['danger'])
    axes[1, 0].fill_between(sorted_scores, 0, y_vals,
                           alpha=0.3, color=COLORS['danger'])
    
    # 标注关键百分位
    percentiles = [25, 50, 75, 90, 95]
    percentile_values = np.percentile(df['Score'], percentiles)
    
    for p, value in zip(percentiles, percentile_values):
        axes[1, 0].axvline(value, color='gray', linestyle='--', alpha=0.5)
        y_pos = p / 100
        axes[1, 0].text(value, y_pos, f'{p}%: {value:.1f}',
                       fontsize=9, ha='right', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    axes[1, 0].set_title('成绩累积分布函数 (CDF)', fontsize=14)
    axes[1, 0].set_xlabel('分数')
    axes[1, 0].set_ylabel('累积概率')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. 分性别直方图
    gender_data = []
    gender_labels = []
    gender_colors = [COLORS['primary'], COLORS['secondary']]
    
    for i, gender in enumerate(['M', 'F']):
        gender_scores = df[df['Gender'] == gender]['Score']
        gender_data.append(gender_scores)
        gender_labels.append('男生' if gender == 'M' else '女生')
    
    # 使用violin plot展示分布
    violin_parts = axes[1, 1].violinplot(gender_data, showmeans=True,
                                        showmedians=True, showextrema=True)
    
    # 自定义violin plot颜色
    for i, pc in enumerate(violin_parts['bodies']):
        pc.set_facecolor(gender_colors[i])
        pc.set_alpha(0.6)
        pc.set_edgecolor('black')
    
    # 设置统计线颜色
    violin_parts['cmeans'].set_color('red')
    violin_parts['cmedians'].set_color('green')
    violin_parts['cmins'].set_color('black')
    violin_parts['cmaxes'].set_color('black')
    
    axes[1, 1].set_title('性别成绩分布对比（小提琴图）', fontsize=14)
    axes[1, 1].set_xlabel('性别')
    axes[1, 1].set_ylabel('分数')
    axes[1, 1].set_xticks([1, 2])
    axes[1, 1].set_xticklabels(gender_labels)
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.suptitle('考试成绩综合分析', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/exam_charts/comprehensive_histograms.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_grade_distribution(df):
    """绘制成绩等级分布"""
    # 创建成绩等级分布数据
    grade_order = ['A', 'B', 'C', 'D', 'F']
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 1. 整体等级分布饼图
    grade_counts = df['Grade'].value_counts().reindex(grade_order)
    
    # 定义颜色
    grade_colors = ['#FFD700', '#C0C0C0', '#CD7F32', '#8B7355', '#696969']
    
    wedges, texts, autotexts = axes[0].pie(grade_counts.values,
                                          labels=grade_counts.index,
                                          colors=grade_colors,
                                          autopct='%1.1f%%',
                                          startangle=90,
                                          explode=[0.05] * len(grade_counts))
    
    # 美化饼图
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    axes[0].set_title('成绩等级分布（全体）', fontsize=14)
    
    # 2. 分班级等级分布堆叠柱状图
    # 创建交叉表
    cross_tab = pd.crosstab(df['Class'], df['Grade'])
    cross_tab = cross_tab.reindex(columns=grade_order)
    
    # 计算百分比
    cross_tab_percent = cross_tab.div(cross_tab.sum(axis=1), axis=0) * 100
    
    # 绘制堆叠柱状图
    bottom = np.zeros(len(cross_tab_percent))
    for i, grade in enumerate(grade_order):
        axes[1].bar(cross_tab_percent.index, cross_tab_percent[grade],
                   bottom=bottom, color=grade_colors[i], label=grade, alpha=0.8)
        bottom += cross_tab_percent[grade].values
    
    axes[1].set_title('各班级成绩等级分布', fontsize=14)
    axes[1].set_xlabel('班级')
    axes[1].set_ylabel('比例 (%)')
    axes[1].legend(title='等级', bbox_to_anchor=(1.05, 1), loc='upper left')
    axes[1].grid(True, alpha=0.3, axis='y')
    
    # 添加数值标签
    for i, cls in enumerate(cross_tab_percent.index):
        bottom = 0
        for grade in grade_order:
            value = cross_tab_percent.loc[cls, grade]
            if value > 5:  # 只显示大于5%的标签
                axes[1].text(i, bottom + value/2, f'{value:.1f}%',
                           ha='center', va='center', color='white',
                           fontweight='bold', fontsize=9)
            bottom += value
    
    plt.tight_layout()
    plt.savefig('images/exam_charts/grade_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_statistical_analysis(df):
    """绘制统计分析图"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. QQ图（检验正态性）
    stats.probplot(df['Score'], dist="norm", plot=axes[0, 0])
    axes[0, 0].get_lines()[0].set_marker('o')
    axes[0, 0].get_lines()[0].set_markersize(4)
    axes[0, 0].get_lines()[0].set_alpha(0.6)
    axes[0, 0].get_lines()[1].set_linewidth(2)
    axes[0, 0].get_lines()[1].set_color('red')
    axes[0, 0].set_title('QQ图 - 正态性检验', fontsize=14)
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. 分班级箱线图
    box_data = []
    box_labels = []
    
    for cls in sorted(df['Class'].unique()):
        box_data.append(df[df['Class'] == cls]['Score'])
        box_labels.append(f'班级{cls}')
    
    box = axes[0, 1].boxplot(box_data, labels=box_labels,
                            patch_artist=True,
                            showmeans=True,
                            meanline=True,
                            showfliers=True)
    
    # 自定义箱线图颜色
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['warning']]
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    
    # 设置中位数线和均值线样式
    for median in box['medians']:
        median.set_color('red')
        median.set_linewidth(2)
    
    for mean in box['means']:
        mean.set_color('green')
        mean.set_linewidth(2)
        mean.set_linestyle('--')
    
    axes[0, 1].set_title('各班级成绩箱线图', fontsize=14)
    axes[0, 1].set_ylabel('分数')
    axes[0, 1].grid(True, alpha=0.3, axis='y')
    
    # 3. 核密度估计
    for cls in sorted(df['Class'].unique()):
        class_scores = df[df['Class'] == cls]['Score']
        kde = stats.gaussian_kde(class_scores)
        x_range = np.linspace(df['Score'].min(), df['Score'].max(), 200)
        axes[1, 0].plot(x_range, kde(x_range), linewidth=2,
                       label=f'班级{cls}')
    
    axes[1, 0].set_title('各班级核密度估计', fontsize=14)
    axes[1, 0].set_xlabel('分数')
    axes[1, 0].set_ylabel('密度')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. 散点图与相关性
    # 创建模拟数据：假设有第二次考试成绩
    np.random.seed(123)
    df['Score2'] = df['Score'] * 0.8 + np.random.normal(0, 8, len(df)) + 15
    df['Score2'] = np.clip(df['Score2'], 0, 100)
    
    scatter = axes[1, 1].scatter(df['Score'], df['Score2'],
                                c=df['Class'].map({'A': 0, 'B': 1, 'C': 2}),
                                cmap='viridis',
                                s=80,
                                alpha=0.7,
                                edgecolors='black')
    
    # 添加回归线
    z = np.polyfit(df['Score'], df['Score2'], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df['Score'].min(), df['Score'].max(), 100)
    axes[1, 1].plot(x_line, p(x_line), 'r--', linewidth=2,
                   label=f'y = {z[0]:.2f}x + {z[1]:.2f}')
    
    # 计算相关系数
    correlation = df['Score'].corr(df['Score2'])
    axes[1, 1].text(0.05, 0.95,
                   f'相关系数: r = {correlation:.3f}',
                   transform=axes[1, 1].transAxes,
                   fontsize=12,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    axes[1, 1].set_title('两次考试成绩相关性', fontsize=14)
    axes[1, 1].set_xlabel('第一次考试分数')
    axes[1, 1].set_ylabel('第二次考试分数')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=axes[1, 1])
    cbar.set_label('班级 (0=A, 1=B, 2=C)')
    
    plt.suptitle('考试成绩统计分析', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/exam_charts/statistical_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """主函数"""
    print("=" * 60)
    print("实验任务三：考试成绩频率直方图案例")
    print("=" * 60)
    
    # 加载数据
    df = load_exam_data()
    
    # 创建输出目录
    os.makedirs('images/exam_charts', exist_ok=True)
    
    # 绘制图表
    print("\n1. 绘制综合直方图...")
    plot_comprehensive_histograms(df)
    
    print("\n2. 绘制成绩等级分布图...")
    plot_grade_distribution(df)
    
    print("\n3. 绘制统计分析图...")
    plot_statistical_analysis(df)
    
    print("\n所有图表已保存到 images/exam_charts/ 目录")
    print("任务三完成！")

if __name__ == "__main__":
    main()
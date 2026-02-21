# task1_stock.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# 导入配置
from .config import COLORS

def load_stock_data():
    """加载股票数据"""
    df = pd.read_csv('data/shanghai_index.csv')
    print("沪指数据加载成功！")
    print(df.head())
    print(f"\n数据统计：")
    print(df.describe())
    return df

def plot_basic_trend(df):
    """绘制基础趋势图"""
    plt.figure(figsize=(14, 7))
    
    # 创建子图
    ax1 = plt.subplot(2, 1, 1)
    
    # 绘制收盘价折线
    line = ax1.plot(df['Year'], df['Closing_Price'], 
                   color=COLORS['primary'],
                   linewidth=2.5,
                   marker='o',
                   markersize=4,
                   label='收盘价')
    
    # 添加移动平均线
    ma_5 = df['Closing_Price'].rolling(window=5).mean()
    ax1.plot(df['Year'], ma_5,
            color=COLORS['danger'],
            linewidth=2,
            linestyle='--',
            label='5年移动平均')
    
    # 标记特殊年份
    special_years = {2007: '大牛市', 2008: '金融危机', 2015: '杠杆牛', 2018: '贸易战'}
    for year, event in special_years.items():
        if year in df['Year'].values:
            idx = df[df['Year'] == year].index[0]
            price = df.loc[idx, 'Closing_Price']
            ax1.annotate(event,
                        xy=(year, price),
                        xytext=(0, 20),
                        textcoords='offset points',
                        ha='center',
                        arrowprops=dict(arrowstyle='->', color='gray'),
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    ax1.set_title('上证综合指数收盘价趋势 (2000-2023)', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('年份')
    ax1.set_ylabel('收盘价 (点)')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(df['Year'][::2])
    
    # 子图2：涨跌幅柱状图
    ax2 = plt.subplot(2, 1, 2)
    
    # 设置颜色（涨为红，跌为绿）
    colors = [COLORS['danger'] if x >= 0 else COLORS['success'] for x in df['Change_Percent']]
    bars = ax2.bar(df['Year'], df['Change_Percent'], color=colors, alpha=0.7)
    
    # 添加零线
    ax2.axhline(y=0, color='black', linewidth=0.8, linestyle='-')
    
    ax2.set_title('年度涨跌幅 (%)', fontsize=14)
    ax2.set_xlabel('年份')
    ax2.set_ylabel('涨跌幅 (%)')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_xticks(df['Year'][::2])
    
    # 标注最大涨跌幅
    max_gain_idx = df['Change_Percent'].idxmax()
    max_loss_idx = df['Change_Percent'].idxmin()
    
    ax2.annotate(f'↑{df.loc[max_gain_idx, "Change_Percent"]:.1f}%',
                xy=(df.loc[max_gain_idx, 'Year'], df.loc[max_gain_idx, 'Change_Percent']),
                xytext=(0, 10),
                textcoords='offset points',
                ha='center',
                fontweight='bold',
                color=COLORS['danger'])
    
    ax2.annotate(f'↓{df.loc[max_loss_idx, "Change_Percent"]:.1f}%',
                xy=(df.loc[max_loss_idx, 'Year'], df.loc[max_loss_idx, 'Change_Percent']),
                xytext=(0, -15),
                textcoords='offset points',
                ha='center',
                fontweight='bold',
                color=COLORS['success'])
    
    plt.tight_layout()
    plt.savefig('images/stock_charts/basic_trend.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def plot_candlestick_chart(df):
    """绘制K线图（简化版）"""
    # 由于我们只有年度数据，这里展示简化版的K线图
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), gridspec_kw={'height_ratios': [3, 1]})
    
    # 子图1：价格和交易量
    color_up = COLORS['danger']  # 上涨颜色
    color_down = COLORS['success']  # 下跌颜色
    
    # 为每年生成OHLC数据（简化）
    for i in range(1, len(df)):
        year = df.loc[i, 'Year']
        close = df.loc[i, 'Closing_Price']
        prev_close = df.loc[i-1, 'Closing_Price']
        change = df.loc[i, 'Change_Percent']
        
        # 生成模拟的开盘、最高、最低价
        open_price = prev_close * (1 + np.random.uniform(-0.02, 0.02))
        high_price = max(open_price, close) * (1 + np.random.uniform(0, 0.03))
        low_price = min(open_price, close) * (1 - np.random.uniform(0, 0.03))
        
        # 绘制K线
        color = color_up if close >= open_price else color_down
        line_width = 0.8
        
        # 绘制影线
        ax1.plot([year, year], [low_price, high_price], 
                color=color, linewidth=line_width)
        
        # 绘制实体
        width = 0.6
        ax1.add_patch(Rectangle((year - width/2, min(open_price, close)), 
                               width, abs(close - open_price),
                               facecolor=color, edgecolor=color))
    
    ax1.plot(df['Year'], df['Closing_Price'], 
            color='gray', alpha=0.5, linewidth=1, label='收盘价趋势')
    
    ax1.set_title('上证指数K线图（简化）', fontsize=16, fontweight='bold')
    ax1.set_xlabel('年份')
    ax1.set_ylabel('价格 (点)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(df['Year'][::2])
    
    # 子图2：交易量
    ax2.bar(df['Year'], df['Volume'] / 1e8, 
           color=[color_up if x >= 0 else color_down for x in df['Change_Percent']],
           alpha=0.6)
    
    ax2.set_title('年度交易量（亿股）', fontsize=14)
    ax2.set_xlabel('年份')
    ax2.set_ylabel('交易量 (亿股)')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_xticks(df['Year'][::2])
    
    plt.tight_layout()
    plt.savefig('images/stock_charts/candlestick_chart.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_correlation_analysis(df):
    """绘制相关性分析图"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. 自相关图
    lags = 10
    autocorr = [df['Closing_Price'].autocorr(lag) for lag in range(1, lags+1)]
    
    axes[0, 0].bar(range(1, lags+1), autocorr, color=COLORS['primary'], alpha=0.7)
    axes[0, 0].axhline(y=0, color='black', linewidth=0.8)
    axes[0, 0].set_title('收盘价自相关性分析', fontsize=14)
    axes[0, 0].set_xlabel('滞后阶数')
    axes[0, 0].set_ylabel('自相关系数')
    axes[0, 0].grid(True, alpha=0.3, axis='y')
    
    # 2. 收益率分布
    returns = df['Change_Percent'].dropna()
    
    axes[0, 1].hist(returns, bins=15, color=COLORS['secondary'], alpha=0.7, edgecolor='black')
    axes[0, 1].axvline(x=returns.mean(), color='red', linestyle='--', label=f'均值: {returns.mean():.2f}%')
    axes[0, 1].axvline(x=returns.median(), color='green', linestyle='--', label=f'中位数: {returns.median():.2f}%')
    axes[0, 1].set_title('年度收益率分布', fontsize=14)
    axes[0, 1].set_xlabel('收益率 (%)')
    axes[0, 1].set_ylabel('频数')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. 滚动波动率
    rolling_volatility = returns.rolling(window=5).std() * np.sqrt(1)
    
    axes[1, 0].plot(df['Year'][4:], rolling_volatility.dropna(), 
                    color=COLORS['warning'], linewidth=2)
    axes[1, 0].fill_between(df['Year'][4:], 0, rolling_volatility.dropna(),
                            alpha=0.3, color=COLORS['warning'])
    axes[1, 0].set_title('5年滚动波动率', fontsize=14)
    axes[1, 0].set_xlabel('年份')
    axes[1, 0].set_ylabel('波动率')
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].set_xticks(df['Year'][4::2])
    
    # 4. 价格与交易量散点图
    scatter = axes[1, 1].scatter(df['Change_Percent'], df['Volume'] / 1e8,
                                c=df['Year'], cmap='viridis', s=100, alpha=0.7)
    
    axes[1, 1].axvline(x=0, color='gray', linestyle='--', alpha=0.5)
    axes[1, 1].axhline(y=df['Volume'].mean() / 1e8, color='gray', linestyle='--', alpha=0.5)
    
    axes[1, 1].set_title('涨跌幅 vs 交易量', fontsize=14)
    axes[1, 1].set_xlabel('涨跌幅 (%)')
    axes[1, 1].set_ylabel('交易量 (亿股)')
    
    # 添加颜色条
    cbar = plt.colorbar(scatter, ax=axes[1, 1])
    cbar.set_label('年份')
    
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('上证指数技术分析', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/stock_charts/technical_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """主函数"""
    print("=" * 60)
    print("实验任务一：沪指综合指数收盘数据趋势图")
    print("=" * 60)
    
    # 加载数据
    df = load_stock_data()
    
    # 创建输出目录
    os.makedirs('images/stock_charts', exist_ok=True)
    
    # 绘制图表
    print("\n1. 绘制基础趋势图...")
    plot_basic_trend(df)
    
    print("\n2. 绘制K线图...")
    plot_candlestick_chart(df)
    
    print("\n3. 绘制技术分析图...")
    plot_correlation_analysis(df)
    
    print("\n所有图表已保存到 images/stock_charts/ 目录")
    print("任务一完成！")

if __name__ == "__main__":
    main()
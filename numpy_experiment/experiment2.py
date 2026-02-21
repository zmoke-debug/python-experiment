# -*- coding: utf-8 -*-
"""
实验二：基于NumPy的数据分析 - VS Code优化版
"""

import numpy as np
import matplotlib.pyplot as plt
import os

def normal_pdf(x, mu=0, sigma=1):
    """正态分布概率密度函数"""
    return (1/(sigma*np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mu)/sigma)**2)

def task1():
    """任务1：生成正态分布数据并绘制直方图"""
    print("=" * 50)
    print("任务1：生成正态分布数据并绘制直方图")
    print("=" * 50)
    
    np.random.seed(42)  # 固定随机种子
    data = np.random.normal(loc=0, scale=1, size=10000)
    
    print(f"数据数量: {len(data)}")
    print(f"均值: {np.mean(data):.4f}")
    print(f"方差: {np.var(data):.4f}")
    print(f"标准差: {np.std(data):.4f}")
    
    # 绘制直方图
    plt.figure(figsize=(10, 4))
    
    # 直方图1：频数分布
    plt.subplot(1, 2, 1)
    n, bins, _ = plt.hist(data, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('正态分布直方图 (n=10000)')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    # 添加正态分布曲线
    x = np.linspace(-4, 4, 1000)
    bin_width = bins[1] - bins[0]
    y = normal_pdf(x) * len(data) * bin_width
    plt.plot(x, y, 'r-', linewidth=2)
    
    # 直方图2：概率密度
    plt.subplot(1, 2, 2)
    plt.hist(data, bins=50, alpha=0.7, color='lightgreen', 
             edgecolor='black', density=True)
    plt.title('概率密度直方图')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.grid(True, alpha=0.3)
    plt.plot(x, normal_pdf(x), 'r-', linewidth=2)
    
    plt.tight_layout()
    plt.savefig('normal_dist_hist.png', dpi=150)
    print("\n直方图已保存为 'normal_dist_hist.png'")
    plt.show()

def task2():
    """任务2：矩阵运算"""
    print("\n" + "=" * 50)
    print("任务2：矩阵运算")
    print("=" * 50)
    
    np.random.seed(123)
    A = np.random.randint(1, 10, size=(3, 3))
    B = np.random.randint(1, 10, size=(3, 3))
    
    print("矩阵A:")
    print(A)
    print("\n矩阵B:")
    print(B)
    
    print("\n1. 矩阵加法 (A + B):")
    print(A + B)
    
    print("\n2. 矩阵减法 (A - B):")
    print(A - B)
    
    print("\n3. 逐元素乘法 (A * B):")
    print(A * B)
    
    print("\n4. 矩阵乘法 (A @ B):")
    print(A @ B)
    
    # 保存矩阵
    np.savetxt('matrix_A.txt', A, fmt='%d')
    np.savetxt('matrix_B.txt', B, fmt='%d')
    print("\n矩阵已保存为 matrix_A.txt 和 matrix_B.txt")

def create_sample_data():
    """创建示例数据文件"""
    # 创建示例数据
    data = """年份,人均国民收入(元),城镇居民收入(元),农村居民收入(元)
2015,49928,31195,11422
2016,53935,33616,12363
2017,59201,36396,13432
2018,64644,39251,14617
2019,70581,42359,16021
2020,72447,43834,17131
2021,80976,47412,18931
2022,85698,49283,20133"""
    
    with open('人均国民收入.csv', 'w', encoding='utf-8') as f:
        f.write(data)
    
    print("示例数据文件 '人均国民收入.csv' 已创建")
    return data

def task3():
    """任务3：文件读取与转换"""
    print("\n" + "=" * 50)
    print("任务3：文件读取与转换")
    print("=" * 50)
    
    # 检查文件是否存在，不存在则创建
    if not os.path.exists('人均国民收入.csv'):
        print("未找到数据文件，创建示例数据...")
        create_sample_data()
    
    try:
        # 使用numpy读取CSV文件
        print("使用np.loadtxt读取数据...")
        data = np.loadtxt('人均国民收入.csv', delimiter=',', skiprows=1)
        
        print(f"\n数据形状: {data.shape}")
        print("数据内容:")
        print(data)
        
        # 分析数据
        years = data[:, 0].astype(int)
        income = data[:, 1]
        
        print(f"\n数据分析:")
        print(f"年份范围: {years.min()} - {years.max()}")
        print(f"平均收入: {income.mean():.2f} 元")
        print(f"最高收入: {income.max():.2f} 元 (年份: {years[income.argmax()]})")
        
        # 绘制收入趋势图
        plt.figure(figsize=(8, 5))
        plt.plot(years, income, 'o-', linewidth=2, markersize=8)
        plt.title('人均国民收入变化趋势')
        plt.xlabel('年份')
        plt.ylabel('人均国民收入 (元)')
        plt.grid(True, alpha=0.3)
        
        # 添加数据标签
        for x, y in zip(years, income):
            plt.text(x, y+1000, f'{y:.0f}', ha='center', va='bottom', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('income_trend.png', dpi=150)
        print("\n趋势图已保存为 'income_trend.png'")
        plt.show()
        
    except Exception as e:
        print(f"读取文件时出错: {e}")
        print("尝试使用genfromtxt...")
        
        # 尝试使用genfromtxt
        data = np.genfromtxt('人均国民收入.csv', delimiter=',', 
                            dtype=None, encoding='utf-8', 
                            skip_header=1)
        print("\n读取到的数据:")
        print(data)

def main():
    """主函数"""
    print("实验二：基于NumPy的数据分析")
    print("=" * 50)
    
    while True:
        print("\n选择要执行的任务:")
        print("1. 正态分布直方图")
        print("2. 矩阵运算")
        print("3. 文件读取与转换")
        print("4. 全部执行")
        print("0. 退出")
        
        choice = input("请输入选择: ").strip()
        
        if choice == '1':
            task1()
        elif choice == '2':
            task2()
        elif choice == '3':
            task3()
        elif choice == '4':
            task1()
            task2()
            task3()
        elif choice == '0':
            print("程序退出")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    main()
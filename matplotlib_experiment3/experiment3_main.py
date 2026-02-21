# experiment3_main.py
import os
import time

def print_header():
    """打印实验标题"""
    print("=" * 70)
    print("实验三：基于Matplotlib库的数据可视化")
    print("=" * 70)
    print("实验目的：")
    print("  1. 熟悉Matplotlib库")
    print("  2. 掌握pyplot基础语法基本方法")
    print("  3. 掌握Matplotlib数据可视化的方法")
    print("实验任务：")
    print("  1. 沪指综合指数收盘数据趋势图案例")
    print("  2. 人均消费与人均国民收入案例")
    print("  3. 考试成绩频率直方图案例")
    print("=" * 70)
    print()

def check_environment():
    """检查环境和依赖"""
    print("检查Python环境和依赖库...")
    
    required_packages = ['numpy', 'pandas', 'matplotlib', 'scipy']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} 未安装，请使用 pip install {package} 安装")
            return False
    
    # 检查目录结构
    required_dirs = ['data', 'images']
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"  ✗ 目录 '{directory}' 不存在")
            return False
    
    print("环境检查通过！")
    print()
    return True

def run_experiment():
    """运行实验"""
    print("开始实验...")
    print()
    
    # 任务一
    print("[任务一] 沪指综合指数收盘数据趋势图案例")
    print("-" * 50)
    try:
        import task1_stock
        task1_stock.main()
        print("✓ 任务一完成")
    except Exception as e:
        print(f"✗ 任务一失败: {e}")
    print()
    
    time.sleep(1)
    
    # 任务二
    print("[任务二] 人均消费与人均国民收入案例")
    print("-" * 50)
    try:
        import task2_consumption
        task2_consumption.main()
        print("✓ 任务二完成")
    except Exception as e:
        print(f"✗ 任务二失败: {e}")
    print()
    
    time.sleep(1)
    
    # 任务三
    print("[任务三] 考试成绩频率直方图案例")
    print("-" * 50)
    try:
        import task3_exam
        task3_exam.main()
        print("✓ 任务三完成")
    except Exception as e:
        print(f"✗ 任务三失败: {e}")
    print()

def generate_report():
    """生成实验报告"""
    print("生成实验报告...")
    print("-" * 50)
    
    report_content = f"""
实验报告：基于Matplotlib库的数据可视化
生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}

一、实验完成情况
1. 沪指综合指数收盘数据趋势图案例
   - 基础趋势图（带移动平均线）
   - K线图（简化版）
   - 技术分析图（自相关、波动率等）

2. 人均消费与人均国民收入案例
   - 双轴对比图
   - 回归分析图
   - 消费结构图

3. 考试成绩频率直方图案例
   - 综合直方图（含CDF）
   - 成绩等级分布图
   - 统计分析图（QQ图、箱线图等）

二、生成的图表文件
图表已保存到 images/ 目录下的相应子文件夹中：
- stock_charts/: 股票相关图表
- consumption_charts/: 消费收入相关图表
- exam_charts/: 考试成绩相关图表

三、主要收获
1. 掌握了Matplotlib的基本绘图方法
2. 学会了多子图布局和复杂图表的创建
3. 了解了数据可视化在数据分析中的应用
4. 掌握了图表美化和自定义的技巧

四、建议与改进
1. 可以尝试添加交互式图表（使用Plotly）
2. 可以增加更多统计分析方法
3. 可以优化图表配色和布局
"""
    
    # 保存报告
    with open('实验报告.txt', 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(report_content)
    print("实验报告已保存到 '实验报告.txt'")
    print()
    print("=" * 70)
    print("实验三：基于Matplotlib库的数据可视化 - 实验完成！")
    print("=" * 70)

def main():
    """主函数"""
    print_header()
    
    if not check_environment():
        print("请先解决环境问题，然后重新运行实验。")
        return
    
    run_experiment()
    generate_report()

if __name__ == "__main__":
    main()
# create_data.py
import numpy as np
import pandas as pd
import os

def create_directories():
    """创建必要的目录"""
    directories = ['data', 'images/stock_charts', 'images/consumption_charts', 'images/exam_charts']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("目录创建完成！")

def create_shanghai_index_data():
    """创建沪指数据"""
    np.random.seed(42)
    
    # 生成2000-2023年的数据
    years = np.arange(2000, 2024)
    
    # 基础趋势：整体上升
    base_trend = np.linspace(1000, 3500, len(years))
    
    # 添加周期性波动
    cycle_1 = 400 * np.sin(2 * np.pi * (years - 2000) / 8)  # 8年周期
    cycle_2 = 200 * np.sin(2 * np.pi * (years - 2000) / 4)  # 4年周期
    
    # 添加随机波动
    random_shock = np.random.normal(0, 150, len(years))
    
    # 模拟几次重大事件的影响
    events = np.zeros(len(years))
    events[years == 2007] = 800   # 2007年牛市
    events[years == 2008] = -1000 # 2008年金融危机
    events[years == 2015] = 600   # 2015年牛市
    events[years == 2018] = -400  # 2018年贸易战
    
    # 计算最终收盘价
    closing_prices = base_trend + cycle_1 + cycle_2 + random_shock + events
    closing_prices = np.abs(closing_prices)  # 确保为正数
    closing_prices = np.round(closing_prices, 2)
    
    # 计算涨跌幅
    changes = np.zeros(len(years))
    changes[1:] = (closing_prices[1:] - closing_prices[:-1]) / closing_prices[:-1] * 100
    
    # 创建DataFrame
    df = pd.DataFrame({
        'Year': years,
        'Closing_Price': closing_prices,
        'Change_Percent': np.round(changes, 2),
        'Volume': np.random.uniform(1e8, 5e8, len(years)).astype(int)
    })
    
    # 保存到CSV
    df.to_csv('data/shanghai_index.csv', index=False, encoding='utf-8-sig')
    print(f"沪指数据已保存，共{len(df)}条记录")
    return df

def create_consumption_income_data():
    """创建人均消费与收入数据"""
    np.random.seed(123)
    
    years = np.arange(2010, 2024)
    
    # 人均GDP（国民收入）趋势
    gdp_base = np.linspace(30000, 85000, len(years))
    gdp_noise = np.random.normal(0, 3000, len(years))
    gdp_per_capita = gdp_base + gdp_noise
    
    # 人均消费支出（与GDP相关但增速略低）
    consumption_ratio = np.linspace(0.65, 0.58, len(years))  # 消费率逐年下降
    consumption_base = gdp_per_capita * consumption_ratio
    consumption_noise = np.random.normal(0, 2000, len(years))
    consumption_per_capita = consumption_base + consumption_noise
    
    # 其他相关指标
    savings_per_capita = gdp_per_capita - consumption_per_capita
    consumption_rate = (consumption_per_capita / gdp_per_capita * 100)
    
    # 创建DataFrame
    df = pd.DataFrame({
        'Year': years,
        'GDP_per_Capita': np.round(gdp_per_capita, 0),
        'Consumption_per_Capita': np.round(consumption_per_capita, 0),
        'Savings_per_Capita': np.round(savings_per_capita, 0),
        'Consumption_Rate': np.round(consumption_rate, 1),
        'Urbanization_Rate': np.round(np.linspace(49, 65, len(years)), 1)
    })
    
    # 保存到CSV
    df.to_csv('data/consumption_income.csv', index=False, encoding='utf-8-sig')
    print(f"消费收入数据已保存，共{len(df)}条记录")
    return df

def create_exam_scores_data():
    """创建考试成绩数据"""
    np.random.seed(456)
    
    n_students = 300
    
    # 生成三个不同班级的数据
    class_a_scores = np.random.normal(78, 8, n_students//3)  # A班：成绩较好
    class_b_scores = np.random.normal(65, 12, n_students//3) # B班：成绩中等
    class_c_scores = np.random.normal(55, 10, n_students//3) # C班：成绩较差
    
    # 合并所有成绩
    all_scores = np.concatenate([class_a_scores, class_b_scores, class_c_scores])
    all_scores = np.clip(all_scores, 0, 100)  # 限制在0-100分
    
    # 添加学号、班级信息
    student_ids = range(1, n_students + 1)
    classes = ['A'] * (n_students//3) + ['B'] * (n_students//3) + ['C'] * (n_students//3)
    
    # 创建DataFrame
    df = pd.DataFrame({
        'Student_ID': student_ids,
        'Class': classes,
        'Score': np.round(all_scores, 1),
        'Gender': np.random.choice(['M', 'F'], n_students)
    })
    
    # 计算等级
    def get_grade(score):
        if score >= 90: return 'A'
        elif score >= 80: return 'B'
        elif score >= 70: return 'C'
        elif score >= 60: return 'D'
        else: return 'F'
    
    df['Grade'] = df['Score'].apply(get_grade)
    
    # 保存到CSV
    df.to_csv('data/exam_scores.csv', index=False, encoding='utf-8-sig')
    print(f"考试成绩数据已保存，共{len(df)}条记录")
    return df

def main():
    """主函数：创建所有数据文件"""
    print("开始创建实验数据...")
    print("-" * 50)
    
    create_directories()
    
    # 创建三个数据集
    df1 = create_shanghai_index_data()
    df2 = create_consumption_income_data()
    df3 = create_exam_scores_data()
    
    print("-" * 50)
    print("所有数据文件创建完成！")
    print("\n数据概览：")
    print(f"1. 沪指数据：{len(df1)} 行 × {len(df1.columns)} 列")
    print(f"2. 消费收入数据：{len(df2)} 行 × {len(df2.columns)} 列")
    print(f"3. 考试成绩数据：{len(df3)} 行 × {len(df3.columns)} 列")

if __name__ == "__main__":
    main()
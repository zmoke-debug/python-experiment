"""
《红楼梦》人物出场次数分析程序
作者：学生
学号：
班级：
实验日期：
"""

import jieba
import jieba.posseg as pseg
from collections import Counter
import os

def check_environment():
    """检查运行环境"""
    print("=" * 60)
    print("《红楼梦》人物出场次数分析系统")
    print("=" * 60)
    
    # 显示当前目录
    current_dir = os.getcwd()
    print(f"当前工作目录: {current_dir}")
    
    # 显示文件列表
    print("\n当前目录下的文件:")
    files = os.listdir('.')
    txt_files = []
    
    for file in files:
        if file.endswith('.txt'):
            txt_files.append(file)
            print(f"  📄 {file}")
        elif file.endswith('.py'):
            print(f"  🐍 {file}")
    
    if not txt_files:
        print("  ❌ 没有找到任何文本文件！")
        return False
    
    print(f"\n找到 {len(txt_files)} 个文本文件")
    return True

def load_novel(file_path):
    """加载小说文本"""
    print(f"\n正在加载文件: {file_path}")
    
    # 尝试不同的编码方式
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            print(f"✓ 成功加载，编码: {encoding}")
            print(f"✓ 文件大小: {len(content):,} 字符")
            return content
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"✗ 读取文件时出错: {e}")
            return None
    
    print("✗ 无法识别文件编码格式")
    return None

def setup_jieba_dict():
    """设置jieba词典，添加《红楼梦》人物"""
    print("\n正在设置人物词典...")
    
    # 《红楼梦》主要人物列表
    characters = [
        # 主要人物
        ('贾宝玉', 10000),
        ('林黛玉', 10000),
        ('薛宝钗', 10000),
        
        # 贾府长辈
        ('贾母', 10000),
        ('贾政', 10000),
        ('王夫人', 10000),
        ('邢夫人', 10000),
        ('贾赦', 10000),
        
        # 贾府同辈
        ('贾琏', 10000),
        ('王熙凤', 10000),
        ('贾珍', 10000),
        ('贾蓉', 10000),
        ('秦可卿', 10000),
        
        # 贾府姐妹
        ('贾元春', 10000),
        ('贾迎春', 10000),
        ('贾探春', 10000),
        ('贾惜春', 10000),
        
        # 丫鬟
        ('袭人', 10000),
        ('晴雯', 10000),
        ('平儿', 10000),
        ('鸳鸯', 10000),
        ('紫鹃', 10000),
        
        # 其他重要人物
        ('史湘云', 10000),
        ('李纨', 10000),
        ('妙玉', 10000),
        ('巧姐', 10000),
        ('刘姥姥', 10000),
        ('薛蟠', 10000),
        ('香菱', 10000),
        ('贾雨村', 10000),
        ('甄士隐', 10000),
    ]
    
    # 添加到jieba词典
    for name, freq in characters:
        jieba.add_word(name, freq=freq, tag='nr')
    
    print(f"✓ 已添加 {len(characters)} 个人物到词典")
    return characters

def extract_characters(text):
    """从文本中提取人物"""
    print("\n正在分析文本中的人物...")
    
    # 使用jieba进行分词和词性标注
    words = pseg.cut(text)
    
    # 收集所有人名
    all_names = []
    for word, flag in words:
        if flag == 'nr':  # nr表示人名
            all_names.append(word)
    
    print(f"✓ 共找到 {len(all_names)} 个人名")
    return all_names

def clean_and_count(names):
    """清理并统计人物出现次数"""
    print("\n正在统计人物出场次数...")
    
    # 初始统计
    counter = Counter(names)
    
    # 人物别名映射（把不同的称呼映射到标准名称）
    alias_map = {
        # 贾宝玉
        '宝玉': '贾宝玉',
        '宝二爷': '贾宝玉',
        
        # 林黛玉
        '黛玉': '林黛玉',
        '林妹妹': '林黛玉',
        '颦儿': '林黛玉',
        
        # 薛宝钗
        '宝钗': '薛宝钗',
        '宝姐姐': '薛宝钗',
        
        # 王熙凤
        '熙凤': '王熙凤',
        '凤姐': '王熙凤',
        '凤姐儿': '王熙凤',
        '凤丫头': '王熙凤',
        
        # 贾母
        '老太太': '贾母',
        '老祖宗': '贾母',
        
        # 贾琏
        '琏二爷': '贾琏',
        '琏儿': '贾琏',
    }
    
    # 需要过滤掉的词（不是人物）
    filter_words = {
        '众人', '说道', '只见', '不知', '一面', '两个',
        '如今', '起来', '进去', '回来', '出去', '今日',
        '明日', '昨日', '这里', '那里', '这个', '那个',
        '我们', '你们', '他们', '自己', '说道', '笑道',
        '问道', '却说', '话说', '原来', '只是', '不是',
        '正是', '便是', '也是', '都是', '却是', '却是',
        '这是', '那是', '这是', '那是', '怎么', '什么',
        '如何', '为何', '因为', '所以', '然后', '忽然',
        '忽然', '连忙', '急忙', '只得', '只好', '只要',
        '只有', '只是', '只是', '只有', '只见'
    }
    
    # 清理数据
    cleaned_counter = Counter()
    
    for name, count in counter.items():
        # 过滤掉短词和常见词
        if len(name) < 2:
            continue
        
        if name in filter_words:
            continue
        
        # 处理别名
        if name in alias_map:
            cleaned_counter[alias_map[name]] += count
        else:
            cleaned_counter[name] += count
    
    print(f"✓ 清理后剩余 {len(cleaned_counter)} 个有效人物")
    return cleaned_counter

def get_top_characters(counter, top_n=10):
    """获取出场次数最多的前N个人物"""
    # 获取所有人物
    all_characters = counter.most_common()
    
    # 过滤掉出现次数太少的人物
    filtered = [(name, count) for name, count in all_characters if count >= 5]
    
    # 取前N个
    top_n = min(top_n, len(filtered))
    return filtered[:top_n]

def display_results(results, total_people):
    """显示统计结果"""
    print("\n" + "=" * 60)
    print("《红楼梦》人物出场次数排行榜")
    print("=" * 60)
    print(f"{'排名':<6}{'人物':<10}{'出场次数':<12}{'柱状图':<30}")
    print("-" * 60)
    
    if not results:
        print("没有找到有效的人物数据")
        return
    
    # 找到最高次数用于比例计算
    max_count = results[0][1] if results else 1
    
    for i, (name, count) in enumerate(results, 1):
        # 计算柱状图长度
        bar_length = int((count / max_count) * 25)
        bar = '█' * bar_length
        
        # 显示结果
        print(f"{i:<6}{name:<10}{count:<12}{bar:<30}")
    
    print("=" * 60)
    
    # 显示统计摘要
    print("\n📊 统计摘要:")
    print(f"  • 分析总人物数: {total_people}")
    print(f"  • 上榜人物数: {len(results)}")
    print(f"  • 第一名 {results[0][0]}: {results[0][1]} 次")
    if len(results) > 1:
        print(f"  • 第二名 {results[1][0]}: {results[1][1]} 次")

def save_results(results, filename="红楼梦人物统计.txt"):
    """保存结果到文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("《红楼梦》人物出场次数统计报告\n")
            f.write("=" * 50 + "\n")
            f.write(f"生成时间: 2024年\n")
            f.write(f"分析文件: 红楼梦.txt\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("🏆 人物出场次数排行榜\n\n")
            for i, (name, count) in enumerate(results, 1):
                f.write(f"{i:2d}. {name:<8} : {count:5d} 次\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("说明:\n")
            f.write("1. 统计基于jieba分词库的人物识别\n")
            f.write("2. 已合并同一人物的不同称呼\n")
            f.write("3. 已过滤常见非人物词汇\n")
        
        print(f"\n💾 结果已保存到: {filename}")
        return True
    except Exception as e:
        print(f"\n❌ 保存文件时出错: {e}")
        return False

def main():
    """主函数"""
    # 1. 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请确保红楼梦.txt文件在当前目录")
        input("按Enter键退出...")
        return
    
    # 2. 选择文件
    target_file = None
    if '红楼梦.txt' in os.listdir('.'):
        target_file = '红楼梦.txt'
    else:
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
        if txt_files:
            target_file = txt_files[0]
            print(f"\n⚠️  使用文件: {target_file}")
    
    if not target_file:
        print("\n❌ 没有找到可用的文本文件")
        input("按Enter键退出...")
        return
    
    # 3. 加载文本
    text = load_novel(target_file)
    if not text:
        print("\n❌ 无法加载文本")
        input("按Enter键退出...")
        return
    
    # 4. 设置jieba词典
    setup_jieba_dict()
    
    # 5. 提取人物
    all_names = extract_characters(text)
    
    if not all_names:
        print("\n❌ 没有找到人物")
        input("按Enter键退出...")
        return
    
    # 6. 统计和清理
    counter = clean_and_count(all_names)
    
    # 7. 获取前10名
    top_10 = get_top_characters(counter, 10)
    
    if not top_10:
        print("\n❌ 没有足够的有效数据")
        input("按Enter键退出...")
        return
    
    # 8. 显示结果
    display_results(top_10, len(counter))
    
    # 9. 保存结果
    save_results(top_10)
    
    # 10. 完成
    print("\n" + "🎉 " * 10)
    print("分析完成！")
    print("🎉 " * 10)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 等待用户按Enter退出
    input("\n按Enter键退出程序...")
"""
市场新闻分析器 - 主程序
允许用户选择不同的标的进行新闻分析
"""

import os
import sys
import argparse
from datetime import datetime
import logging
from typing import Optional, List, Dict, Any

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入配置和模块
from config.config import ASSET_CONFIG
from src.models import NewsItem, PriceItem, NewsScore, AnalysisReport
from src.news_fetcher import fetch_news, generate_test_news, setup_logging


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="市场新闻分析器 - 分析不同标的的新闻")
    
    # 添加资产类型参数
    parser.add_argument(
        "-a", "--asset", 
        type=str, 
        default="oil",
        choices=list(ASSET_CONFIG.keys()),
        help="要分析的资产类型"
    )
    
    # 添加日期参数
    parser.add_argument(
        "-d", "--date", 
        type=str, 
        default=datetime.now().strftime("%Y%m%d"),
        help="要分析的日期，格式为YYYYMMDD"
    )
    
    # 添加测试模式参数
    parser.add_argument(
        "-t", "--test", 
        action="store_true",
        help="使用测试数据而不是真实数据"
    )
    
    # 添加输出目录参数
    parser.add_argument(
        "-o", "--output", 
        type=str, 
        default="data",
        help="输出目录"
    )
    
    # 添加详细模式参数
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="显示详细输出"
    )
    
    return parser.parse_args()


def display_asset_menu():
    """显示资产选择菜单"""
    print("\n" + "="*50)
    print("市场新闻分析器 - 请选择要分析的资产类型")
    print("="*50)
    
    for i, (asset_key, asset_info) in enumerate(ASSET_CONFIG.items(), 1):
        print(f"{i}. {asset_info['asset_name']} ({asset_key})")
    
    print("0. 退出程序")
    print("="*50)
    
    while True:
        try:
            choice = input("请输入选项编号: ")
            if choice == "0":
                print("退出程序")
                sys.exit(0)
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(ASSET_CONFIG):
                asset_key = list(ASSET_CONFIG.keys())[choice_idx]
                return asset_key
            else:
                print(f"无效的选项，请输入0-{len(ASSET_CONFIG)}之间的数字")
        except ValueError:
            print("请输入有效的数字")


def display_date_menu():
    """显示日期选择菜单"""
    print("\n" + "="*50)
    print("请选择要分析的日期")
    print("="*50)
    print("1. 今天")
    print("2. 昨天")
    print("3. 指定日期")
    print("0. 返回上级菜单")
    print("="*50)
    
    while True:
        try:
            choice = input("请输入选项编号: ")
            if choice == "0":
                return None
            
            if choice == "1":
                return datetime.now().strftime("%Y%m%d")
            elif choice == "2":
                # 简单计算昨天日期，不考虑月底等特殊情况
                yesterday = datetime.now()
                yesterday = yesterday.replace(day=yesterday.day-1)
                return yesterday.strftime("%Y%m%d")
            elif choice == "3":
                date_str = input("请输入日期(YYYYMMDD格式): ")
                try:
                    # 验证日期格式
                    datetime.strptime(date_str, "%Y%m%d")
                    return date_str
                except ValueError:
                    print("日期格式不正确，请使用YYYYMMDD格式")
            else:
                print("无效的选项，请输入0-3之间的数字")
        except ValueError:
            print("请输入有效的数字")


def interactive_mode():
    """交互模式"""
    print("\n欢迎使用市场新闻分析器!")
    
    while True:
        # 选择资产类型
        asset_type = display_asset_menu()
        if asset_type is None:
            continue
        
        # 选择日期
        target_date = display_date_menu()
        if target_date is None:
            continue
        
        # 获取资产名称
        asset_name = ASSET_CONFIG[asset_type]["asset_name"]
        
        # 确认选择
        print(f"\n您选择了分析 {target_date} 的{asset_name}相关新闻")
        confirm = input("是否继续? (y/n): ")
        if confirm.lower() != "y":
            continue
        
        # 设置日志
        logger = setup_logging()
        
        # 获取新闻数据
        print(f"\n开始获取{asset_name}相关新闻...")
        news_items = fetch_news(asset_type, target_date, logger)
        
        # 如果没有找到新闻，询问是否使用测试数据
        if not news_items:
            print(f"没有找到{target_date}的{asset_name}相关新闻")
            use_test = input("是否使用测试数据? (y/n): ")
            if use_test.lower() == "y":
                news_items = generate_test_news(asset_type)
            else:
                print("返回主菜单")
                continue
        
        # 显示新闻标题
        print(f"\n获取到的{asset_name}相关新闻标题:")
        for i, item in enumerate(news_items, 1):
            print(f"{i}. {item.title} (来源: {item.source}, 情感分数: {item.alpha_sentiment:.2f})")
        
        print(f"\n{asset_name}新闻获取完成")
        
        # 询问是否继续分析其他资产
        continue_analysis = input("\n是否继续分析其他资产? (y/n): ")
        if continue_analysis.lower() != "y":
            print("退出程序")
            break


def main():
    """主函数"""
    # 解析命令行参数
    args = parse_arguments()
    
    # 如果没有提供命令行参数，进入交互模式
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    # 设置日志
    logger = setup_logging()
    
    # 获取资产类型和日期
    asset_type = args.asset
    target_date = args.date
    
    # 验证日期格式
    try:
        datetime.strptime(target_date, "%Y%m%d")
    except ValueError:
        print(f"错误：日期格式不正确，应为YYYYMMDD，例如20250307")
        return
    
    # 检查资产类型是否有效
    if asset_type not in ASSET_CONFIG:
        print(f"错误：无效的资产类型: {asset_type}")
        print(f"有效的资产类型: {', '.join(ASSET_CONFIG.keys())}")
        return
    
    # 获取资产名称
    asset_name = ASSET_CONFIG[asset_type]["asset_name"]
    
    print(f"开始获取{asset_name}相关新闻，日期: {target_date}...")
    logger.info(f"开始获取{asset_name}相关新闻，日期: {target_date}...")
    
    # 获取新闻数据
    if args.test:
        print(f"使用测试数据")
        logger.info(f"使用测试数据")
        news_items = generate_test_news(asset_type)
    else:
        news_items = fetch_news(asset_type, target_date, logger)
        
        # 如果没有找到新闻，使用测试数据
        if not news_items:
            print(f"没有找到真实新闻，使用测试数据")
            logger.warning(f"没有找到真实新闻，使用测试数据")
            news_items = generate_test_news(asset_type)
    
    print(f"新闻项数量: {len(news_items)}")
    logger.info(f"新闻项数量: {len(news_items)}")
    
    # 显示新闻标题
    print(f"\n获取到的{asset_name}相关新闻标题:")
    for i, item in enumerate(news_items, 1):
        print(f"{i}. {item.title} (来源: {item.source}, 情感分数: {item.alpha_sentiment:.2f})")
    
    print(f"\n{asset_name}新闻获取完成")
    logger.info(f"{asset_name}新闻获取完成")


if __name__ == "__main__":
    main() 
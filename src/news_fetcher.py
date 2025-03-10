"""
新闻获取模块 - 从Alpha Vantage API获取新闻数据
"""

import os
import sys
import json
import logging
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入配置和模型
from config.config import API_CONFIG, ASSET_CONFIG
from src.models import NewsItem


def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """
    设置日志
    
    Args:
        log_dir: 日志目录
        
    Returns:
        logging.Logger: 日志记录器
    """
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    
    # 配置日志
    logger = logging.getLogger("news_fetcher")
    logger.setLevel(logging.INFO)
    
    # 创建文件处理器
    file_handler = logging.FileHandler(
        os.path.join(log_dir, f'news_fetcher_{datetime.now().strftime("%Y%m%d")}.log'),
        encoding='utf-8'
    )
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    
    # 设置格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


def fetch_news(asset_type: str, target_date: Optional[str] = None, logger: Optional[logging.Logger] = None) -> List[NewsItem]:
    """
    获取特定资产类型的新闻
    
    Args:
        asset_type: 资产类型，如'oil', 'gold', 'stock', 'crypto', 'forex'
        target_date: 目标日期，格式为YYYYMMDD，如果为None则使用当前日期
        logger: 日志记录器，如果为None则创建新的
        
    Returns:
        List[NewsItem]: 新闻项列表
    """
    # 如果未提供日志记录器，创建一个
    if logger is None:
        logger = setup_logging()
    
    # 如果未指定日期，使用当前日期
    if target_date is None:
        target_date = datetime.now().strftime("%Y%m%d")
    
    # 检查资产类型是否有效
    if asset_type not in ASSET_CONFIG:
        logger.error(f"无效的资产类型: {asset_type}")
        return []
    
    # 获取资产配置
    asset_conf = ASSET_CONFIG[asset_type]
    keywords = asset_conf["keywords"]
    data_dir = os.path.join("data", asset_conf["data_dir"])
    asset_name = asset_conf["asset_name"]
    
    logger.info(f"获取{asset_name}相关新闻，日期: {target_date}")
    print(f"获取{asset_name}相关新闻，日期: {target_date}")
    
    # 创建数据目录
    os.makedirs(data_dir, exist_ok=True)
    
    api_key = API_CONFIG["alpha_vantage_api_key"]
    
    # 准备请求参数
    params = {
        "function": "NEWS_SENTIMENT",
        "apikey": api_key,
        "keywords": keywords,
        "sort": "RELEVANCE",
        "limit": 50
    }
    
    url = "https://www.alphavantage.co/query"
    
    try:
        # 发送请求
        response = requests.get(url, params=params)
        data = response.json()
        
        # 保存原始响应用于调试
        with open(os.path.join(data_dir, f"alpha_vantage_response_{datetime.now().strftime('%Y%m%d')}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 检查响应是否包含feed
        if "feed" not in data:
            logger.warning(f"响应中没有feed，可能是API密钥限制或关键词问题")
            print(f"响应中没有feed，可能是API密钥限制或关键词问题")
            return []
        
        # 提取新闻项
        news_items = []
        target_date_obj = datetime.strptime(target_date, "%Y%m%d")
        
        for item in data["feed"]:
            # 解析发布时间
            time_published = item.get("time_published", "")
            if time_published:
                try:
                    # 格式：YYYYMMDDTHHMMSS
                    news_date = datetime.strptime(time_published[:8], "%Y%m%d")
                    
                    # 检查新闻日期是否匹配目标日期
                    if news_date.date() == target_date_obj.date():
                        # 创建NewsItem
                        news_item = NewsItem(
                            title=item.get("title", ""),
                            original_title=item.get("title", ""),
                            content=item.get("summary", ""),
                            publish_time=time_published,
                            source=item.get("source", ""),
                            url=item.get("url", ""),
                            alpha_sentiment=float(item.get("overall_sentiment_score", 0.0))
                        )
                        news_items.append(news_item)
                except Exception as e:
                    logger.error(f"解析time_published时出错: {str(e)}")
                    continue
        
        logger.info(f"找到 {len(news_items)} 条日期为 {target_date} 的{asset_name}相关新闻")
        print(f"找到 {len(news_items)} 条日期为 {target_date} 的{asset_name}相关新闻")
        
        # 保存新闻数据
        news_file = os.path.join(data_dir, f"{asset_type}_news_{target_date}.json")
        with open(news_file, "w", encoding="utf-8") as f:
            json_data = [item.to_dict() for item in news_items]
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"新闻数据已保存到 {news_file}")
        print(f"新闻数据已保存到 {news_file}")
        
        return news_items
    
    except Exception as e:
        logger.error(f"获取{asset_name}新闻时出错: {str(e)}")
        print(f"获取{asset_name}新闻时出错: {str(e)}")
        return []


def generate_test_news(asset_type: str, count: int = 3) -> List[NewsItem]:
    """
    生成测试新闻数据
    
    Args:
        asset_type: 资产类型，如'oil', 'gold', 'stock', 'crypto', 'forex'
        count: 生成的新闻数量
        
    Returns:
        List[NewsItem]: 新闻项列表
    """
    print(f"生成{count}条{asset_type}测试新闻数据...")
    
    # 检查资产类型是否有效
    if asset_type not in ASSET_CONFIG:
        print(f"无效的资产类型: {asset_type}")
        return []
    
    # 获取资产配置
    asset_conf = ASSET_CONFIG[asset_type]
    asset_name = asset_conf["asset_name"]
    
    # 测试新闻模板
    news_templates = {
        "oil": [
            {
                "title": "OPEC+延长减产协议，油价小幅上涨",
                "content": "石油输出国组织及其盟友（OPEC+）周三宣布将延长减产协议至2025年底，以支撑油价。消息公布后，WTI原油期货价格上涨1.2%，达到每桶69.5美元，布伦特原油上涨1.0%，至每桶74.3美元。分析师表示，这一决定表明产油国对当前需求前景持谨慎态度。",
                "source": "Reuters",
                "sentiment": 0.35
            },
            {
                "title": "美国原油库存意外下降，市场供应趋紧",
                "content": "美国能源信息署(EIA)周二公布的数据显示，上周美国原油库存减少250万桶，而分析师此前预期增加100万桶。汽油库存也下降了180万桶。这一数据表明美国石油需求可能强于预期，推动WTI原油期货价格短线上涨2%。",
                "source": "Bloomberg",
                "sentiment": 0.42
            },
            {
                "title": "中国经济数据疲软，油价承压下行",
                "content": "中国国家统计局周一公布的数据显示，2月制造业PMI为49.5，连续第四个月处于收缩区间，表明全球第二大经济体和最大原油进口国的需求可能继续疲软。受此影响，国际油价下跌约1.5%，WTI原油跌至68美元/桶以下。",
                "source": "Financial Times",
                "sentiment": -0.28
            }
        ],
        "gold": [
            {
                "title": "美联储暗示年内降息，黄金价格创新高",
                "content": "美联储主席鲍威尔在最新讲话中暗示，如果通胀继续降温，可能在年内开始降息。受此消息影响，黄金期货价格上涨1.8%，突破每盎司2,100美元，创历史新高。分析师认为，低利率环境将继续支撑黄金价格。",
                "source": "Wall Street Journal",
                "sentiment": 0.65
            },
            {
                "title": "全球地缘政治紧张局势加剧，避险需求推动金价上涨",
                "content": "中东冲突持续升级，加上俄乌战争进入新阶段，全球地缘政治风险明显上升。投资者纷纷转向黄金等避险资产，推动金价在过去一周上涨2.5%，达到每盎司2,050美元。央行购金需求也保持强劲。",
                "source": "Reuters",
                "sentiment": 0.38
            },
            {
                "title": "印度黄金进口税下调，实物需求有望增加",
                "content": "印度财政部宣布将黄金进口税从12.5%下调至10%，以抑制走私并提振合法进口。作为全球第二大黄金消费国，印度的政策变化预计将刺激实物黄金需求，尤其是在即将到来的婚礼和节日季节。",
                "source": "Economic Times",
                "sentiment": 0.51
            }
        ],
        "stock": [
            {
                "title": "科技股领涨，纳斯达克指数创历史新高",
                "content": "受人工智能概念股强劲表现推动，纳斯达克综合指数上涨1.2%，创下历史新高。英伟达股价上涨3.5%，微软和谷歌母公司Alphabet分别上涨2.1%和1.8%。分析师表示，AI相关投资热潮仍在持续，科技巨头有望继续受益。",
                "source": "CNBC",
                "sentiment": 0.72
            },
            {
                "title": "美国就业数据强劲，市场对经济软着陆预期升温",
                "content": "美国劳工部公布的数据显示，上月非农就业人口增加22.5万人，失业率保持在3.7%的低位。这一数据好于经济学家预期，表明美国经济仍然保持韧性。受此影响，道琼斯工业平均指数上涨0.8%，标普500指数上涨0.6%。",
                "source": "Bloomberg",
                "sentiment": 0.58
            },
            {
                "title": "欧洲央行降息，欧洲股市普涨",
                "content": "欧洲央行宣布将基准利率下调25个基点，为三年来首次降息。此举旨在支持欧元区经济增长，同时认为通胀已得到有效控制。受此消息提振，泛欧Stoxx 600指数上涨1.5%，德国DAX指数和法国CAC 40指数分别上涨1.7%和1.6%。",
                "source": "Financial Times",
                "sentiment": 0.45
            }
        ],
        "crypto": [
            {
                "title": "比特币突破8万美元，创历史新高",
                "content": "比特币价格突破8万美元大关，创下历史新高。分析师认为，此轮上涨主要受到比特币ETF持续资金流入和即将到来的减半事件推动。机构投资者参与度明显提升，市场情绪乐观。以太坊等其他主要加密货币也跟随上涨。",
                "source": "CoinDesk",
                "sentiment": 0.81
            },
            {
                "title": "美国SEC批准以太坊ETF，加密市场迎来里程碑",
                "content": "美国证券交易委员会(SEC)批准了首批以太坊现货ETF，这被视为加密货币市场的重要里程碑。消息公布后，以太坊价格上涨12%，突破4,000美元。分析师表示，这一决定将为以太坊带来更多机构资金，并提高整个加密市场的合法性。",
                "source": "Bloomberg",
                "sentiment": 0.75
            },
            {
                "title": "多国央行加速CBDC研发，私人加密货币面临监管压力",
                "content": "据国际清算银行最新报告，全球已有超过80%的央行正在研究或开发中央银行数字货币(CBDC)。同时，多国监管机构加强了对私人加密货币的监管。市场担忧这可能对比特币等去中心化加密货币构成长期挑战，部分代币价格因此承压。",
                "source": "Reuters",
                "sentiment": -0.32
            }
        ],
        "forex": [
            {
                "title": "美元指数跌至九个月低点，非美货币普遍走强",
                "content": "美联储降息预期升温，美元指数下跌0.8%，跌至九个月低点。欧元兑美元上涨至1.12水平，英镑兑美元突破1.30关口，日元兑美元升值至140以下。分析师表示，美国与其他主要经济体的利差收窄是美元走弱的主要原因。",
                "source": "Reuters",
                "sentiment": -0.25
            },
            {
                "title": "中国央行出手稳定人民币，离岸人民币大幅反弹",
                "content": "中国人民银行通过多种渠道干预外汇市场，并上调人民币中间价，以遏制近期人民币贬值趋势。受此影响，离岸人民币兑美元汇率上涨近1%，创三个月最大单日涨幅。分析师认为，这表明中国当局不希望看到人民币快速贬值。",
                "source": "Bloomberg",
                "sentiment": 0.42
            },
            {
                "title": "日本央行暗示可能进一步收紧货币政策，日元大幅升值",
                "content": "日本央行行长植田和男在最新讲话中表示，如果通胀持续高于目标，将考虑进一步收紧货币政策。受此消息影响，日元兑美元汇率上涨1.5%，创六个月新高。分析师预计，日本可能在年内再次加息，结束长期超宽松货币政策。",
                "source": "Financial Times",
                "sentiment": 0.38
            }
        ]
    }
    
    # 获取当前时间
    now = datetime.now()
    current_time = now.strftime("%Y%m%dT%H%M%S")
    
    # 生成测试新闻
    news_items = []
    templates = news_templates.get(asset_type, [])
    
    # 如果没有找到对应资产类型的模板，使用通用模板
    if not templates and asset_type in ASSET_CONFIG:
        print(f"未找到{asset_type}的测试新闻模板，使用通用模板")
        templates = news_templates.get("stock", [])
    
    # 限制生成的新闻数量
    templates = templates[:count]
    
    for i, template in enumerate(templates):
        news_item = NewsItem(
            title=template["title"],
            original_title=template["title"],
            content=template["content"],
            publish_time=current_time,
            source=template["source"],
            url=f"https://example.com/news/{asset_type}/{i+1}",
            alpha_sentiment=template["sentiment"]
        )
        news_items.append(news_item)
    
    print(f"已生成 {len(news_items)} 条{asset_name}测试新闻数据")
    return news_items


def main():
    """主函数"""
    # 设置日志
    logger = setup_logging()
    
    # 检查命令行参数
    if len(sys.argv) > 2:
        # 如果提供了资产类型和日期参数
        asset_type = sys.argv[1].lower()
        target_date = sys.argv[2]
        
        # 验证日期格式
        try:
            datetime.strptime(target_date, "%Y%m%d")
            print(f"使用指定资产类型: {asset_type}, 日期: {target_date}")
        except ValueError:
            print(f"错误：日期格式不正确，应为YYYYMMDD，例如20250307")
            print(f"使用当前日期代替...")
            target_date = datetime.now().strftime("%Y%m%d")
    elif len(sys.argv) > 1:
        # 如果只提供了资产类型参数
        asset_type = sys.argv[1].lower()
        target_date = datetime.now().strftime("%Y%m%d")
        print(f"使用指定资产类型: {asset_type}, 当前日期: {target_date}")
    else:
        # 默认使用原油和当前日期
        asset_type = "oil"
        target_date = datetime.now().strftime("%Y%m%d")
        print(f"未指定参数，使用默认资产类型: {asset_type}, 当前日期: {target_date}")
    
    # 检查资产类型是否有效
    if asset_type not in ASSET_CONFIG:
        print(f"错误：无效的资产类型: {asset_type}")
        print(f"有效的资产类型: {', '.join(ASSET_CONFIG.keys())}")
        return
    
    # 获取资产名称
    asset_name = ASSET_CONFIG[asset_type]["asset_name"]
    
    print(f"开始获取{asset_name}相关新闻...")
    logger.info(f"开始获取{asset_name}相关新闻...")
    
    # 获取新闻数据
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
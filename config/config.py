"""
配置文件 - 包含API密钥和其他配置信息
"""

# API密钥
ALPHA_VANTAGE_API_KEY = "2KVNLYT4PWIH5WEZ"  # Alpha Vantage API密钥
DEEPSEEK_API_KEY = "sk-c8fbfadab4184b23b6122829ae44114d"  # DeepSeek API密钥

# API配置字典 - 用于导入
API_CONFIG = {
    "alpha_vantage_api_key": ALPHA_VANTAGE_API_KEY,
    "deepseek_api_key": DEEPSEEK_API_KEY
}

# 模型配置
MODEL_CONFIG = {
    "finGPT_params": {
        "model_path": "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # 使用开放访问的TinyLlama模型
        "max_length": 512,
        "temperature": 0.2,  # 控制输出稳定性
        "precision": "fp16"  # GPU推理优化
    },
    "use_ollama": True,  # 是否使用Ollama API
    "ollama_model": "fingpt"  # Ollama中的模型名称，使用我们创建的FinGPT模型
}

# 路径配置
LOGS_DIR = "logs"
DATA_DIR = "data"
REPORTS_DIR = "reports"

# 评分配置
SCORING_CONFIG = {
    "sentiment_weight": 0.6,  # 情绪分数权重
    "importance_weight": 0.4,  # 重要性分数权重
    "min_importance_threshold": 20.0,  # 最低重要性阈值
    "top_news_count": 10  # 保留的顶级新闻数量
}

# 系统配置
SYSTEM_CONFIG = {
    "retry_count": 3,  # API调用失败重试次数
    "retry_delay": 15,  # 重试间隔（秒）
    "news_timeout": 30,  # 单条新闻处理超时（秒）
    "batch_size": 8,  # 批处理大小
    "execution_time": "00:05"  # 每日执行时间（UTC）
}

# 标的配置
ASSET_CONFIG = {
    "oil": {
        "keywords": "oil,crude oil,petroleum,WTI,Brent,OPEC,barrel,energy,gasoline,fuel",
        "data_dir": "oil_data",
        "report_prefix": "oil_analysis",
        "asset_name": "原油",
        "asset_types": ["WTI", "BRENT"]
    },
    "gold": {
        "keywords": "gold,precious metal,bullion,XAU,ounce,troy,karat,carat,jewelry,mining",
        "data_dir": "gold_data",
        "report_prefix": "gold_analysis",
        "asset_name": "黄金",
        "asset_types": ["GOLD"]
    },
    "stock": {
        "keywords": "stock market,equity,shares,nasdaq,nyse,dow jones,s&p 500,index,etf,dividend",
        "data_dir": "stock_data",
        "report_prefix": "stock_analysis",
        "asset_name": "股票",
        "asset_types": ["STOCK"]
    },
    "crypto": {
        "keywords": "bitcoin,ethereum,cryptocurrency,blockchain,crypto,altcoin,token,defi,nft,mining",
        "data_dir": "crypto_data",
        "report_prefix": "crypto_analysis",
        "asset_name": "加密货币",
        "asset_types": ["BTC", "ETH"]
    },
    "forex": {
        "keywords": "forex,currency,exchange rate,USD,EUR,JPY,GBP,CHF,central bank,monetary policy",
        "data_dir": "forex_data",
        "report_prefix": "forex_analysis",
        "asset_name": "外汇",
        "asset_types": ["USD/EUR", "USD/JPY", "USD/GBP"]
    }
} 
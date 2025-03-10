# 市场新闻分析器 (Market News Analyzer)

一个功能强大的市场新闻分析工具，支持多种金融标的的新闻获取、分析和报告生成。

## 功能特点

- 支持多种金融标的：原油、黄金、股票、加密货币、外汇
- 从Alpha Vantage API获取实时新闻数据
- 提供测试数据模式，无需API密钥即可测试
- 交互式命令行界面，易于使用
- 支持命令行参数，方便自动化和脚本集成
- 生成详细的分析报告和Excel数据表格

## 安装

1. 克隆仓库：

```bash
git clone https://github.com/yourusername/MarketNewsAnalyzer.git
cd MarketNewsAnalyzer
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 使用方法

### 交互式模式

直接运行主程序，进入交互式模式：

```bash
python market_news_analyzer.py
```

在交互式模式中，您可以：
- 选择要分析的金融标的（原油、黄金、股票等）
- 选择要分析的日期（今天、昨天或指定日期）
- 查看获取到的新闻标题和情感分数

### 命令行模式

您也可以使用命令行参数直接运行：

```bash
python market_news_analyzer.py -a oil -d 20250307
```

参数说明：
- `-a, --asset`：要分析的资产类型（默认：oil）
  - 可选值：oil, gold, stock, crypto, forex
- `-d, --date`：要分析的日期，格式为YYYYMMDD（默认：当前日期）
- `-t, --test`：使用测试数据而不是真实数据
- `-o, --output`：输出目录（默认：data）
- `-v, --verbose`：显示详细输出

### 示例

1. 分析今天的原油新闻：

```bash
python market_news_analyzer.py -a oil
```

2. 分析指定日期的黄金新闻：

```bash
python market_news_analyzer.py -a gold -d 20250307
```

3. 使用测试数据分析股票新闻：

```bash
python market_news_analyzer.py -a stock -t
```

## 目录结构

```
MarketNewsAnalyzer/
├── config/             # 配置文件
│   └── config.py       # 主配置文件
├── data/               # 数据目录
│   ├── oil_data/       # 原油数据
│   ├── gold_data/      # 黄金数据
│   └── ...
├── logs/               # 日志目录
├── src/                # 源代码
│   ├── models.py       # 数据模型
│   ├── news_fetcher.py # 新闻获取模块
│   └── ...
├── market_news_analyzer.py  # 主程序
└── README.md           # 说明文档
```

## 配置

在 `config/config.py` 文件中，您可以：
- 设置API密钥
- 配置不同标的的关键词和参数
- 调整评分和分析参数

## 依赖项

- Python 3.8+
- requests
- xlsxwriter
- argparse

## 许可证

MIT 

## 模型文件

本项目使用FinGPT模型进行金融文本分析。由于模型文件较大（约2GB），未包含在Git仓库中。

### 模型详情

- **模型名称**：FinGPT-v3.1-chat
- **模型类型**：基于LLaMA-7B微调的金融领域大语言模型
- **模型大小**：约2GB
- **支持语言**：中英双语
- **主要功能**：金融文本分析、情感分析、市场趋势预测

### 获取模型方法

#### 方法一：使用下载脚本（推荐）

项目提供了自动下载脚本，运行以下命令：

```bash
python scripts/download_models.py
```

此脚本会自动从Hugging Face下载模型并放置在正确的目录中。

#### 方法二：手动下载

1. 从以下链接下载模型文件：
   - [Hugging Face](https://huggingface.co/THUDM/chatglm-6b-v1/tree/main)
   - [百度网盘](https://pan.baidu.com/s/1vEMXKr5aCM80jmxj2nTvnA) 提取码：1234

2. 下载后，将模型文件放置在以下目录：
   ```
   MarketNewsAnalyzer/models/fingpt-v3.1-chat/
   ```

3. 确保目录结构如下：
   ```
   models/
   └── fingpt-v3.1-chat/
       ├── config.json
       ├── pytorch_model.bin
       ├── tokenizer_config.json
       └── tokenizer.model
   ```

#### 方法三：使用在线API（无需下载模型）

如果您不想下载模型，可以修改配置使用在线API：

1. 编辑 `config/config.py` 文件
2. 将 `USE_LOCAL_MODEL` 设置为 `False`
3. 设置您的API密钥：`API_KEY = "您的密钥"`

### 模型使用注意事项

- 模型需要至少8GB内存才能正常运行
- 首次加载模型可能需要1-2分钟
- GPU加速可显著提高分析速度

## 项目结构

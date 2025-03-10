"""
数据模型 - 定义新闻项和价格项的类
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class NewsItem:
    """新闻项类"""
    title: str
    original_title: str
    content: str
    publish_time: str
    source: str
    url: str
    alpha_sentiment: float = 0.0
    summary: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "title": self.title,
            "original_title": self.original_title,
            "content": self.content,
            "summary": self.summary or self.content[:200] + "..." if len(self.content) > 200 else self.content,
            "publish_time": self.publish_time,
            "source": self.source,
            "url": self.url,
            "alpha_sentiment": self.alpha_sentiment
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NewsItem':
        """从字典创建实例"""
        return cls(
            title=data.get("title", ""),
            original_title=data.get("original_title", data.get("title", "")),
            content=data.get("content", ""),
            summary=data.get("summary", ""),
            publish_time=data.get("publish_time", ""),
            source=data.get("source", ""),
            url=data.get("url", ""),
            alpha_sentiment=float(data.get("alpha_sentiment", 0.0))
        )


@dataclass
class PriceItem:
    """价格项类"""
    date: str
    price: float
    asset_type: str
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "date": self.date,
            "price": self.price,
            "asset_type": self.asset_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PriceItem':
        """从字典创建实例"""
        return cls(
            date=data.get("date", ""),
            price=float(data.get("price", 0.0)),
            asset_type=data.get("asset_type", "")
        )


@dataclass
class NewsScore:
    """新闻评分类"""
    title: str
    sentiment_score: float
    impact_score: float
    relevance_score: float = 0.8
    summary: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "title": self.title,
            "sentiment_score": self.sentiment_score,
            "impact_score": self.impact_score,
            "relevance_score": self.relevance_score,
            "summary": self.summary
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'NewsScore':
        """从字典创建实例"""
        return cls(
            title=data.get("title", ""),
            sentiment_score=float(data.get("sentiment_score", 0.0)),
            impact_score=float(data.get("impact_score", 0.0)),
            relevance_score=float(data.get("relevance_score", 0.8)),
            summary=data.get("summary", "")
        )


@dataclass
class AnalysisReport:
    """分析报告类"""
    title: str
    date: str
    asset_name: str
    market_overview: str
    news_summary: str
    market_analysis: str
    conclusion: str
    generation_time: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    
    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        return f"""**{self.asset_name}市场分析报告**  
**标题：{self.title}**  
**日期：{self.date}**  

---

### **正文分析**  

#### **1. 市场概览**  
{self.market_overview}

#### **2. 重要新闻摘要**  
{self.news_summary}

#### **3. 市场分析**  
{self.market_analysis}

---

### **结论**  
{self.conclusion}

---  
**（报告生成时间：{self.generation_time}）**"""
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "title": self.title,
            "date": self.date,
            "asset_name": self.asset_name,
            "market_overview": self.market_overview,
            "news_summary": self.news_summary,
            "market_analysis": self.market_analysis,
            "conclusion": self.conclusion,
            "generation_time": self.generation_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnalysisReport':
        """从字典创建实例"""
        return cls(
            title=data.get("title", ""),
            date=data.get("date", ""),
            asset_name=data.get("asset_name", ""),
            market_overview=data.get("market_overview", ""),
            news_summary=data.get("news_summary", ""),
            market_analysis=data.get("market_analysis", ""),
            conclusion=data.get("conclusion", ""),
            generation_time=data.get("generation_time", datetime.now().strftime("%Y-%m-%d"))
        ) 
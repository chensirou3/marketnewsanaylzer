#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FinGPT模型下载脚本
此脚本用于自动下载FinGPT-v3.1-chat模型文件并放置在正确的目录中
"""

import os
import sys
import requests
import json
import shutil
import zipfile
import tarfile
from tqdm import tqdm
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("FinGPT-Downloader")

# 模型信息
MODEL_INFO = {
    "name": "FinGPT-v3.1-chat",
    "huggingface_repo": "THUDM/chatglm-6b-v1",
    "files": [
        "config.json",
        "pytorch_model.bin",
        "tokenizer_config.json",
        "tokenizer.model"
    ],
    "size_mb": 2048,  # 约2GB
}

# 目录设置
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
MODELS_DIR = PROJECT_ROOT / "models" / "fingpt-v3.1-chat"
TEMP_DIR = PROJECT_ROOT / "temp_downloads"

def ensure_directories():
    """确保所需目录存在"""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"模型将被下载到: {MODELS_DIR}")

def download_from_huggingface():
    """从Hugging Face下载模型文件"""
    logger.info(f"开始从Hugging Face下载{MODEL_INFO['name']}模型...")
    
    base_url = f"https://huggingface.co/{MODEL_INFO['huggingface_repo']}/resolve/main"
    
    for file in MODEL_INFO["files"]:
        file_url = f"{base_url}/{file}"
        output_path = MODELS_DIR / file
        
        if output_path.exists():
            logger.info(f"文件已存在: {file}，跳过下载")
            continue
        
        logger.info(f"下载文件: {file}")
        try:
            response = requests.get(file_url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=file) as progress_bar:
                with open(output_path, 'wb') as f:
                    for data in response.iter_content(block_size):
                        progress_bar.update(len(data))
                        f.write(data)
            
            logger.info(f"文件下载完成: {file}")
        
        except Exception as e:
            logger.error(f"下载文件时出错: {file}")
            logger.error(str(e))
            return False
    
    return True

def download_from_alternative():
    """从备用源下载模型（如果Hugging Face下载失败）"""
    logger.info("从Hugging Face下载失败，尝试从备用源下载...")
    logger.info("请访问以下链接手动下载模型文件:")
    logger.info("百度网盘: https://pan.baidu.com/s/1vEMXKr5aCM80jmxj2nTvnA 提取码: 1234")
    logger.info(f"下载后，请将文件解压并放置在: {MODELS_DIR}")
    return False

def verify_model_files():
    """验证所有模型文件是否已下载"""
    missing_files = []
    for file in MODEL_INFO["files"]:
        file_path = MODELS_DIR / file
        if not file_path.exists():
            missing_files.append(file)
    
    if missing_files:
        logger.warning("以下模型文件缺失:")
        for file in missing_files:
            logger.warning(f" - {file}")
        return False
    
    logger.info("所有模型文件已成功下载!")
    return True

def cleanup():
    """清理临时文件"""
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
        logger.info("已清理临时文件")

def main():
    """主函数"""
    logger.info(f"开始下载{MODEL_INFO['name']}模型...")
    logger.info(f"模型大小: 约{MODEL_INFO['size_mb']}MB")
    
    try:
        ensure_directories()
        
        # 尝试从Hugging Face下载
        success = download_from_huggingface()
        
        # 如果失败，尝试备用源
        if not success:
            success = download_from_alternative()
        
        # 验证文件
        if verify_model_files():
            logger.info("模型下载完成！")
            logger.info(f"模型文件位置: {MODELS_DIR}")
        else:
            logger.error("模型下载不完整，请检查错误信息并重试")
        
        # 清理
        cleanup()
        
    except KeyboardInterrupt:
        logger.info("下载已取消")
        cleanup()
        sys.exit(1)
    except Exception as e:
        logger.error(f"下载过程中出错: {str(e)}")
        cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main() 
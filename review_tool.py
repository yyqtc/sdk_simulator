from langchain.tools import tool

import json
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

config = json.load(open("./config.json", "r", encoding="utf-8"))

@tool
def write_opinion_file(content: str) -> str:
    """
    写入审核员意见文件的内容

    Args:
        content: 文件的内容
    
    Returns:
        返回字符串“文件写入成功”
    """
    logger.info("use write_opinion_file tool")
    with open(config["OPINION_FILE_PATH"], "w+", encoding="utf-8") as f:
        f.write(content)

    return "文件写入成功"

@tool
def read_opinion_file() -> str:
    """
    读取审核员意见文件的内容

    Args:
        无
    
    Returns:
        如果文件不存在，返回“文件不存在”
        如果文件存在且扩展名是.md，返回文件的内容
    """
    logger.info("use read_opinion_file tool")
    if not os.path.exists(config["OPINION_FILE_PATH"]):
        return "文件不存在"
    
    with open(config["OPINION_FILE_PATH"], "r", encoding="utf-8") as f:
        return f.read()

@tool
def read_sdk_use_doc() -> str:
    """
    读取sdk的使用文档

    Args:
        无
    
    Returns:
        如果文件不存在，返回“文件不存在”
        如果文件存在且扩展名是.md，返回文件的内容
    """
    logger.info("use read_sdk_use_doc tool")
    if not os.path.exists(config["USE_DOC_PATH"]):
        return "文件不存在"
    
    with open(config["USE_DOC_PATH"], "r", encoding="utf-8") as f:
        return f.read()

@tool
def read_sdk_file() -> str:
    """
    读取sdk文件的内容

    Args:
        无
    
    Returns:
        如果文件不存在，返回“文件不存在”
        如果文件存在且扩展名是.py，返回文件的内容
    """
    logger.info("use read_sdk_file tool")
    if not os.path.exists(config["SDK_FILE_PATH"]):
        return "文件不存在"
    
    with open(config["SDK_FILE_PATH"], "r", encoding="utf-8") as f:
        return f.read()

tools = [read_sdk_use_doc, read_sdk_file, write_opinion_file, read_opinion_file]

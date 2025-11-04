from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from custom_type import ActionReview
from executor_tool import tools

import json
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

def init_agent():
    _model = ChatOpenAI(
        model="qwen-plus",
        openai_api_key=config["QWEN_API_KEY"],
        openai_api_base=config["QWEN_API_BASE"],
        temperature=0.7
    )

    _prompt = f"""
        你是一位非常专业的软件开发工程师，我需要你根据sdk的使用文档，写一个模拟sdk的{config["SDK_LANGUAGE"]}文件。
        注意！
        你必须把模拟sdk以文件形式保存到系统。
        你必须把你做了那些修改以注释的形式体现在模拟sdk的{config["SDK_LANGUAGE"]}文件中。
        如果需要生成一张图片，这张图片必须是白色的纯色图片。
        如果需要调用网络接口，模拟延时然后直接返回静态数据即可，不要真的去调用网络接口！
        模拟sdk尽量做到简单易用，用户可以即插即用。
    """

    agent = create_agent(
        model=_model,
        system_prompt=_prompt,
        tools=tools
    )

    return agent

agent = init_agent()

async def execute_node(state: ActionReview) -> ActionReview:
    count = 0
    if "count" in state:
        count = state["count"]
    
    logger.info("正在创建模拟sdk的文件...")

    if count == 0:
        user_prompt = """
        请根据sdk的使用文档，写一个模拟sdk的文件。
        注意！
        1. sdk中的api必须完全符合sdk的使用文档的说明。
        2. sdk的使用文档中描述的所有api都必须在模拟sdk的文件中实现。
        """
        response = await agent.ainvoke({
            "messages": [("user", user_prompt)]
        })

        return {
            "count": count
        }
    else: 
        user_prompt = """
            请根据sdk的使用文档和审核员的意见，修改模拟sdk的文件。
            注意！
            1. sdk中的api必须完全符合sdk的使用文档的说明。
            2. sdk的使用文档中描述的所有api都必须在模拟sdk的文件中实现。
            3. 你不能忽视审核员的意见，必须根据审核员的意见修改模拟sdk的文件。
        """

        response = await agent.ainvoke({
            "messages": [("user", user_prompt)]
        })

        return {
            "count": count
        }

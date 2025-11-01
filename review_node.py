from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from custom_type import ActionReview, Action, Response, Act
from review_tool import tools

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

    _prompt = """
        你是一位非常负责的审核员，我需要你根据sdk的使用文档检查模拟sdk的js文件。
    """

    agent = create_agent(
        model=_model,
        system_prompt=_prompt,
        tools=tools,
        response_format=Act
    )

    return agent

agent = init_agent()


async def review_node(state: ActionReview) -> ActionReview:
    count = 0
    if "count" in state:
        count = state["count"]
    
    logger.info("正在审核SDK代码是否符合使用文档的说明...")

    if count == 0:
        user_prompt = f"""
        当前你正在进行第{count + 1}轮审核。
        请根据sdk的使用文档，检查模拟sdk的js文件是否符合sdk的使用文档的说明。
        如果你认为模拟sdk符合sdk的使用文档的说明，就审核通过，并结束修改模拟sdk。
        如果你认为模拟sdk不符合sdk的使用文档的说明，就需要你将你的检查结果以审核员意见文件的形式保存，并让前端工程师继续修改模拟sdk。
        如果你认为模拟sdk不需要进一步修改，请以JSON格式输出，包含action字段，action字段应该包含response字段，response字段的值为“审核通过”。
        如果你认为模拟sdk需要进一步修改，请以JSON格式输出，包含action字段，action字段应该包含count字段，count字段的数据类型为整数，count字段的值为当前审核轮数加1。
        注意！
        1. sdk中的api应该完全符合sdk的使用文档的说明。
        2. sdk的使用文档中描述的所有api都必须在模拟sdk的js文件中实现。
        3. 模拟sdk应该是可以正常运行的，不能存在语法错误或逻辑错误。
        4. 意见中不要包括图片文件或是图片的base64编码
        """
        response = await agent.ainvoke({
            "messages": [("user", user_prompt)]
        })

        response = response["structured_response"]

        if isinstance(response.action, Action):
            return {
                "count": response.action.count - 1
            }
        
        elif isinstance(response.action, Response):
            return {
                "response": response.action.response
            }

    else:
        user_prompt = f"""
        当前你正在进行第{count + 1}轮审核。
        请根据sdk的使用文档和上一轮的审核意见，检查模拟sdk的js文件是否符合sdk的使用文档的说明，并检查sdk文档是否已经修复了上一轮的审核提出的问题。
        如果你认为模拟sdk符合sdk的使用文档的说明，就审核通过，并结束修改模拟sdk。
        如果你认为模拟sdk不符合sdk的使用文档的说明，就需要你将你的检查结果以审核员意见文件的形式保存，并让前端工程师继续修改模拟sdk。
        如果你认为模拟sdk不需要进一步修改，请以JSON格式输出，包含action字段，action字段应该包含response字段，response字段的值为“审核通过”。
        如果你认为模拟sdk需要进一步修改，请以JSON格式输出，包含action字段，action字段应该包含count字段，count字段的数据类型为整数，count字段的值为当前审核轮数加1。
        注意！
        1. sdk中的api应该完全符合sdk的使用文档的说明。
        2. sdk的使用文档中描述的所有api都必须在模拟sdk的js文件中实现。
        3. 模拟sdk应该是可以正常运行的，不能存在语法错误或逻辑错误。
        """
        response = await agent.ainvoke({
            "messages": [("user", user_prompt)]
        })

        response = response["structured_response"]
        if isinstance(response.action, Action):
            return {
                "count": response.action.count - 1
            }
        
        elif isinstance(response.action, Response):
            return {
                "response": response.action.response
            }
    

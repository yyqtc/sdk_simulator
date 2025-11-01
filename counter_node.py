from __future__ import annotations

from custom_type import ActionReview
from langgraph.graph import END
from typing import Union

import json
import logging

config = json.load(open("./config.json", "r", encoding="utf-8"))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def counter_node(state: ActionReview) -> Union[ActionReview, END]:
    if config["HUMAN_REVIEW_THRESHOLD"] == 0:
        logger.info("请你检查配置，将HUMAN_REVIEW_THRESHOLD设置为大于0的值，否则工作流将无法正常进行。")
        return {
            "response": "error"
        }

    count = 0
    if "count" in state:
        count = state["count"]
    
    logger.info(f"counter_node count: {count + 1}")
    
    if "response" in state and len(state["response"]) > 0:
        return {
            "response": state["response"]
        }

    if count == max(config["HUMAN_REVIEW_THRESHOLD"] - 1, 0):
        user_input = input(f"请你检查{config["SDK_FILE_PATH"]}是否符合sdk的使用文档的说明。如果符合，请输入“pass”。如果不符合，请输入“reject”：")
        if user_input == "pass":
            return {
                "response": "pass"
            }

        else:
            check_input = input(f"请检查审核意见{config["OPINION_FILE_PATH"]}。如果你认为没有必要继续修改，请输入“pass”。如果你认为有必要继续修改，请输入“reject”：")
            if check_input == "pass":
                return {
                    "response": "pass"
                }
            else:
                return {
                    "count": 0
                }

    else:
        if count != 0:
            check_input = input(f"请检查审核意见{config["OPINION_FILE_PATH"]}。如果你认为没有必要继续修改，请输入“pass”。如果你认为有必要继续修改，请输入“reject”：")
            if check_input == "pass":
                return {
                    "response": "pass"
                }
            else:
                return {
                    "count": count
                }

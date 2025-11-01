from langgraph.graph import StateGraph, START, END
from custom_type import ActionReview
from counter_node import counter_node
from review_node import review_node
from execute_node import execute_node

import asyncio

def _should_end(state: ActionReview):
    if "response" in state and len(state["response"]) > 0:
        return END
    else:
        return "execute"

async def main():
    workflow = StateGraph(ActionReview)
    workflow.add_node("counter", counter_node)
    workflow.add_node("review", review_node)
    workflow.add_node("execute", execute_node)

    workflow.add_edge(START, "counter")
    workflow.add_conditional_edges("counter", _should_end, ["execute", END])
    workflow.add_edge("execute", "review")
    workflow.add_edge("review", "counter")

    app = workflow.compile()

    result = await app.ainvoke({
        "count": 0
    })

    print("result: ", result)

if __name__ == "__main__":
    asyncio.run(main())

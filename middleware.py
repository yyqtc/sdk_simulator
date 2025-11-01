from langchain.agents.middleware import wrap_model_call

# 开发降级中间件，当大模型请求失败时，将state中所有信息脱敏，然后在拿到返回结果后，将脱敏信息还原
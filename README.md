# SDK Simulator

这是一个SDK模拟器项目，用于根据SDK使用文档自动生成和审核模拟SDK代码。

## 项目功能

1. **自动生成SDK**：根据提供的SDK使用文档自动生成模拟SDK代码
2. **智能审核**：自动检查生成的SDK是否符合使用文档的要求
3. **迭代优化**：根据审核意见不断优化SDK代码
4. **人工介入**：支持在特定轮次进行人工审核

## 项目结构

```
sdk_simulator/
├── main.py              # 主程序入口，定义工作流
├── custom_type.py       # 自定义数据类型定义
├── counter_node.py      # 计数器节点，控制流程
├── review_node.py       # 审核节点，检查SDK代码
├── execute_node.py      # 执行节点，生成/修改SDK代码
├── review_tool.py       # 审核工具集
├── executor_tool.py     # 执行工具集
├── middleware.py        # 中间件（预留）
├── config.default.json  # 默认配置文件
├── sdk/                 # SDK文件存放目录
├── md/                  # 文档存放目录
└── opinion/             # 审核意见存放目录
```

## 安装说明

1. 克隆项目代码
2. 安装依赖包

```bash
pip install -r requirement.txt
```

3. 复制配置文件并填入必要配置

```bash
cp config.default.json config.json
```

## 使用方法

1. 在`md/`目录下准备SDK使用文档
2. 配置`config.json`文件中的必要参数
3. 运行主程序

```bash
python main.py
```

## 配置说明

`config.json`文件需要包含以下配置项：

- `SDK_FILE_PATH`: SDK文件路径
- `USE_DOC_PATH`: SDK使用文档路径
- `OPINION_FILE_PATH`: 审核意见文件路径
- `HUMAN_REVIEW_THRESHOLD`: 人工审核触发轮次
- `QWEN_API_KEY`: 文心一言API密钥
- `QWEN_API_BASE`: 文心一言API基础地址

## 工作流程

1. 初始化工作流
2. 执行计数器节点，确定是否需要人工审核
3. 执行节点生成或修改SDK代码
4. 审核节点检查SDK代码
5. 根据审核结果决定是否需要再次迭代

## 注意事项

- 确保提供的SDK使用文档格式规范
- 配置文件中的路径需要使用相对路径
- 人工审核时请仔细检查SDK是否符合文档要求
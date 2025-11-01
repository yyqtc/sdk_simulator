# SDK 模拟器

一个基于 LangGraph 和 AI 代理的 SDK 模拟代码自动生成工具。该工具能够根据 SDK 使用文档自动生成对应的 JavaScript 模拟 SDK 文件，并通过多轮审核迭代机制确保生成代码的质量和准确性。

## 功能特性

- 🤖 **AI 驱动生成**：使用 Qwen 模型自动根据 SDK 使用文档生成模拟 SDK 代码
- 🔄 **迭代优化机制**：通过执行-审核-修正的循环流程，不断优化生成的 SDK
- 👤 **人工审核集成**：在达到指定审核轮次后，支持人工介入审核
- 📝 **自动意见管理**：审核员可以将修改意见保存到文件，开发者根据意见进行修正
- 🛠️ **灵活的工具系统**：提供文件读写、文档解析等工具，支持完整的开发流程

## 项目结构

```
sdk_simulator/
├── main.py                 # 主程序入口，定义工作流
├── counter_node.py         # 计数器节点，管理审核轮次和人工审核
├── execute_node.py         # 执行节点，AI 代理生成/修改 SDK 代码
├── review_node.py          # 审核节点，AI 代理审核 SDK 代码
├── executor_tool.py        # 执行器工具集（读取文档、读写 SDK 文件等）
├── review_tool.py          # 审核器工具集（读写审核意见文件等）
├── custom_type.py          # 自定义类型定义
├── config.json             # 配置文件（需要根据 config.default.json 创建）
├── config.default.json     # 配置文件模板
├── requirement.txt         # Python 依赖包列表
├── md/                     # SDK 使用文档目录
│   ├── sdk.md             # SDK 使用文档
│   └── img/               # 文档图片资源
├── sdk/                    # 生成的 SDK 文件目录
│   └── sim_sdk.js         # 模拟 SDK JavaScript 文件
└── opinion/                # 审核意见目录
    └── opinion.md         # 审核员意见文件
```

## 工作流程

项目使用 LangGraph 构建了一个状态图工作流，流程如下：

```
START → counter → execute → review → counter → ...
         ↓                    ↓
        END ←───────────────┘
```

1. **counter（计数器节点）**：
   - 管理审核轮次计数
   - 当达到人工审核阈值时，提示用户进行人工审核
   - 如果审核通过，流程结束

2. **execute（执行节点）**：
   - 如果是第一轮（count=0）：根据 SDK 使用文档生成模拟 SDK 文件
   - 如果是后续轮次：根据 SDK 使用文档和审核意见修改 SDK 文件
   - 使用 AI 代理（前端开发工程师角色）执行代码生成/修改

3. **review（审核节点）**：
   - AI 代理（审核员角色）检查生成的 SDK 是否符合使用文档
   - 如果不符合，将审核意见写入意见文件，继续下一轮修改
   - 如果符合，返回审核通过，流程结束

## 安装与配置

### 1. 安装依赖

```bash
pip install -r requirement.txt
```

### 2. 配置文件

复制配置文件模板并填入相应信息：

```bash
cp config.default.json config.json
```

编辑 `config.json`，配置以下参数：

```json
{
    "LANGCHAIN_API_KEY": "your-langchain-api-key",           // LangChain API Key
    "QWEN_API_KEY": "your-qwen-api-key",                     // 阿里云 Qwen API Key
    "QWEN_API_BASE": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "USE_DOC_PATH": "./md/sdk.md",                           // SDK 使用文档路径
    "SDK_FILE_PATH": "./sdk/sim_sdk.js",                     // 生成的 SDK 文件路径
    "OPINION_FILE_PATH": "./opinion/opinion.md",             // 审核意见文件路径
    "HUMAN_REVIEW_THRESHOLD": 3                              // 人工审核阈值（第几轮后触发）
}
```

### 3. 准备 SDK 使用文档

将 SDK 使用文档放置在 `md/sdk.md`（或配置文件中指定的路径）。

## 使用方法

运行主程序：

```bash
python main.py
```

程序将自动执行以下流程：

1. 读取 SDK 使用文档
2. AI 代理生成模拟 SDK 代码
3. AI 审核员检查代码
4. 根据审核意见进行修正（如需要）
5. 重复步骤 3-4，直到审核通过或达到人工审核阈值
6. 人工审核（如触发）
7. 输出最终结果

### 交互提示

在运行过程中，可能会遇到以下交互提示：

- **人工审核提示**：当达到 `HUMAN_REVIEW_THRESHOLD` 轮次时，会提示你检查 SDK 文件，输入 `pass` 表示通过，`reject` 表示拒绝
- **检查审核意见提示**：在每轮审核后，会提示你检查审核员意见文件，按回车继续

## 依赖说明

- `langgraph==1.0.1`：工作流状态图框架
- `langchain==1.0.2`：LLM 应用开发框架
- `langchain_openai==0.3.32`：OpenAI 兼容的 LLM 接口
- `pydantic==2.11.7`：数据验证和类型定义
- `typing_extensions==4.14.1`：类型扩展支持

## 工具说明

### 执行器工具（executor_tool.py）

- `read_sdk_use_doc()`：读取 SDK 使用文档
- `read_sdk_file()`：读取生成的 SDK 文件
- `write_sdk_file(content)`：写入 SDK 文件内容
- `read_opinion_file()`：读取审核意见文件

### 审核器工具（review_tool.py）

- `read_sdk_use_doc()`：读取 SDK 使用文档
- `read_sdk_file()`：读取生成的 SDK 文件
- `write_opinion_file(content)`：写入审核意见
- `read_opinion_file()`：读取审核意见文件

## 注意事项

1. **API 密钥安全**：请妥善保管 API 密钥，不要将包含真实密钥的 `config.json` 提交到版本控制系统
2. **文档格式**：确保 SDK 使用文档格式清晰，包含完整的 API 说明
3. **生成代码验证**：AI 生成的代码建议进行人工验证，特别是在生产环境使用前
4. **图片生成**：生成的图片为白色纯色图片（符合模拟 SDK 的要求）

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 更新日志

### v0.1.0
- 初始版本发布
- 支持基于文档的 SDK 自动生成
- 实现多轮审核迭代机制
- 集成人工审核功能


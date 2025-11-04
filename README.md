# SDK 模拟器

一个基于 LangGraph 和 AI 代理的 SDK 模拟代码自动生成工具。该工具能够根据 SDK 使用文档自动生成对应的 JavaScript 模拟 SDK 文件，并通过多轮审核迭代机制确保生成代码的质量和准确性。

## 功能特性

- 🤖 **AI 驱动生成**：使用 Qwen 模型自动根据 SDK 使用文档生成模拟 SDK 代码
- 🔄 **迭代优化机制**：通过执行-审核-修正的循环流程，不断优化生成的 SDK
- 👤 **人工审核集成**：每轮审核后支持人工介入决策是否继续迭代
- 📝 **自动意见管理**：审核员可以将修改意见保存到文件，开发者根据意见进行修正
- 🛠️ **灵活的工具系统**：提供文件读写、文档解析、历史文件管理等工具，支持完整的开发流程
- 📚 **历史版本追踪**：自动保存每轮修改前的 SDK 版本到历史文件

## 项目结构

```
sdk_simulator/
├── main.py                 # 主程序入口，定义工作流
├── counter_node.py         # 计数器节点，管理审核轮次和人工审核
├── execute_node.py         # 执行节点，AI 代理生成/修改 SDK 代码
├── review_node.py          # 审核节点，AI 代理审核 SDK 代码
├── executor_tool.py        # 执行器工具集（读取文档、读写 SDK 文件、历史文件等）
├── review_tool.py          # 审核器工具集（读写审核意见文件等）
├── custom_type.py          # 自定义类型定义
├── config.json             # 配置文件（需要根据 config.default.json 创建）
├── config.default.py       # 配置文件模板
├── requirement.txt         # Python 依赖包列表
├── md/                     # SDK 使用文档目录
│   ├── sdk.md             # SDK 使用文档
│   └── img/               # 文档图片资源
├── sdk/                    # 生成的 SDK 文件目录
│   └── sim_sdk.py         # 模拟 SDK JavaScript 文件
├── opinion/                # 审核意见目录
│   └── opinion.md         # 审核员意见文件
└── history/                # 历史版本目录（自动创建）
    └── history_sim_sdk.py  # 历史版本 SDK 文件
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
   - 如果已有审核通过响应，直接结束流程
   - 如果 count != 0（非第一轮），提示用户检查审核意见文件，由用户决定是否继续
   - 在继续之前，将当前 SDK 文件备份到历史文件路径
   - 返回当前的 count 值继续流程

2. **execute（执行节点）**：
   - 如果是第一轮（count=0）：根据 SDK 使用文档生成模拟 SDK 文件
   - 如果是后续轮次：根据 SDK 使用文档和审核意见修改 SDK 文件
   - 使用 AI 代理（软件开发工程师角色）执行代码生成/修改
   - AI 代理会将所做的修改以注释形式体现在 SDK 文件中
   - 如果需要生成图片，会生成白色纯色图片

3. **review（审核节点）**：
   - AI 代理（审核员角色）检查生成的 SDK 是否符合使用文档
   - 使用结构化输出（Act 类型）来决定下一步行动
   - 如果不符合，将审核意见写入意见文件，返回新的 count 值继续下一轮修改
   - 如果符合，返回审核通过响应，流程将在 counter 节点结束

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
    "SDK_FILE_PATH": "./sdk/sim_sdk.py",                     // 生成的 SDK 文件路径
    "OPINION_FILE_PATH": "./opinion/opinion.md",             // 审核意见文件路径
    "HISTORY_FILE_PATH": "./history/history_sim_sdk.py"      // 历史版本文件路径（自动备份）
}
```

**注意**：请确保 `history/` 目录存在，或者在首次运行前创建该目录。

### 3. 准备 SDK 使用文档

将 SDK 使用文档放置在 `md/sdk.md`（或配置文件中指定的路径）。

## 使用方法

运行主程序：

```bash
python main.py
```

程序将自动执行以下流程：

1. 从 `counter` 节点开始，初始化 count=0
2. 进入 `execute` 节点，AI 代理根据 SDK 使用文档生成模拟 SDK 代码
3. 进入 `review` 节点，AI 审核员检查代码是否符合使用文档
4. 如果审核通过，返回审核通过响应，流程在 `counter` 节点结束
5. 如果审核不通过，审核员将意见写入意见文件，返回新的 count 值
6. 返回 `counter` 节点，如果 count != 0，会提示用户检查审核意见
7. 用户输入 `pass` 或 `reject` 决定是否继续迭代
8. 如果继续，备份当前 SDK 文件到历史路径，然后重复步骤 2-7
9. 直到审核通过或用户选择停止，输出最终结果

### 交互提示

在运行过程中，可能会遇到以下交互提示：

- **检查审核意见提示**：从第二轮（count != 0）开始，每轮审核后都会提示：
  ```
  请检查审核意见{OPINION_FILE_PATH}。如果你认为没有必要继续修改，请输入"pass"。如果你认为有必要继续修改，请输入"reject"：
  ```
  - 输入 `pass`：结束流程，使用当前版本
  - 输入 `reject`：继续下一轮迭代修改

## 依赖说明

- `langgraph==1.0.1`：工作流状态图框架
- `langchain==1.0.2`：LLM 应用开发框架
- `langchain_openai==0.3.32`：OpenAI 兼容的 LLM 接口
- `pydantic==2.11.7`：数据验证和类型定义
- `typing_extensions==4.14.1`：类型扩展支持

## 工具说明

### 执行器工具（executor_tool.py）

执行节点使用的工具集，供 AI 开发代理使用：

- `read_sdk_use_doc()`：读取 SDK 使用文档内容
- `read_sdk_file()`：读取当前生成的 SDK 文件内容
- `write_sdk_file(content)`：写入/覆盖 SDK 文件内容
- `read_opinion_file()`：读取审核员意见文件内容
- `read_history_file()`：读取历史版本的 SDK 文件内容（上一轮修改前的版本）

### 审核器工具（review_tool.py）

审核节点使用的工具集，供 AI 审核代理使用：

- `read_sdk_use_doc()`：读取 SDK 使用文档内容
- `read_sdk_file()`：读取当前生成的 SDK 文件内容
- `write_opinion_file(content)`：写入审核意见到意见文件
- `read_opinion_file()`：读取审核员意见文件内容

## 注意事项

1. **API 密钥安全**：请妥善保管 API 密钥，不要将包含真实密钥的 `config.json` 提交到版本控制系统
2. **文档格式**：确保 SDK 使用文档格式清晰，包含完整的 API 说明
3. **生成代码验证**：AI 生成的代码建议进行人工验证，特别是在生产环境使用前
4. **图片生成**：生成的图片为白色纯色图片（符合模拟 SDK 的要求）
5. **历史文件管理**：每轮修改前，当前 SDK 文件会自动备份到 `HISTORY_FILE_PATH`，请确保该路径所在目录存在
6. **修改追踪**：AI 开发代理会在生成的 SDK 文件中以注释形式记录所做的修改，便于追踪变更

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 技术实现细节

### 状态管理

使用 `ActionReview` TypedDict 管理工作流状态：
- `count`：当前审核轮次（整数）
- `response`：审核通过响应（字符串）

### 决策机制

审核节点使用结构化输出（`Act` Pydantic 模型）来控制流程：
- `Action`：包含 `count` 字段，表示需要继续下一轮修改
- `Response`：包含 `response` 字段，值为"审核通过"，表示流程结束

### 工作流控制

- `_should_end()` 函数检查状态中是否有 `response` 字段，如果有则结束流程
- counter 节点负责检查状态，决定是继续执行还是结束
- 每轮迭代都会备份 SDK 文件，便于回滚和对比

## 更新日志

### v0.2.0
- 初始版本发布
- 支持基于文档的 SDK 自动生成
- 实现多轮审核迭代机制
- 集成人工审核功能
- 支持历史版本备份
- 支持修改注释追踪


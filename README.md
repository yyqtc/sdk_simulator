# SDK 模拟器（Mock SDK Generator）

⚠️ **重要说明**：本项目生成的是 **模拟 SDK（Mock SDK/测试桩）**，用于开发测试和模拟真实 SDK 的行为，**并非真实的、可连接实际 API 的 SDK**。

一个基于 LangGraph 和 AI 代理的 **多语言模拟 SDK 代码自动生成工具**。该工具能够根据 SDK 使用文档自动生成对应**任意编程语言**的模拟 SDK 文件（Python、JavaScript、TypeScript、Java、Go、Rust 等），这些生成的代码是**测试桩（Stub/Mock）**，用于模拟真实 SDK 的接口和行为，便于开发和测试，并通过多轮审核迭代机制确保生成代码的质量和准确性。

## 功能特性

- 🌍 **多语言支持**：✨ **核心亮点** - 支持生成任意编程语言的 **模拟 SDK（Mock SDK/测试桩）**（Python、JavaScript、TypeScript、Java、Go、Rust、C#、PHP 等），只需通过配置文件指定目标语言和文件扩展名
- 🤖 **AI 驱动生成**：使用 Qwen 模型自动根据 SDK 使用文档生成模拟 SDK 代码（测试桩代码）
- 🔄 **迭代优化机制**：通过执行-审核-修正的循环流程，不断优化生成的模拟 SDK
- 👤 **人工审核集成**：每轮审核后支持人工介入决策是否继续迭代
- 📝 **自动意见管理**：审核员可以将修改意见保存到文件，开发者根据意见进行修正
- 🛠️ **灵活的工具系统**：提供文件读写、文档解析、历史文件管理等工具，支持完整的开发流程
- 📚 **历史版本追踪**：自动保存每轮修改前的模拟 SDK 版本到历史文件

⚠️ **再次提醒**：生成的代码是**模拟/测试桩**，不会真实调用 API，主要用于：
- 开发和测试环境的接口模拟
- 前端开发时的后端接口 Mock
- 单元测试和集成测试的测试桩
- 学习和理解 SDK API 设计的参考

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
├── config.default.json     # 配置文件模板
├── requirement.txt         # Python 依赖包列表
├── md/                     # SDK 使用文档目录（用户提供）
│   └── img/               # 文档图片资源（可选）
├── sdk/                    # 生成的 SDK 文件目录（自动生成，不会被版本控制）
│   └── [生成的 SDK 文件]   # 根据配置生成对应语言的 SDK 文件
├── opinion/                # 审核意见目录（自动生成，不会被版本控制）
│   └── [审核意见文件]      # 审核过程中自动生成的意见文件
└── history/                # 历史版本目录（自动创建，不会被版本控制）
    └── [历史版本文件]      # 每轮修改前自动备份的 SDK 文件
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
   - 如果是第一轮（count=0）：根据 SDK 使用文档生成**模拟 SDK（测试桩）**文件
   - 如果是后续轮次：根据 SDK 使用文档和审核意见修改模拟 SDK 文件
   - 使用 AI 代理（软件开发工程师角色）执行代码生成/修改
   - 🌍 **智能语言识别**：AI 会根据文件扩展名和 `SDK_LANGUAGE` 配置自动识别目标语言，生成符合该语言语法和最佳实践的**模拟代码（Mock Code）**
   - AI 代理会将所做的修改以注释形式体现在模拟 SDK 文件中
   - 如果需要生成图片，会生成白色纯色图片（模拟数据）

3. **review（审核节点）**：
   - AI 代理（审核员角色）检查生成的**模拟 SDK（测试桩）**是否符合使用文档
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
    "LANGCHAIN_API_KEY": "your-langchain-api-key",
    "QWEN_API_KEY": "your-qwen-api-key",
    "QWEN_API_BASE": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "USE_DOC_PATH": "./md/your-sdk-document.md",
    "SDK_FILE_PATH": "./sdk/your-sdk-name.[ext]",
    "OPINION_FILE_PATH": "./opinion/your-opinion.md",
    "HISTORY_FILE_PATH": "./history/your-history.[ext]",
    "SDK_LANGUAGE": "python"
}
```

**参数说明**：
- `USE_DOC_PATH`: SDK 使用文档路径（用户提供）
- `SDK_FILE_PATH`: 生成的 SDK 文件路径，`[ext]` 为文件扩展名（如 `.py`, `.js`, `.ts` 等）
- `OPINION_FILE_PATH`: 审核意见文件路径（自动生成）
- `HISTORY_FILE_PATH`: 历史版本文件路径（自动备份），建议与 `SDK_FILE_PATH` 使用相同的扩展名
- `SDK_LANGUAGE`: 目标语言（可选，AI 会根据文件扩展名自动识别）

### 🌍 多语言配置示例

**核心优势**：通过修改 `SDK_FILE_PATH` 的文件扩展名和 `SDK_LANGUAGE`，即可生成不同编程语言的 SDK！

#### Python SDK
```json
{
    "SDK_FILE_PATH": "./sdk/your_sdk.py",
    "HISTORY_FILE_PATH": "./history/your_sdk_history.py",
    "SDK_LANGUAGE": "python"
}
```

#### JavaScript SDK
```json
{
    "SDK_FILE_PATH": "./sdk/your_sdk.js",
    "HISTORY_FILE_PATH": "./history/your_sdk_history.js",
    "SDK_LANGUAGE": "javascript"
}
```

#### TypeScript SDK
```json
{
    "SDK_FILE_PATH": "./sdk/your_sdk.ts",
    "HISTORY_FILE_PATH": "./history/your_sdk_history.ts",
    "SDK_LANGUAGE": "typescript"
}
```

#### Java SDK
```json
{
    "SDK_FILE_PATH": "./sdk/YourSDK.java",
    "HISTORY_FILE_PATH": "./history/YourSDKHistory.java",
    "SDK_LANGUAGE": "java"
}
```

#### Go SDK
```json
{
    "SDK_FILE_PATH": "./sdk/your_sdk.go",
    "HISTORY_FILE_PATH": "./history/your_sdk_history.go",
    "SDK_LANGUAGE": "go"
}
```

#### Rust SDK
```json
{
    "SDK_FILE_PATH": "./sdk/your_sdk.rs",
    "HISTORY_FILE_PATH": "./history/your_sdk_history.rs",
    "SDK_LANGUAGE": "rust"
}
```

**注意**：
- 请确保 `history/` 目录存在，或者在首次运行前创建该目录
- AI 会根据文件扩展名自动识别目标语言，`SDK_LANGUAGE` 参数可选，用于明确指定语言风格和最佳实践
- 支持所有主流编程语言，只需修改文件扩展名即可！

### 3. 准备 SDK 使用文档

将**真实 SDK 的使用文档**放置在配置文件中指定的 `USE_DOC_PATH` 路径（例如 `md/your-sdk-document.md`）。本工具会根据这份文档生成对应的**模拟 SDK（测试桩）**。文档应包含：
- SDK 的 API 接口说明
- 使用示例和代码片段
- 参数说明和返回值描述
- 任何特殊配置或要求

**注意**：生成的模拟 SDK 会模拟这些接口的行为，但不会真实调用 API。

## 使用方法

运行主程序：

```bash
python main.py
```

程序将自动执行以下流程：

1. 从 `counter` 节点开始，初始化 count=0
2. 进入 `execute` 节点，AI 代理根据 SDK 使用文档生成**模拟 SDK（测试桩）**代码
3. 进入 `review` 节点，AI 审核员检查生成的模拟代码是否符合使用文档
4. 如果审核通过，返回审核通过响应，流程在 `counter` 节点结束
5. 如果审核不通过，审核员将意见写入意见文件，返回新的 count 值
6. 返回 `counter` 节点，如果 count != 0，会提示用户检查审核意见
7. 用户输入 `pass` 或 `reject` 决定是否继续迭代
8. 如果继续，备份当前模拟 SDK 文件到历史路径，然后重复步骤 2-7
9. 直到审核通过或用户选择停止，输出最终的模拟 SDK 文件

⚠️ **提醒**：生成的代码是模拟/测试桩，不会真实连接 API 或执行实际的网络请求。

### 交互提示

在运行过程中，可能会遇到以下交互提示：

- **检查审核意见提示**：从第二轮（count != 0）开始，每轮审核后都会提示：
  ```
  请检查审核意见文件。如果你认为没有必要继续修改，请输入"pass"。如果你认为有必要继续修改，请输入"reject"：
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

## 🌍 多语言 SDK 生成

### 核心亮点

**本项目最大的特色是支持生成任意编程语言的 SDK！** 你只需要：

1. 修改配置文件中的 `SDK_FILE_PATH` 为对应语言的扩展名
2. （可选）设置 `SDK_LANGUAGE` 参数指定目标语言
3. 运行 `python main.py`，AI 会自动生成符合目标语言语法和最佳实践的 SDK 代码

### 支持的语言

- ✅ **Python** (`.py`) - 支持类、函数、类型提示等
- ✅ **JavaScript** (`.js`) - 支持 ES6+、模块化、Promise 等
- ✅ **TypeScript** (`.ts`) - 支持类型系统、接口、泛型等
- ✅ **Java** (`.java`) - 支持类、接口、泛型、注解等
- ✅ **Go** (`.go`) - 支持包、结构体、接口、错误处理等
- ✅ **Rust** (`.rs`) - 支持所有权、生命周期、模式匹配等
- ✅ **C#** (`.cs`) - 支持类、命名空间、LINQ 等
- ✅ **PHP** (`.php`) - 支持类、命名空间、类型提示等
- ✅ **更多语言** - 理论上支持所有编程语言，AI 会根据文档和语言特性自动适配

### 使用生成的模拟 SDK

⚠️ **重要**：生成的代码是**模拟 SDK（Mock SDK/测试桩）**，用于开发和测试，**不会真实调用 API**。

生成的模拟 SDK 文件位于配置文件中指定的 `SDK_FILE_PATH`。根据不同的语言，使用方式如下：

#### Python 模拟 SDK
```python
# 假设 SDK_FILE_PATH = "./sdk/your_sdk.py"
# ⚠️ 这是模拟 SDK，不会真实调用 API
from sdk.your_sdk import YourSDKClass

sdk = YourSDKClass()
result = sdk.some_method("参数")  # 返回模拟数据，不会真实请求
```

#### JavaScript 模拟 SDK
```javascript
// 假设 SDK_FILE_PATH = "./sdk/your_sdk.js"
// ⚠️ 这是模拟 SDK，不会真实调用 API
const { YourSDKClass } = require('./sdk/your_sdk');

const sdk = new YourSDKClass();
const result = sdk.someMethod("参数");  // 返回模拟数据
```

#### TypeScript 模拟 SDK
```typescript
// 假设 SDK_FILE_PATH = "./sdk/your_sdk.ts"
// ⚠️ 这是模拟 SDK，不会真实调用 API
import { YourSDKClass } from './sdk/your_sdk';

const sdk = new YourSDKClass();
const result = sdk.someMethod("参数");  // 返回模拟数据
```

#### Java 模拟 SDK
```java
// 假设 SDK_FILE_PATH = "./sdk/YourSDK.java"
// ⚠️ 这是模拟 SDK，不会真实调用 API
import com.example.your_sdk.YourSDKClass;

YourSDKClass sdk = new YourSDKClass();
Result result = sdk.someMethod("参数");  // 返回模拟数据
```

#### Go 模拟 SDK
```go
// 假设 SDK_FILE_PATH = "./sdk/your_sdk.go"
// ⚠️ 这是模拟 SDK，不会真实调用 API
import "github.com/example/your_sdk"

sdk := your_sdk.NewYourSDKClass()
result, err := sdk.SomeMethod("参数")  // 返回模拟数据
```

**重要说明**：
- ⚠️ **生成的代码是模拟/测试桩，不会真实调用 API**
- ⚠️ **所有网络请求都是模拟的，返回的是模拟数据**
- ⚠️ **仅用于开发、测试、学习和理解 SDK 接口设计**
- ⚠️ **不要在生产环境中使用生成的模拟 SDK 替代真实 SDK**
- AI 会根据目标语言的特性自动生成符合该语言习惯的代码风格和最佳实践
- 生成的模拟 SDK 可能需要特定的环境变量（如 API key），但这些配置仅用于模拟，不会真实使用

## 注意事项

### ⚠️ 重要警告

1. **这不是真实的 SDK**：本项目生成的是**模拟 SDK（Mock SDK/测试桩）**，用于开发和测试，**不会真实调用 API**。所有网络请求都是模拟的，返回的是模拟数据。

2. **不要在生产环境使用**：生成的模拟 SDK **仅用于开发、测试、学习和理解 SDK 接口设计**，**不要在生产环境中使用生成的模拟 SDK 替代真实 SDK**。

3. **用途说明**：生成的模拟 SDK 适用于：
   - ✅ 开发和测试环境的接口模拟
   - ✅ 前端开发时的后端接口 Mock
   - ✅ 单元测试和集成测试的测试桩
   - ✅ 学习和理解 SDK API 设计的参考
   - ❌ **不适用于生产环境的真实 API 调用**

### 其他注意事项

4. **API 密钥安全**：请妥善保管 API 密钥，不要将包含真实密钥的 `config.json` 提交到版本控制系统

5. **文档格式**：确保 SDK 使用文档格式清晰，包含完整的 API 说明

6. **生成代码验证**：AI 生成的模拟代码建议进行人工验证，确保符合预期

7. **图片生成**：生成的图片为白色纯色图片（符合模拟 SDK 的要求）

8. **历史文件管理**：每轮修改前，当前模拟 SDK 文件会自动备份到 `HISTORY_FILE_PATH`，请确保该路径所在目录存在

9. **修改追踪**：AI 开发代理会在生成的模拟 SDK 文件中以注释形式记录所做的修改，便于追踪变更

10. **环境变量**：生成的模拟 SDK 可能需要特定的环境变量（如 API key），但这些配置仅用于模拟，不会真实使用

11. **WSL 环境**：如果在 WSL 环境下使用生成的模拟 SDK，请注意环境变量的设置需要在 WSL 的 shell 配置文件中进行（如 `~/.bashrc` 或 `~/.zshrc`），因为 Windows 和 WSL 的环境变量是隔离的

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

### v0.3.0
- 🎉 初始版本发布
- 🌍 **核心功能**：支持生成任意编程语言的**模拟 SDK（Mock SDK/测试桩）**（Python、JavaScript、TypeScript、Java、Go、Rust、C#、PHP 等）
- ⚠️ **重要说明**：生成的代码是模拟/测试桩，不会真实调用 API，仅用于开发、测试和学习
- 支持基于文档的模拟 SDK 自动生成
- 实现多轮审核迭代机制
- 集成人工审核功能
- 支持历史版本备份
- 支持修改注释追踪
- 支持通过配置文件自定义生成的模拟 SDK 文件路径和语言类型
- AI 自动识别目标语言并生成符合该语言最佳实践的模拟代码


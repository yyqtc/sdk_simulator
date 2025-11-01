# SDK Simulator

这是一个基于LangChain和LangGraph构建的智能SDK模拟器项目，能够根据SDK使用文档自动生成、审核和迭代优化模拟SDK代码。项目采用了多节点工作流架构，结合AI模型能力实现自动化SDK开发流程。

## 项目功能

1. **自动SDK生成**：根据提供的SDK使用文档自动生成符合规范的JavaScript模拟SDK代码
2. **智能代码审核**：利用AI模型自动检查生成的SDK是否严格符合使用文档要求
3. **多轮迭代优化**：根据审核意见自动修改和优化SDK代码
4. **人机协作机制**：支持在特定迭代轮次自动触发人工审核流程
5. **状态化工作流**：基于LangGraph实现的状态管理，确保流程稳定可控

## 项目结构

```
sdk_simulator/
├── main.py              # 主程序入口，定义LangGraph工作流
├── custom_type.py       # 自定义数据类型和状态定义
├── counter_node.py      # 计数器节点，控制迭代次数和人工审核触发
├── review_node.py       # 审核节点，调用AI模型审核SDK代码
├── execute_node.py      # 执行节点，调用AI模型生成/修改SDK代码
├── review_tool.py       # 审核工具集，提供文件读写和文档访问功能
├── executor_tool.py     # 执行工具集，提供SDK文件生成和访问功能
├── config.default.json  # 默认配置文件模板
├── config.json          # 实际配置文件（需自行创建）
├── sdk/                 # SDK文件存放目录
├── md/                  # SDK使用文档存放目录
├── opinion/             # 审核意见存放目录
├── requirement.txt      # 项目依赖配置
└── LICENSE              # 项目许可证文件
```

## 安装说明

1. 确保安装Python 3.8+
2. 克隆项目代码
3. 安装依赖包

```bash
pip install -r requirement.txt
```

4. 复制配置文件并填入必要配置

```bash
cp config.default.json config.json
```

## 使用方法

1. 在`md/`目录下准备SDK使用文档（Markdown格式）
2. 配置`config.json`文件中的必要参数
3. 运行主程序

```bash
python main.py
```

4. 每次审核意见文件生成后，都会提示用户检查审核意见文件，确保sdk生成符合用户预期
5. 程序运行过程中，当达到设定的人工审核轮次时，会提示进行人工确认

## 配置说明

`config.json`文件需要包含以下配置项：

```json
{
  "SDK_FILE_PATH": "./sdk/simulated_sdk.js",
  "USE_DOC_PATH": "./md/sdk_documentation.md",
  "OPINION_FILE_PATH": "./opinion/review_opinion.md",
  "HUMAN_REVIEW_THRESHOLD": 3,
  "QWEN_API_KEY": "your_api_key_here",
  "QWEN_API_BASE": "your_api_base_url_here"
}
```

- `SDK_FILE_PATH`: 生成的SDK文件保存路径
- `USE_DOC_PATH`: SDK使用文档的路径
- `OPINION_FILE_PATH`: 审核意见文件的保存路径
- `HUMAN_REVIEW_THRESHOLD`: 触发人工审核的迭代轮次阈值
- `QWEN_API_KEY`: 千问大模型API密钥
- `QWEN_API_BASE`: 千问大模型API基础地址

## 技术栈

- **Python 3.8+**: 主要开发语言
- **LangGraph**: 状态管理和工作流控制
- **LangChain**: LLM应用开发框架
- **ChatOpenAI (Qwen)**: 用于代码生成和审核的LLM接口
- **Pydantic**: 数据类型验证（通过typing_extensions使用）

## 详细工作流程

1. **初始化阶段**
   - 程序加载配置文件
   - 初始化LangGraph状态管理工作流
   - 注册三个核心节点：counter、execute和review

2. **迭代循环阶段**
   - **计数器节点**：检查迭代次数，决定是继续迭代还是触发人工审核
   - **执行节点**：根据SDK文档和当前迭代状态，调用AI模型生成或修改SDK代码
   - **审核节点**：调用AI模型审核生成的SDK代码，生成审核意见，决定是否通过或继续优化

3. **终止条件**
   - 人工审核通过
   - AI审核自动通过
   - 达到设定的最大迭代次数（通过HUMAN_REVIEW_THRESHOLD控制）

## 工具函数说明

项目实现了两类主要工具集：

1. **执行工具** (`executor_tool.py`)
   - `read_sdk_use_doc()`: 读取SDK使用文档
   - `read_sdk_file()`: 读取当前SDK文件
   - `write_sdk_file()`: 写入新的SDK代码
   - `read_opinion_file()`: 读取审核意见文件

2. **审核工具** (`review_tool.py`)
   - `write_opinion_file()`: 写入审核意见
   - `read_sdk_use_doc()`: 读取SDK使用文档
   - `read_sdk_file()`: 读取当前SDK文件
   - `read_opinion_file()`: 读取审核意见文件

## 注意事项

- 确保提供的SDK使用文档格式规范且内容完整
- 配置文件中的路径需要使用相对路径，基于项目根目录
- API密钥信息请妥善保管，避免泄露
- 人工审核时请仔细检查SDK是否符合文档要求
- 程序运行过程中需要保持网络连接，以便调用AI模型API

## 常见问题

1. **API调用失败**：请检查API密钥和基础地址是否正确
2. **文件读写错误**：确认目录权限和路径设置是否正确
3. **审核意见生成异常**：可能是SDK文档格式不规范，请检查文档内容

## 许可证

该项目采用MIT许可证，详情请参阅LICENSE文件。
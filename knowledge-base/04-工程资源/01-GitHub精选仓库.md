# GitHub 精选仓库

GitHub 上直接以 FDE 命名的高质量资料不多，真正有用的内容分散在 Agent、评测、观测、安全、隐私和发布工具里。本页只做导航和使用判断，不复制第三方代码。许可证和依赖会变化，商用前打开仓库再次确认。

## 开始构建

### OpenAI Cookbook

[openai/openai-cookbook](https://github.com/openai/openai-cookbook) 收录 API、Agent、检索和评测样例，适合快速验证一个薄切片。项目采用 MIT License。FDE 可以先找与任务最接近的样例，再把身份、数据、业务评测和运行控制补齐。Cookbook 证明 API 怎样使用，不证明方案满足客户生产要求。

### OpenAI Agents SDK for Python

[openai/openai-agents-python](https://github.com/openai/openai-agents-python) 提供 Agent、handoff、guardrail、session 和 tracing 等基础能力。适合需要工具调用和多步骤编排的项目。先用单 Agent 跑通任务，只有不同角色确实需要独立提示、工具和责任时才加 handoff。

### Claude Cookbooks

[anthropics/claude-cookbooks](https://github.com/anthropics/claude-cookbooks) 包含提示、RAG、工具和 Agent 工作流示例。`patterns/agents` 展示 prompt chaining、routing、parallelization、orchestrator workers 和 evaluator optimizer。样例适合学习结构，真实项目仍要加入权限、预算、Trace 和失败处理。

### MCP Servers

[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) 提供 MCP 参考服务器和社区服务器入口。FDE 可以用它理解资源、工具和传输方式。社区服务器获得了系统访问能力后会成为供应链和权限边界，采用前要检查维护者、权限、凭据处理、日志和发布版本。

## 评测与回归

### OpenAI Evals

[openai/evals](https://github.com/openai/evals) 是 LLM 与 LLM 系统评测框架和公开注册表。它适合学习数据集、eval 定义和评分结构。OpenAI 的平台 Evals 已经发展，旧仓库与新 API 的关系需要按当前文档确认。客户数据不应未经授权进入公开注册表。

### Promptfoo

[promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) 适合在本地和 CI 比较提示、模型与 Agent，并做红队测试。FDE 可以把高风险样本和历史事故放进发布门禁。配置文件里不要硬编码密钥，模型评分器要用人工样本校准。

### Garak

[NVIDIA/garak](https://github.com/NVIDIA/garak) 用探针检查提示注入、泄露、越狱和其他 LLM 风险。扫描适合扩大攻击覆盖，结果可能有误报和漏报。项目团队仍要根据业务工具、权限和数据设计自己的攻击链。

## 观测与调试

### Langfuse

[langfuse/langfuse](https://github.com/langfuse/langfuse) 提供 Trace、提示版本、数据集、评测和成本观测。适合快速建立 Agent 调试闭环。自托管不自动等于合规，团队仍要定义正文是否记录、谁能访问、保留多久和怎样删除个人数据。

### Arize Phoenix

[Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) 使用 OpenTelemetry 支持 LLM Trace、评测和实验。适合已经有 Python 或 OpenTelemetry 体系的团队。上线前检查采集器、导出端点和敏感字段，不要把完整客户文档默认写进 span。

### OpenTelemetry Specification

[open-telemetry/opentelemetry-specification](https://github.com/open-telemetry/opentelemetry-specification) 是跨服务 Trace、Metric 和 Log 的基础规范。FDE 项目可以沿用现有观测体系，再添加模型、提示、检索、工具和人工接管字段。字段要稳定，不能把所有调试正文都当属性保存。

## 隐私、安全与发布控制

### Microsoft Presidio

[microsoft/presidio](https://github.com/microsoft/presidio) 提供个人信息识别和匿名化组件。它可以进入数据导入、日志和评测准备流程。不同语言、行业编号和地址格式会影响误差，必须用客户数据样本测试，不能把默认模型当完整脱敏保证。

### Unleash

[Unleash/unleash](https://github.com/Unleash/unleash) 提供功能开关和渐进发布能力。FDE 可以按客户、用户、风险或地区灰度，事故时关闭特定工具而不必停止整个应用。开关本身需要权限、审计和默认安全状态。

### LiteLLM

[BerriAI/litellm](https://github.com/BerriAI/litellm) 提供多模型接口、代理、预算和路由。它能降低调用层切换成本，模型行为仍不会因此一致。切换供应商前要跑任务评测、工具调用、错误语义、速率限制和数据处理检查。

## 平台接入

### Palantir Foundry Python SDK

[palantir/foundry-platform-python](https://github.com/palantir/foundry-platform-python) 提供 Foundry API 的 Python 接口。学习 Skywise 或医院案例时，它能帮助理解平台对象如何进入代码。它只适用于相应平台，不应为了模仿 FDE 而强行引入。

## 两个社区 FDE 项目

[davidahmann/fde-guide](https://github.com/davidahmann/fde-guide) 试图把价值、架构、评测、安全和运营组合成完整 FDE 指南。[thecoder8890/forward-deployed-engineer-roadmap](https://github.com/thecoder8890/forward-deployed-engineer-roadmap) 偏职业学习路径。两者可作选题和结构参考，核心事实仍应回到官方岗位、客户案例和技术文档。社区仓库的维护状态与内容质量需要逐页判断。

## 按项目阶段选工具

| 阶段 | 可以先看 | 仍需自己完成 |
| --- | --- | --- |
| 原型 | OpenAI Cookbook、Claude Cookbooks | 用户任务、真实数据入口和价值基线 |
| Agent | Agents SDK、MCP Servers | 工具权限、状态、人工控制和异常路径 |
| 评测 | OpenAI Evals、Promptfoo | 领域样本、阈值、专家量表和生产指标 |
| 观测 | Langfuse、Phoenix、OpenTelemetry | 敏感数据、保留、告警和事件责任 |
| 安全 | Garak、Presidio | 业务威胁模型、权限与红队判定 |
| 发布 | Unleash、LiteLLM | 灰度策略、回滚、供应商故障和成本边界 |

## 采用前检查

1. 仓库是否仍活跃，最近版本和安全公告是什么。
2. 许可证是否允许你的修改、托管和商业分发方式。
3. 代码会把数据发到哪里，默认日志记录什么。
4. 凭据和服务账号需要哪些权限。
5. 失败时会重试、降级还是静默跳过。
6. 团队能否在不依赖原作者的情况下运营。

开源项目缩短实现时间，不能替客户承担系统责任。

# 附录　FDE 工具包

## 附录 A　业务访谈问题清单

### 任务事实

- 请用最近一次真实案例带我走完整个过程。
- 谁触发任务？完成的定义是什么？
- 输入来自哪些系统、文件和人？
- 哪些步骤需要判断，依据是什么？
- 最常见与最昂贵的异常分别是什么？
- 任务完成后，结果写回哪里？谁会使用？

### 时间与价值

- 每周发生多少次？平均与最慢耗时是多少？
- 哪个角色的时间最稀缺？
- 错误、延迟和遗漏分别造成什么后果？
- 如果时间减少一半，释放的能力会用于什么？

### 权限与控制

- 哪些数据敏感？谁可以读取和写入？
- 哪些动作不可逆或需要审批？
- 发生错误时如何发现、暂停和恢复？
- 哪些法规、行业规则或内部政策适用？

### 采用与变化

- 用户现在为什么采用现有绕法？
- 新系统会增加或减少哪些步骤？
- 谁可能因职责或指标变化而抵触？
- 谁能成为试点冠军用户？

## 附录 B　用例优先级评分表

每项 1-5 分，并记录证据。没有流程所有者、数据来源不合法或风险无法控制时直接暂停，不以总分覆盖否决项。

| 维度 | 1 分 | 3 分 | 5 分 |
|---|---|---|---|
| 业务价值 | 影响不明 | 有局部节省 | 影响关键指标 |
| 频率规模 | 低频个例 | 稳定重复 | 高频大规模 |
| AI 适配度 | 规则足够 | 部分非结构化 | AI 显著解除瓶颈 |
| 数据准备度 | 无法获得 | 需治理接入 | 合法、可用、可评测 |
| 风险可控度 | 不可逆且难检测 | 可人工复核 | 可检测、可回退 |
| 所有者投入 | 无负责人 | 有支持但资源弱 | 有权决策并投入用户 |

## 附录 C　一页价值契约

**目标用户与任务：**  
**当前流程与基线：**  
**价值假设：**  
**目标业务指标：**  
**不可恶化指标：**  
**试点范围与周期：**  
**数据与系统依赖：**  
**评测方法与最低阈值：**  
**高风险动作与控制：**  
**业务结果负责人：**  
**暂停/退出条件：**  
**下一次决策日期：**

## 附录 D　项目范围与交付契约

1. 问题陈述与成功指标。
2. 本期必须、手工支撑、延期和不做范围。
3. 客户与交付团队的直接负责人。
4. 数据、环境、账号和审批的提供日期。
5. 每周工作节奏、演示和决策会议。
6. 风险台账与升级路径。
7. 变更如何影响时间、资源和质量。
8. 上线、回滚、支持与交接条件。

## 附录 E　AI 系统架构审查

- 用户与服务身份是否清晰，是否继承源系统权限？
- 模型、提示、工具、索引和策略是否版本化？
- 确定性逻辑是否被不必要地交给模型？
- 写操作是否幂等、可预览、可确认、可审计？
- 外部内容是否按不可信输入处理？
- 是否存在完整 Trace，同时控制敏感日志？
- 超时、重试、预算、终止和降级路径是否明确？
- 模型或供应商切换的边界和代价是否被记录？

## 附录 F　Evals 设计模板

**任务与用户：**  
**业务成功标准：**  
**风险分级：**  
**数据来源与时间范围：**  
**常见/边界/高风险/历史失败样本：**  
**开发集与保留集划分：**  
**确定性评分器：**  
**专家量表与分歧处理：**  
**模型评分器及人工校准：**  
**成本与时延预算：**  
**关键切片最低阈值：**  
**回归触发条件：**  
**失败如何进入下一版本：**

## 附录 G　上线与安全检查清单

### 上线前

- 业务负责人签认指标、范围和责任。
- 核心评测与关键风险切片达标。
- 完成提示词注入、越权、数据泄露和工具滥用测试。
- 身份、权限、租户隔离、日志和保留期通过审查。
- 性能、并发、成本和外部依赖压测完成。
- 高风险动作的人工确认与最小权限生效。
- 灰度、暂停、回滚、降级和数据恢复演练完成。
- 用户培训、支持入口与事故值班明确。

### 上线后

- 观察任务成功、采用、人工接管、风险和业务指标。
- 每周审查新增失败样本并更新分类。
- 模型、提示、索引、工具变更触发回归。
- 定期复查权限、供应链和知识时效。
- 重大事件进入事故复盘和产品反馈闭环。

## 附录 H　生产事故复盘模板

**事件摘要与影响：**  
**开始、发现、缓解、恢复时间：**  
**受影响用户、任务与数据：**  
**事实时间线：**  
**直接技术原因：**  
**系统与组织促成因素：**  
**为什么控制未提前发现：**  
**临时缓解和永久修复：**  
**负责人、截止时间与验证方式：**  
**新增评测/告警/流程：**  
**需要反馈给产品或供应商的内容：**

## 附录 I　FDE 能力自评

对六个维度按 1-5 分评分，并为每项附一条项目证据。1 分表示只能在指导下完成，3 分表示能独立交付，5 分表示能处理高复杂度并教会团队。

| 能力维度 | 当前分 | 项目证据 | 下一步实践 |
|---|---:|---|---|
| 工程实现 |  |  |  |
| AI 系统 |  |  |  |
| 产品发现 |  |  |  |
| 业务判断 |  |  |  |
| 交付领导 |  |  |  |
| 沟通影响 |  |  |  |

## 附录 J　作品集项目模板

**一句话问题：**  
**真实用户证据：**  
**现状流程与基线：**  
**为何采用/不采用 AI：**  
**价值契约：**  
**薄切片与架构：**  
**权限、安全和风险控制：**  
**评测集与版本对比：**  
**生产指标与成本：**  
**采用结果：**  
**失败、局限和下一步：**  
**可复制资产：**

## 附录 K　30/60/90 天行动表

| 阶段 | 目标 | 必须交付 | 验收信号 |
|---|---|---|---|
| 0-30 天 | 建立地图与可信度 | 角色图、流程图、风险假设、小修复 | 能清晰解释客户工作与系统 |
| 31-60 天 | 跑通有效闭环 | 基线、黄金集、真实薄切片、Trace | 用户用真实任务测试并产生数据 |
| 61-90 天 | 上线并沉淀 | 灰度、运营指标、复盘、复用资产 | 客户可承担部分运营，下一阶段有证据 |

# 术语表

**Agent**：由模型动态决定步骤和工具使用、在循环中完成目标的系统。  
**Adoption**：系统进入真实日常工作并持续产生价值的程度。  
**Evals**：将任务质量和风险标准变成可重复运行测试的评测体系。  
**FDE**：Forward Deployed Engineer，嵌入业务现场、端到端交付工程结果的角色。  
**FDSE**：Forward Deployed Software Engineer，与 FDE 高度相关的岗位名称。  
**Golden Set**：由真实任务与专家标准构成的高质量评测样本集。  
**Human-in-the-loop**：人在关键步骤提供审批、复核、上下文或异常接管。  
**MCP**：Model Context Protocol，连接 AI 应用与外部数据、工具的开放协议。  
**RAG**：Retrieval-Augmented Generation，以检索证据增强模型生成。  
**Shadow Mode**：系统处理真实流量但不影响业务结果的旁路运行方式。  
**Technical Deployment Lead**：负责部署范围、节奏、依赖和跨组织协调的角色。  
**Trace**：一次任务中模型、检索、工具、策略和人工操作的完整可追踪记录。

# 主要资料来源

## FDE 岗位与行业演进

1. OpenAI. “Forward Deployed Engineer (FDE) - SF.” https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/
2. OpenAI. “OpenAI launches the OpenAI Deployment Company.” https://openai.com/index/openai-launches-the-deployment-company/
3. OpenAI. “Introducing OpenAI Frontier.” https://openai.com/index/introducing-openai-frontier/
4. Anthropic. “Forward Deployed Engineer.” https://job-boards.greenhouse.io/anthropic/jobs/5302966008
5. Palantir. “A Day in the Life of a Palantir Forward Deployed Software Engineer.” https://blog.palantir.com/a-day-in-the-life-of-a-palantir-forward-deployed-software-engineer-45ef2de257b1
6. Palantir. “Dev versus Delta: Demystifying Engineering Roles at Palantir.” https://blog.palantir.com/dev-versus-delta-demystifying-engineering-roles-at-palantir-ad44c2a6e87

## Agent、评测与安全

7. Anthropic. “Building effective agents.” https://www.anthropic.com/engineering/building-effective-agents
8. Anthropic. “Trustworthy agents in practice.” https://www.anthropic.com/research/trustworthy-agents
9. OpenAI. “How evals drive the next chapter in AI for businesses.” https://openai.com/index/evals-drive-next-chapter-of-ai/
10. OpenAI. “Evals API Reference.” https://platform.openai.com/docs/api-reference/evals
11. Model Context Protocol. “Specification.” https://modelcontextprotocol.io/specification/
12. NIST. “AI Risk Management Framework.” https://www.nist.gov/itl/ai-risk-management-framework
13. NIST. “Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile.” https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
14. OWASP GenAI Security Project. “OWASP GenAI LLM Top 10 2026.” https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/

## 中国监管与标准

15. 国家互联网信息办公室等，《生成式人工智能服务管理暂行办法》，2023。https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm
16. 国家互联网信息办公室等，《人工智能生成合成内容标识办法》，2025。https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm
17. 国家市场监督管理总局、国家标准化管理委员会，GB 45438-2025《网络安全技术 人工智能生成合成内容标识方法》。https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=F32EA2A561F1886CD8D606513512D547

# 更新记录

**v1.0｜2026 年 8 月**：完成 8 篇、28 章、终章及 11 组工具模板；加入 FIELD 交付环、中国部署提示和资料来源分级。


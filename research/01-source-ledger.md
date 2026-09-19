# 公开来源台账

## 深入实战版核验　2026-09-18

本轮对参考书进行主题研究，正文、结构化教学数据、演算及配套代码独立编写。公开客户资料只证明材料明确报告的事实。新增系统设计、错误演练与项目步骤标记为本书教学设计，不宣称复原客户实现。

| ID | 来源 | 本轮用途 | 许可与限制 |
| --- | --- | --- | --- |
| D01 | [李博杰 AI Agent 开源书](https://github.com/bojieli/ai-agent-book) | 检查上下文、工具、评测与运行控制主题 | Apache-2.0；本书不复制其正文或代码 |
| D02 | [范冰公开 FDE 指南](https://github.com/xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer) | 对照岗位、业务与交付主题 | 免费阅读与非商业分享，商业改编需书面许可；本书独立表达，不作商业改编 |
| D03 | [Awesome FDE Roadmap](https://github.com/pierpaolo28/Awesome-FDE-Roadmap) | 对照数据工程、系统设计与学习范围 | MIT；清单中的岗位比例、工期及工具推荐不视为通用事实 |
| D04 | [Transformer 原始论文](https://arxiv.org/abs/1706.03762) | 注意力公式及机制边界 | 只讨论适用架构，不推定当前全部商业模型实现 |
| D05 | [PagedAttention 论文](https://arxiv.org/abs/2309.06180) | KV 内存管理与容量推演 | 教学参数由作者设计，非厂商实测 |
| D06 | [长上下文位置研究](https://arxiv.org/abs/2307.03172) | 证据顺序与回归测试 | 结果限于论文被测任务及模型 |
| D07 | [MCP 架构文档](https://modelcontextprotocol.io/docs/learn/architecture) | host、client、server 及协议边界 | 本轮文档重定向到 2026-07-28 版；实施时固定协议版本 |
| D08 | [PostgreSQL 显式锁文档](https://www.postgresql.org/docs/current/explicit-locking.html) | 资源并发教学与数据库责任 | 当前版本文档，示意 SQL 不构成完整生产实现 |
| D09 | [Google SRE 过载处理](https://sre.google/sre-book/handling-overload/) | 故障切换、限流与重试范围 | 本书自行设计客服故障演练 |
| D10 | [Anthropic Agent 评测工程说明](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 核对任务与轨迹评测主题 | 发布方工程经验，与本书测试结果分开 |

BBVA 页面在顶部将超过 70% 活跃使用标为月活，在结果汇总标为周活，两个口径不一致。第 22 章保留该问题，不以该比例做精确比较。每周节时仍属于发布方报告，不外推为已兑现利润。

最后的物料与采购助手是原创离线教学项目，证据等级 D。合成数据、确定性规划器与本地测试不能证明真实 ERP 接入、模型质量或生产收益。完整实现及运行方式见 [项目说明](../examples/material_assistant/README.md)。

具体研究与复算见 [理论交付笔记](deep-theory-notes.md)、[技术笔记](deep-tech-notes.md)和 [项目实测笔记](capstone-notes.md)。最终验收对 17 个 Python 片段做语法检查，10 个标记可独立运行的片段实际通过断言。Wilson 区间初稿下界误写已在集中执行中发现并修正，90/100、z 为 1.96 的区间为约 0.82563 至 0.94477。

## 图书重编增补　2026-09-17 核验，2026-09-18 发布

原有台账继续保留。新版基础章节是本书方法建议，案例的企业结果与教学设计分别标注。官方客户故事说明来源直接，不等于独立效果审计。

| ID | 来源 | 用途与限制 | 等级 |
| --- | --- | --- | --- |
| E01 | [Datawhale FDE100 案例](https://fde100.datawhale.cn/cases) | 本次可见 24 条案例，不把品牌名称中的 100 当作已公开篇数 | C |
| E02 | [制造业培训实践](https://fde100.datawhale.cn/cases/cases-009) | 培训平台、知识检索和陪跑；节时为案例自述，样本未完整披露 | C |
| E03 | [工业物料实践](https://fde100.datawhale.cn/cases/cases-024) | ERP 清理与检索，没有最终节省金额，不补写 ROI | C |
| E04 | [范冰的公开 FDE 指南](https://github.com/xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer) | 按章阅读参考与推荐原作；商业改编需作者书面许可，本项目不复制正文 | C |
| E05 | [Palantir AIP 入门](https://www.palantir.com/docs/foundry/aip/getting-started-with-aip) | 官方用例界定及工作流课程入口，账号与开放条件以官网为准 | A |
| E06 | [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction) | Agent 概念、框架、实践与评测，课程完成不等于生产交付能力 | A |
| E07 | [DeepLearning.AI 评测课程](https://www.deeplearning.ai/courses/evaluating-ai-agents) | 官方搜索结果核验课程与 Arize 合作；覆盖监控、组件评测与实验，费用不作固定承诺 | A |
| E08 | [Anthropic 工作流与 Agent](https://www.anthropic.com/engineering/building-effective-agents) | 概念与简单架构原则；原文提示工具生态已变化，不复制旧版本实现 | A |
| E09 | [Anthropic Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) | 检索过程与片段背景，本书不将实验结果泛化为通用提升幅度 | A |
| E10 | [MCP 架构](https://modelcontextprotocol.io/docs/learn/architecture) | 宿主、客户端、服务器及能力交换；实施需核对当前协议版本 | A |
| E11 | [Google SRE 监控](https://sre.google/sre-book/monitoring-distributed-systems/) | 服务监控原则，本书另行建议任务质量指标 | A |
| E12 | [OWASP 大模型风险项目](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | 安全检查参考，不代替具体组织审查 | A |
| E13 | [Arize Agent 评测文档](https://arize.com/docs/ax/learn/evaluation-concepts/agent-evaluation) | 组件与过程评测入口 | A |
| E14 | [Speechmatics X 招聘帖](https://x.com/Speechmatics/status/2030980311022985622) | 仅证明曾发布岗位线索，不证明职位仍开放、薪酬与行业规模 | C |

新版海外案例重新打开 C02、C05–C12 页面核对，正文只保留必要结果及流程概述。Datawhale cases-015 的顶部摘要与正文不一致，未纳入新版案例。社区审核徽记不表述为独立审计。

既有公开来源访问日期为 2026 年 9 月 6 日；破局社区 P01–P25 查询日期为 2026 年 9 月 16 日。日期写“未标注”的页面仍可能在发布后更新。使用前建议重新打开原页。

## 岗位与交付模式

| ID | 来源 | 发布方 | 日期 | 支持的内容 | 等级 |
| --- | --- | --- | --- | --- | --- |
| R01 | [OpenAI FDE 岗位](https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/) | OpenAI | 未标注 | 从发现、范围、设计到生产上线，采用和 eval 反馈 | A |
| R02 | [Anthropic FDE 岗位](https://job-boards.greenhouse.io/anthropic/jobs/5302966008) | Anthropic | 未标注 | 客户系统生产应用、MCP、sub-agent、skill 和模式复用 | A |
| R03 | [Palantir Forward Deployed AI Engineer](https://jobs.lever.co/palantir/636fc05c-d348-4a06-be51-597cb9e07488) | Palantir | 未标注 | 端到端 GenAI 工作流、客户共同交付和产品反馈 | A |
| R04 | [Scale GenAI FDE 岗位](https://scale.com/careers/4593571005) | Scale AI | 未标注 | 客户专用数据基础设施、全栈开发和快速实验 | A |
| R05 | [OpenAI Deployment Company](https://openai.com/index/openai-launches-the-deployment-company/) | OpenAI | 2026 | 价值诊断、流程优先级、FDE 驻场构建和复用 | A |
| R06 | [OpenAI Frontier](https://openai.com/zh-Hans-CN/index/introducing-openai-frontier/) | OpenAI | 2026 | 由 FDE 与客户团队共同建立生产 Agent 实践 | A |
| R07 | [Palantir 资深 FDE 对工作方式的说明](https://community.palantir.com/t/who-are-palantir-fdes/6847/4) | Palantir Developer Community | 2026-07-15 | FDE 是产品开发方式，现场学习进入核心平台 | C |
| R08 | [Palantir AI FDE 文档](https://www.palantir.com/docs/foundry/ai-fde/overview) | Palantir | 持续更新 | Agent 的上下文、工具、权限、分支与审查 | A |
| R09 | [Palantir AI FDE GA 公告](https://www.palantir.com/docs/foundry/announcements/2026-03) | Palantir | 2026-03-12 | AI FDE 从测试进入正式可用 | A |
| R10 | [OpenAI 新加坡计划](https://openai.com/index/introducing-openai-for-singapore/) | OpenAI | 2026 | FDE 人才建设和行业部署方向 | A |

## 海外案例

| ID | 来源 | 发布方 | 日期 | 支持的内容 | 等级 |
| --- | --- | --- | --- | --- | --- |
| C01 | [Skywise 早期采用案例](https://www.airbus.com/en/newsroom/news/2017-06-skywise-airline-early-adopter-highlights) | Airbus | 2017-06 | AirAsia、Delta、easyJet、Emirates 的流程和早期结果 | A |
| C02 | [Airbus 发布 Skywise](https://www.airbus.com/en/newsroom/press-releases/2017-06-airbus-launches-skywise-aviations-open-data-platform) | Airbus | 2017-06 | 平台范围、数据整合和主要业务目标 | A |
| C03 | [Airbus 扩展 Skywise 到供应商](https://www.airbus.com/en/newsroom/press-releases/2018-07-airbus-extends-skywise-to-suppliers) | Airbus | 2018-07 | Dispatch 应用与 Premium Aerotec 试点 | A |
| C04 | [Airbus 2026 公司资料](https://mediaassets.airbus.com/pm_38_779_779043-7t75d4o17q.pdf) | Airbus | 2026-01 | 用户、飞机规模与部分节省指标 | A |
| C05 | [Tampa General 与 Palantir 扩大合作](https://www.tgh.org/news/tgh-press-releases/2024/june/tgh-selects-palantir-ai-software-connected-care-coordination) | Tampa General Hospital | 2024-06-05 | 病床安排、PACU、脓毒症住院时长和协作方式 | A |
| C06 | [Morgan Stanley eval 案例](https://openai.com/index/morgan-stanley/) | OpenAI 与 Morgan Stanley | 未标注 | 评测、检索、会议总结、人工复核和采用 | A |
| C07 | [BBVA 全球 AI 部署](https://openai.com/index/bbva/) | OpenAI 与 BBVA | 2026-06-11 | 从 3000 人试点到 10 万人、治理与冠军网络 | A |
| C08 | [TIME AI 案例](https://scale.com/customers/time) | Scale AI 与 TIME | 未标注 | 两个月上线、多模态、7000 条攻击向量和护栏 | A |
| C09 | [GitLab 产品集成案例](https://claude.com/customers/gitlab) | Anthropic 与 GitLab | 2024 | 多模型评估、Duo 功能和工程组织 | A |
| C10 | [GitLab 企业采用案例](https://claude.com/customers/gitlab-enterprise) | Anthropic 与 GitLab | 2024 | 满意度、效率区间、SSO 和跨部门工作流 | A |
| C11 | [Assembled 客服运营案例](https://claude.com/customers/assembled) | Anthropic 与 Assembled | 2025 | 全量响应评测、路由、故障切换和业务指标 | A |
| C12 | [Klarna AI 助手早期结果](https://openai.com/index/klarna/) | OpenAI 与 Klarna | 2024 | 对话量、处理时长、重复咨询和利润预估 | A |
| C13 | [Klarna 上市申报文件](https://www.sec.gov/Archives/edgar/data/2003292/000200329225000036/klarnagroupplcf-1a4.htm) | Klarna 与 SEC | 2025 | AI 和高质量人工支持并行的后续策略 | A |
| C14 | [客服自动化仍需人工的报道](https://apnews.com/article/ca87ae77d7c6797ebb2628bd1b532929) | Associated Press | 2025 | 身份盗用等复杂问题需要人工 | B |

## GitHub 与工程资料

| ID | 来源 | 用途 | 备注 |
| --- | --- | --- | --- |
| G01 | [OpenAI Cookbook](https://github.com/openai/openai-cookbook) | API、Agent、eval 和生产样例 | MIT，使用时确认具体示例依赖 |
| G02 | [OpenAI Evals](https://github.com/openai/evals) | 评测数据与评分框架 | MIT，旧框架与平台 Evals 的关系需按最新文档确认 |
| G03 | [OpenAI Agents SDK for Python](https://github.com/openai/openai-agents-python) | Agent、handoff、guardrail 与 tracing | 版本变化快 |
| G04 | [Claude Cookbooks](https://github.com/anthropics/claude-cookbooks) | Agent 工作流和 Claude API 样例 | 检查各目录说明 |
| G05 | [MCP Servers](https://github.com/modelcontextprotocol/servers) | MCP 参考服务器和社区入口 | 参考实现不等于已通过企业安全评审 |
| G06 | [Langfuse](https://github.com/langfuse/langfuse) | Trace、评测、数据集和提示管理 | 自托管仍需设计数据保留 |
| G07 | [Arize Phoenix](https://github.com/Arize-ai/phoenix) | OpenTelemetry、LLM Trace 和评测 | 检查模型调用数据去向 |
| G08 | [Promptfoo](https://github.com/promptfoo/promptfoo) | 提示、Agent 和红队测试 | 适合 CI 回归 |
| G09 | [NVIDIA Garak](https://github.com/NVIDIA/garak) | LLM 漏洞扫描 | 扫描结果仍需人工研判 |
| G10 | [Microsoft Presidio](https://github.com/microsoft/presidio) | PII 检测与脱敏 | 需要按语言和业务数据做误差测试 |
| G11 | [Unleash](https://github.com/Unleash/unleash) | 功能开关和灰度 | 生产控制组件 |
| G12 | [Palantir Foundry Python SDK](https://github.com/palantir/foundry-platform-python) | Foundry API 接入 | 与特定平台绑定 |
| G13 | [LiteLLM](https://github.com/BerriAI/litellm) | 多模型代理、预算与路由 | 上线前核验兼容性和故障模式 |
| G14 | [OpenTelemetry Specification](https://github.com/open-telemetry/opentelemetry-specification) | 跨服务观测规范 | 需要额外定义 AI 语义字段 |

## X 与社区信号

| ID | 来源 | 信号 | 等级 |
| --- | --- | --- | --- |
| X01 | [Custom Autonomous Software 长帖](https://x.com/mikiarlo3/status/2019662719503274036) | 有创业者把 FDE 视为定制自治软件的交付角色 | C |
| X02 | [Speechmatics 招聘帖](https://x.com/Speechmatics/status/2030980311022985622) | 语音 AI 公司公开招聘 FDE | C |
| X03 | [法律 AI 公司招聘信号](https://x.com/AndreaShuyuWang/status/2029996449136791919) | 法律 AI 初创公司同时招聘解决方案、客户成功与 FDE | C |
| X04 | [OpenAI Forward Deployed Evals 从业者资料页](https://x.com/bfioca/with_replies) | FDE 内部分工开始出现 eval 专门化 | C |

## 破局社区高赞主题（2026-09-16）

以下仅支持社区观点、作者自述或自身活动安排，外链全文未读取。点赞来自官网列表快照，不能证明业务效果。详见 [分类梳理](../knowledge-base/07-中国社区实践/01-破局FDE点赞Top25分类梳理.md)。

| ID | 主题 | 发布者 | 创建日期 | 等级及限制 |
| --- | --- | --- | --- | --- |
| P01 | [FDE 行动营立项调研](https://aipoju.com/topic-details/22255411124825821) | findyi | 2026-08-11 | C：社区陈述，非独立核验 |
| P02 | [AI洞察37：FDE 与企业 AI 落地](https://aipoju.com/topic-details/14422142451251212) | findyi | 2026-07-21 | C：社区陈述，非独立核验 |
| P03 | [AI洞察39：从个人经验到 AI 生产系统](https://aipoju.com/topic-details/82255158222225822) | findyi | 2026-08-14 | C：社区陈述，非独立核验 |
| P04 | [AI洞察38：训练能交付的 AI 员工](https://aipoju.com/topic-details/55522441822825484) | findyi | 2026-07-29 | C：社区陈述，非独立核验 |
| P05 | [AI洞察36：AI 企业服务的三层定位](https://aipoju.com/topic-details/45544282214441288) | findyi | 2026-07-16 | C：社区陈述，非独立核验 |
| P06 | [从追工具到系统化、产品化](https://aipoju.com/topic-details/45544228841514818) | findyi | 2026-07-28 | C：社区陈述，非独立核验 |
| P07 | [企业分享经历与体系化学习](https://aipoju.com/topic-details/45548858885218488) | findyi | 2026-08-27 | C：社区陈述，非独立核验 |
| P08 | [部署 Obsidian + Claude Code 知识库](https://aipoju.com/topic-details/22258842455154411) | 攀登者 | 2026-09-03 | C：社区陈述，非独立核验 |
| P09 | [BSS 共创办公中心计划](https://aipoju.com/topic-details/22258828551255241) | findyi | 2026-08-26 | C：社区陈述，非独立核验 |
| P10 | [第十二期行动营与系统化能力](https://aipoju.com/topic-details/82258841825852242) | findyi | 2026-09-08 | C：社区陈述，非独立核验 |
| P11 | [Skill 商城和 CLI 内测开启](https://aipoju.com/topic-details/22258842558454481) | 文辉 | 2026-09-02 | C：社区陈述，非独立核验 |
| P12 | [人、Agent、AI 团队与 FDE 的关系](https://aipoju.com/topic-details/82258825552818552) | 晓君@AI破局 | 2026-08-24 | C：社区陈述，非独立核验 |
| P13 | [50 万+业绩背后的企业服务踩坑](https://aipoju.com/topic-details/45544225211444288) | 小林 | 2026-08-01 | C：社区陈述，非独立核验 |
| P14 | [从超级个体到超级组织：直播复盘](https://aipoju.com/topic-details/45544212142488488) | 栋哥 | 2026-08-08 | C：社区陈述，非独立核验 |
| P15 | [FDE 在企业 AI 落地的碰撞、方法与案例](https://aipoju.com/topic-details/14425558442428542) | 潘达 | 2026-08-23 | C：社区陈述，非独立核验 |
| P16 | [两个进行中的 FDE 项目：网店与电子厂](https://aipoju.com/topic-details/14425511224421222) | 伍哥_广州 | 2026-09-04 | C：社区陈述，非独立核验 |
| P17 | [企业级六位数 FDE 商单详解](https://aipoju.com/topic-details/55521154242142554) | 小林 | 2026-08-31 | C：社区陈述，非独立核验 |
| P18 | [第十二期行动教练与志愿者招募](https://aipoju.com/topic-details/14422822584224882) | 果果｜竹子助理(10:00-20:00) | 2026-08-12 | A：自身活动；C：效果与观点 |
| P19 | [破局新人使用地图](https://aipoju.com/topic-details/82811422125448852) | 竹子助理(10:00-20:00) | 2026-03-24 | A：自身活动；C：效果与观点 |
| P20 | [消费品行业 FDE：AI 与人的现场磨合](https://aipoju.com/topic-details/22258881525444581) | 潘达 | 2026-08-22 | C：社区陈述，非独立核验 |
| P21 | [从 AI 聊天到业务工作系统](https://aipoju.com/topic-details/82258881525544422) | 王庆 | 2026-08-21 | C：社区陈述，非独立核验 |
| P22 | [30 天五金厂 FDE 交付日记](https://aipoju.com/topic-details/45548852824524448) | 一只阿木木 | 2026-09-01 | C：社区陈述，非独立核验 |
| P23 | [赏金猎人015：FDE 与企业服务实战征集](https://aipoju.com/topic-details/45548882114558418) | findyi | 2026-08-21 | A：自身活动；C：效果与观点 |
| P24 | [FDE 行动营拆解与学习边界](https://aipoju.com/topic-details/22258841241152241) | 小林 | 2026-09-08 | C：社区陈述，非独立核验 |
| P25 | [实测十个 Skill：把经验变成工具](https://aipoju.com/topic-details/55521154281822454) | 王庆 | 2026-08-31 | C：社区陈述，非独立核验 |

## 本轮案例文章回读　2026-09-19

破局 CLI 逐页返回 13 页、1274 条“FDE”检索结果。筛选时排除活动通知、概念讨论、课程推广和只有标题的线索，识别出 21 篇实战类主题。四篇被扩写为新版第 28–31 章，其余 17 篇整理在[实战案例文章集](../knowledge-base/07-中国社区实践/08-FDE实战案例文章集.md)。前三篇同时回读了作者公开的飞书文档；五金厂文章目前只能核对破局官网导读。金额、项目结果和架构仍按作者陈述或未核验线索处理，不作为独立审计结论。

| ID | 原始文章与补充材料 | 本轮读取范围 | 等级与限制 |
| --- | --- | --- | --- |
| P15/F01 | [潘达：FDE 在企业 AI 落地的碰撞、方法与案例](https://aipoju.com/topic-details/14425558442428542)；[公开飞书文档](https://fcnubuhvffh5.feishu.cn/wiki/X7scwWN1BiWF2lkQEnscC1Oln9d) | 破局主题与飞书正文；关注黑河外贸物流、夜间 WhatsApp 咨询、猎头辅助、工业多系统和“工具—SOP—组织能力”路径 | C：作者陈述；无客户审计、合同或完整架构 |
| P42/F02 | [凡人：五万元商单从需求到交付](https://aipoju.com/topic-details/45548825414152218)；[公开飞书文档](https://my.feishu.cn/wiki/Ix4UwGPbzikeP8khlITcVechnvc) | 破局主题与飞书正文；读取需求抓取、报价合同、深挖、设计、受控开发、测试、部署迁移、验收和复购流程 | C：金额和经历为作者自述；无合同、回款或客户指标 |
| P17/F03 | [小林：企业级六位数 FDE 商单详解](https://aipoju.com/topic-details/55521154242142554)；[公开飞书文档](https://my.feishu.cn/wiki/AcLZwC18MiJEE1kZf6XclnwWnWb) | 破局主题与飞书正文；读取小单验证、正式项目、案例积累、大单破冰、介绍渠道和复购思路 | C：金额、佣金和利润为作者自述；无客户系统或财务审计 |
| P22 | [30 天五金厂 FDE 交付日记](https://aipoju.com/topic-details/45548852824524448)；[CLI 案例检索记录](breakout-2026-09-19-fde-cases.json) | 官网可见导读；未读取可验证的全文交付记录 | C：只能写观察文章；搜索摘要中的 Agent 数量、百分比和停机结果均未采用 |

案例检索记录保存在 [`research/breakout-2026-09-19-fde-cases.json`](breakout-2026-09-19-fde-cases.json)，列出查询规模、筛选规则、入选文章和证据限制。X 搜索页本轮只作为发现线索，未把无法稳定读取的正文写入案例事实。

## 破局社区 Top 100 扩展来源（P26–P100）

查询日期2026-09-16。P01–P25沿用上节编号且与本轮前25名一致；后75篇如下。详情复核改用可见正文解析，排名以本轮列表快照为准。见 [Top100分类索引](../knowledge-base/07-中国社区实践/02-破局FDE点赞Top100分类索引.md)。

| ID | 主题 | 发布者 | 创建日期 | 等级及限制 |
| --- | --- | --- | --- | --- |
| P26 | [第十二期行动报名与能力升级](https://aipoju.com/topic-details/82258841421115542) | 果果｜竹子助理(10:00-20:00) | 2026-09-09 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P27 | [信号站：把 AI 能力翻译成业务结果](https://aipoju.com/topic-details/22258848181552821) | 是苗苗呀 | 2026-09-01 | C（社区作者陈述）；外链全文未读 |
| P28 | [智能体大赛观察与 FDE 需求判断](https://aipoju.com/topic-details/45544228852121288) | findyi | 2026-07-28 | C（社区作者陈述）；外链全文未读 |
| P29 | [第十二期行动选题拆解直播预告](https://aipoju.com/topic-details/45548825448824858) | 果果｜竹子助理(10:00-20:00) | 2026-09-02 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P30 | [FDE 的百万之路](https://aipoju.com/topic-details/55521118212841124) | 右军 | 2026-08-21 | C（社区作者陈述）；外链全文未读 |
| P31 | [从超级个体到超级组织的实战地图](https://aipoju.com/topic-details/14422188421814552) | 晓君@AI破局 | 2026-08-10 | C（社区作者陈述）；外链全文未读 |
| P32 | [从蚂蚁 P9 到 AI 企业服务创业](https://aipoju.com/topic-details/82255444182288182) | 右军 | 2026-08-04 | C（社区作者陈述）；外链全文未读 |
| P33 | [十个项目的预报名选择指南](https://aipoju.com/topic-details/45548822228441588) | 果果｜竹子助理(10:00-20:00) | 2026-09-07 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P34 | [开营仪式：先动手，再沉淀系统](https://aipoju.com/topic-details/82258818118824512) | 果果｜竹子助理(10:00-20:00) | 2026-09-15 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P35 | [APP 开发流程的 Agent 与 Skill 改造](https://aipoju.com/topic-details/45544145254145818) | 卓峰丶 | 2026-08-18 | C（社区作者陈述）；外链全文未读 |
| P36 | [云端 AI 工作台与运行规则的个人实践](https://aipoju.com/topic-details/22258841821524241) | 静水流深 | 2026-09-08 | C（社区作者陈述）；外链全文未读 |
| P37 | [把破局 CLI 封装成可复用 Skill](https://aipoju.com/topic-details/82258842585414182) | AI生产力廖老师 | 2026-09-02 | C（社区作者陈述）；外链全文未读 |
| P38 | [FDE 初探营扩容需求调研](https://aipoju.com/topic-details/55521148811811144) | 果果｜竹子助理(10:00-20:00) | 2026-09-09 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P39 | [政策线索与应用型 FDE 人才](https://aipoju.com/topic-details/82258842518845452) | 小林 | 2026-09-02 | C（社区作者陈述）；外链全文未读 |
| P40 | [第 1001 篇帖子：组织成长与企业服务定位](https://aipoju.com/topic-details/45548814458541128) | 小林 | 2026-09-09 | C（社区作者陈述）；外链全文未读 |
| P41 | [Skill 和 Agent 是 FDE 入门基础](https://aipoju.com/topic-details/55521182155224854) | findyi | 2026-09-10 | C（社区作者陈述）；外链全文未读 |
| P42 | [五万元商单：从需求到交付](https://aipoju.com/topic-details/45548825414152218) | 凡人 | 2026-09-02 | C（社区作者陈述）；外链全文未读 |
| P43 | [是否增加 Agent、Skill 与 FDE 行动营](https://aipoju.com/topic-details/14422114448148282) | findyi | 2026-07-31 | C（社区作者陈述）；外链全文未读 |
| P44 | [破局七月刊：企业服务与 AI 系统资料导航](https://aipoju.com/topic-details/22255411251455511) | 竹子助理(10:00-20:00) | 2026-08-10 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P45 | [初探营扩容与理性报名建议](https://aipoju.com/topic-details/55521182124488214) | 果果｜竹子助理(10:00-20:00) | 2026-09-10 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P46 | [FDE 所需技能与现场软能力](https://aipoju.com/topic-details/22258884825244141) | 小林 | 2026-08-19 | C（社区作者陈述）；外链全文未读 |
| P47 | [从逗号事故到企业 Agent 工作流](https://aipoju.com/topic-details/82258815145225852) | 成都大书 | 2026-09-12 | C（社区作者陈述）；外链全文未读 |
| P48 | [FDE 与外包：需求、交付和算力成本](https://aipoju.com/topic-details/14422825252845222) | 小林 | 2026-08-14 | C（社区作者陈述）；外链全文未读 |
| P49 | [报名截止提醒与聚焦一个主项目](https://aipoju.com/topic-details/22258818444854811) | 果果｜竹子助理(10:00-20:00) | 2026-09-14 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P50 | [破局八月刊：AI 员工与 FDE 精选](https://aipoju.com/topic-details/22258815824854581) | 竹子助理(10:00-20:00) | 2026-09-10 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P51 | [不要跳过 Skills 与 Agent 基础](https://aipoju.com/topic-details/14425582545154242) | 王庆 | 2026-09-10 | C（社区作者陈述）；外链全文未读 |
| P52 | [机器人服务付费用户与人机判断边界](https://aipoju.com/topic-details/22258841854455851) | 静水流深 | 2026-09-08 | C（社区作者陈述）；外链全文未读 |
| P53 | [短视频共学复盘：流量与转化的断点](https://aipoju.com/topic-details/55522488148814114) | 攀哥用AIP做文创变现 | 2026-08-10 | C（社区作者陈述）；外链全文未读 |
| P54 | [右军的 FDE 交付方法论资料](https://aipoju.com/topic-details/45548855851585248) | 右军 | 2026-08-30 | C（社区作者陈述）；外链全文未读 |
| P55 | [七类行业咨询：让经验成为可调用资产](https://aipoju.com/topic-details/14422821558141182) | 晓君@AI破局 | 2026-08-19 | C（社区作者陈述）；外链全文未读 |
| P56 | [不写代码，在培训公司做四个月 FDE](https://aipoju.com/topic-details/14425582185825882) | 小鱼AI成长日记 | 2026-09-11 | C（社区作者陈述）；外链全文未读 |
| P57 | [FDE 如何报价、分成与选择行业](https://aipoju.com/topic-details/14425585825514542) | 小林 | 2026-09-14 | C（社区作者陈述）；外链全文未读 |
| P58 | [周报：FDE 行动营立项与直播复盘入口](https://aipoju.com/topic-details/82255158222222282) | 竹子助理(10:00-20:00) | 2026-08-14 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P59 | [FDE 是企业落地操盘手的能力组合](https://aipoju.com/topic-details/82258815182554282) | 乘风 | 2026-09-11 | C（社区作者陈述）；外链全文未读 |
| P60 | [周报：行动营报名、扩容与案例推荐](https://aipoju.com/topic-details/45548814142251858) | 竹子助理(10:00-20:00) | 2026-09-11 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P61 | [线下组局导航：FDE 与智能体交流](https://aipoju.com/topic-details/22258841154114451) | 清程｜官方组局官 | 2026-09-09 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P62 | [右军的城市 FDE 组局协作条件](https://aipoju.com/topic-details/45548825288514188) | 右军 | 2026-09-03 | C（社区作者陈述）；外链全文未读 |
| P63 | [商业思维复盘：先听懂老板的场景](https://aipoju.com/topic-details/45548825551584818) | 栋哥 | 2026-09-03 | C（社区作者陈述）；外链全文未读 |
| P64 | [从 PPT 单次交付到生产系统](https://aipoju.com/topic-details/45548814128454528) | 礼尚往来 | 2026-09-12 | C（社区作者陈述）；外链全文未读 |
| P65 | [用 Aily 与多维表格做客服问题分诊](https://aipoju.com/topic-details/55521141815844584) | 书小哥 | 2026-09-01 | C（社区作者陈述）；外链全文未读 |
| P66 | [把个人经验转成企业能力的学习思考](https://aipoju.com/topic-details/22255414151882121) | 紫晶-人生处处有希望 | 2026-08-09 | C（社区作者陈述）；外链全文未读 |
| P67 | [第一次 FDE 线下分享的组织记录](https://aipoju.com/topic-details/82255445811258182) | AI卷王龙哥 | 2026-07-26 | C（社区作者陈述）；外链全文未读 |
| P68 | [赏金猎人015收官与十九篇实战合集](https://aipoju.com/topic-details/14425582822512512) | 竹子助理(10:00-20:00) | 2026-09-11 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P69 | [周报：CLI 内测与课程拆解直播](https://aipoju.com/topic-details/14425511248142182) | 竹子助理(10:00-20:00) | 2026-09-04 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P70 | [周报：课程、体验卡与线下参与导航](https://aipoju.com/topic-details/22255445542481251) | 竹子助理(10:00-20:00) | 2026-07-24 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P71 | [企业 AI 最后一公里与人才白皮书入口](https://aipoju.com/topic-details/45544544544518148) | 曲率出逃 | 2026-05-26 | C（社区作者陈述）；外链全文未读 |
| P72 | [产品经理进入 GEO 与 FDE 创业](https://aipoju.com/topic-details/14425582821422152) | 韩四四 | 2026-09-11 | C（社区作者陈述）；外链全文未读 |
| P73 | [周报：企业分享与系统化升级直播](https://aipoju.com/topic-details/45548855451411258) | 竹子助理(10:00-20:00) | 2026-08-28 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P74 | [AI 夜校、培训项目与企业服务生态](https://aipoju.com/topic-details/22258824524484811) | 江校长-华强北AI生态发起人 | 2026-08-31 | C（社区作者陈述）；外链全文未读 |
| P75 | [FDE 是组织能力，现场经验要回流产品](https://aipoju.com/topic-details/82258881554181112) | 大圣 | 2026-08-21 | C（社区作者陈述）；外链全文未读 |
| P76 | [周报：超级个体到超级组织直播预告](https://aipoju.com/topic-details/55522484515522524) | 竹子助理(10:00-20:00) | 2026-08-07 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P77 | [九月中旬全国线下组局导航](https://aipoju.com/topic-details/55521522482285514) | 清程｜官方组局官 | 2026-09-16 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P78 | [从客户一句话到原型的线下活动导航](https://aipoju.com/topic-details/55521145252558254) | 清程｜官方组局官 | 2026-09-02 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P79 | [小白 SOP：从最小任务训练 AI 员工](https://aipoju.com/topic-details/45544212188815888) | 神经蛙 | 2026-08-09 | C（社区作者陈述）；外链全文未读 |
| P80 | [FDE 岗位、生态与先行者经验导航](https://aipoju.com/topic-details/45548858552225158) | 兔女财 | 2026-08-27 | C（社区作者陈述）；外链全文未读 |
| P81 | [个人 AI 组织系统的峰会复盘](https://aipoju.com/topic-details/55522411411815454) | 栋哥 | 2026-07-11 | C（社区作者陈述）；外链全文未读 |
| P82 | [把 AI 技能转成业务结果的能力](https://aipoju.com/topic-details/45548814142255458) | 一只阿木木 | 2026-09-11 | C（社区作者陈述）；外链全文未读 |
| P83 | [超级组织直播的深度学习笔记](https://aipoju.com/topic-details/22255414154152181) | 龚大平 | 2026-08-09 | C（社区作者陈述）；外链全文未读 |
| P84 | [组局经验：文案、内容与参与体验](https://aipoju.com/topic-details/82255444148582212) | 朱胜 | 2026-08-04 | C（社区作者陈述）；外链全文未读 |
| P85 | [文创服务在企业服务金字塔中的定位](https://aipoju.com/topic-details/55522418155228214) | 攀哥用AIP做OPC文创变现 | 2026-07-18 | C（社区作者陈述）；外链全文未读 |
| P86 | [行业大会后的周报与复盘推荐](https://aipoju.com/topic-details/14422158554422842) | 竹子助理(10:00-20:00) | 2026-07-17 | A（自身活动安排）／C（转述、观点及效果）；外链全文未读 |
| P87 | [训练营学习：从访谈到 PoC 与试点](https://aipoju.com/topic-details/14425585551182282) | 悦读者｜02 | 2026-09-13 | C（社区作者陈述）；外链全文未读 |
| P88 | [国企内部 AI 实践：业务需求翻译](https://aipoju.com/topic-details/22258842425885541) | 梓惠 | 2026-09-04 | C（社区作者陈述）；外链全文未读 |
| P89 | [珠海 FDE 交流：从学技术走向业务闭环](https://aipoju.com/topic-details/82258844412582442) | 风影子 | 2026-09-07 | C（社区作者陈述）；外链全文未读 |
| P90 | [Skill、CLI、MCP 与 Agent 的进阶理解](https://aipoju.com/topic-details/45548828128544888) | 栋哥 | 2026-09-02 | C（社区作者陈述）；外链全文未读 |
| P91 | [矿山工程场景的 FDE 落地思考](https://aipoju.com/topic-details/14425544511255422) | 岁月不饶人 | 2026-08-30 | C（社区作者陈述）；外链全文未读 |
| P92 | [内容运营与知识库工具的个人进展](https://aipoju.com/topic-details/55521151428551214) | amy | 2026-08-27 | C（社区作者陈述）；外链全文未读 |
| P93 | [灯具外贸市场发现与业务拓展](https://aipoju.com/topic-details/14425558845485112) | 一只阿木木 | 2026-08-24 | C（社区作者陈述）；外链全文未读 |
| P94 | [东莞厂区的现场访谈记录](https://aipoju.com/topic-details/22255428558445281) | 林高山 | 2026-07-22 | C（社区作者陈述）；外链全文未读 |
| P95 | [To B AI 项目：数据与经营结果优先](https://aipoju.com/topic-details/55521182242814184) | 怪兽抱抱 | 2026-09-09 | C（社区作者陈述）；外链全文未读 |
| P96 | [一个人用 AI 编程支撑商业化软件](https://aipoju.com/topic-details/82258844525221482) | 天狼🐺 | 2026-09-04 | C（社区作者陈述）；外链全文未读 |
| P97 | [从 AI 培训走向 FDE 的交流复盘](https://aipoju.com/topic-details/55521141855848244) | 醒狮 | 2026-09-01 | C（社区作者陈述）；外链全文未读 |
| P98 | [左手 IP、右手 FDE 的个人服务规划](https://aipoju.com/topic-details/45548855252815128) | AI卷王龙哥 | 2026-08-31 | C（社区作者陈述）；外链全文未读 |
| P99 | [从 Agent 开发到企业 FDE 内部转岗](https://aipoju.com/topic-details/55521155452815824) | 石彬 | 2026-08-30 | C（社区作者陈述）；外链全文未读 |
| P100 | [五级进阶：从会用 AI 到带 AI 做事](https://aipoju.com/topic-details/82258828582458252) | 攀哥用AIP做文创变现 | 2026-08-26 | C（社区作者陈述）；外链全文未读 |

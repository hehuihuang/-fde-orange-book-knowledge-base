# 深入版理论与交付章节研究笔记

本笔记对应第 1 至 4 章及第 11 至 18 章。核对日期为 2026-09-18。正文保留原版中仍成立的简要说明，并新增由作者组织的系统分析、教学工件、明确算例及练习参考。

## 参考项目与许可边界

| 项目 | 已核对内容 | 许可或版权说明 | 本次使用方式 |
| --- | --- | --- | --- |
| [范冰的 FDE 指南](https://github.com/xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer) | README 的主题与版权段落 | 著作权归作者，允许免费阅读及非商业分享，商业使用含改编培训需书面许可 | 仅作为阅读线索与正文链接，没有复制正文、例子、代码或逐章改写 |
| [Awesome FDE Roadmap](https://github.com/pierpaolo28/Awesome-FDE-Roadmap) | README 主题、工具路线与 [LICENSE](https://github.com/pierpaolo28/Awesome-FDE-Roadmap/blob/main/LICENSE) | MIT，版权人 Pier Paolo Ippolito，2026 | 参考数据、架构、客户协作主题，独立组织采购教学流程，不复制其代码、模板、措辞或强制学习时间表 |

Roadmap 的军事与合规段落包含需要具体法律和环境条件才能成立的断言。本书没有采用这些段落作为法律结论。引用阅读入口不意味着接受原作的全部数字或主张。

## 第一方资料与事实边界

| 来源 | 核对的具体材料 | 对应章节 | 本书能够据此说明 | 不支持的结论 |
| --- | --- | --- | --- | --- |
| [OpenAI FDE 岗位](https://openai.com/careers/forward-deployed-engineer-%28fde%29-sf-san-francisco/) | discovery、technical scoping、system design、build、production rollout 及 adoption、workflow impact、eval-driven feedback | 1、4 | 这份岗位把发现到生产与采用列在职责中 | 所有公司的统一职责、人员配置、岗位增长或平均薪酬 |
| [Palantir Ontology](https://www.palantir.com/docs/foundry/ontology/overview) | 对象、关系、动作及与应用的连接 | 1、2 | 业务对象及动作有助于组织数据与应用 | 任何案例客户的私有架构、内部表结构 |
| [Palantir AIP 学习入口](https://www.palantir.com/docs/foundry/aip/getting-started-with-aip) | 平台入门、Scoping Use Cases、First AIP Workflow 的官方课程入口 | 2、11、18 | 官方学习将用例界定与构建连接 | 完成课程就能交付生产系统，或固定天数就业保证 |
| [OMG BPMN](https://www.omg.org/spec/BPMN/) | BPMN 2.0.2 规范入口与流程表达的事件、活动和分支概念 | 2 | 可以使用标准符号进一步表达流程 | 本书简化状态表已覆盖规范全部语义 |
| [MIT 制造系统排队课程](https://live.ocw.mit.edu/courses/2-854-introduction-to-manufacturing-systems-fall-2016/5d3e9532c2ff6e156d48e41f9bd9576f_MIT2_854F16_Queueing.pdf) | 平稳条件下 L=λW、平均在途和平均停留时间的关系 | 2 | 可作边界一致、稳定流程的平均量一致性检查 | 对真实复杂队列的确定性预测 |
| [Stripe 幂等请求](https://docs.stripe.com/api/idempotent_requests) | 同键重试、结果复用及参数冲突处理 | 2 | 说明一种实际接口的幂等语义约定 | 自定义工具天然幂等，或不同服务都使用相同有效期限 |
| [PostgreSQL 事务隔离](https://www.postgresql.org/docs/current/transaction-iso.html) | 并发隔离保证、冲突与事务重试条件 | 2、14 | 应用的先查后写需要明确并发控制 | 普通客户端读取足以保证后续写入规则仍成立 |
| [Anthropic 有效 Agent](https://www.anthropic.com/engineering/building-effective-agents) | 工作流与 Agent 的结构差异，从简单结构开始的工程建议 | 1、13、18 | 根据任务不确定性考虑结构取舍 | 作者教学采购架构是 Anthropic 客户内部实现 |
| [Anthropic Agent 评测](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 评测及执行结果的区分、样本和评分维护 | 13 | 原型应由可重复实验而非单次演示支持 | 教学三十条样本可推算真实业务准确率 |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) 与 [Playbook](https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook) | 自愿风险管理框架与治理、映射、测量、管理实践入口 | 1、11、12 | 资料适合帮助整理条件、责任和风险工件 | 等同法规认证，或为本项目提供统一合规结论 |
| [Google Cloud 架构框架](https://docs.cloud.google.com/architecture/framework) | 安全、运行、可靠性、性能、成本等架构观察方向 | 4 | 架构审阅需要考虑多个质量属性 | 本项目必须采用某个云产品 |
| [AWS ADR 指导](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html) | 决策背景、决定、后果及记录生命周期 | 4、14、17 | 架构选择应保留理由与条件变化 | 本书自编 ADR 例子是 AWS 的原模板 |
| [Google SRE 服务目标](https://sre.google/sre-book/service-level-objectives/) 与 [实施 SLO](https://sre.google/workbook/implementing-slos/) | 测量指标与目标的区别、合格事件及错误预算 | 3、12、15 | 运行承诺需要明确分子分母和测量方法 | 使用一个 HTTP 成功率即可证明业务正确 |
| [Google SRE 灰度](https://sre.google/workbook/canarying-releases/) | 部分范围、有限时间暴露变更，再观察是否扩大 | 14 | 发布可以按风险单位逐步扩大 | 本书五用户或阶段安排是 Google 通用标准 |
| [Google SRE 监控](https://sre.google/sre-book/monitoring-distributed-systems/) | 延迟、流量、错误和饱和度 | 14、15 | 服务指标之外仍需任务质量证据 | 日志充分即可证明真实采用与收益 |
| [OpenTelemetry 追踪](https://opentelemetry.io/docs/concepts/signals/traces/) | trace、span 与操作父子关系 | 15 | 追踪帮助将请求关联到依赖步骤 | 必须采集用户全文或模型隐藏推理 |
| [Google SRE 过载](https://sre.google/sre-book/handling-overload/) | 限制负载、处理容量与重试压力 | 15 | 依赖预算、限流和降级需要设计 | 可以略过权限与关键规则以缓解过载 |
| [Google SRE 事故](https://sre.google/sre-book/managing-incidents/) 与 [复盘](https://sre.google/sre-book/postmortem-culture/) | 协调、运行、沟通及关注系统条件的复盘 | 15 | 故障处理和业务沟通需明确角色 | 按客户案例的单次切换即可证明备用系统总有效 |
| [Google SRE 值班](https://sre.google/workbook/on-call/) 与 [重复运维](https://sre.google/sre-book/eliminating-toil/) | 值班准备、支持责任、运维容量与重复工作 | 16、17 | 已交付维护应进入团队容量与交接 | 教学工时安排是行业标准配置 |
| [BBVA 案例](https://openai.com/index/bbva/) | 公司及供应商对组织采用与效率的自述 | 3、16 | 采用与效率有各自指标口径 | 时间自述直接证明利润、因果或独立审计 |
| [Klarna 早期案例](https://openai.com/index/klarna/) | 发布时点、客服工作量与效果的发布方自述 | 3 | 工作量指标需要其时间及分母背景 | 岗位工作量等价必然代表实际裁员或兑现利润 |
| [TIME 案例](https://scale.com/customers/time) | 公开交付范围与项目期限说明 | 13 | 可以回读固定期限项目怎样描述范围 | 教学实验设计是 TIME 内部评测 |
| [Assembled 案例](https://claude.com/customers/assembled) | 供应商对故障切换与评测的案例叙述 | 15 | 可作为备用路径阅读线索 | 本书故障 JSON 和相对时间线来自客户日志 |
| [Datawhale 制造培训](https://fde100.datawhale.cn/cases/cases-009) | 社区发布的制造业培训任务叙述 | 16 | 可找到具体培训业务的自述例子 | 社区标签等同独立审计或其架构已全部公开 |

## 作者设计的教学工件

第 1、2 章用采购需求、物料、包装、价格和草稿对象推导系统边界与状态转换。采购例子为自主教学设计，未使用参考仓库中的客户故事或代码。第 4 章的责任表、ADR、第 11 至 18 章的访谈、验收、实验、灰度、日志、采用、容量与作品评分均为本书建议。

没有声称本分支的教学流程完成真实客户试点。最后一章的程序由其它协作者提供，其实际支持能力需另行测试。本组章节不依赖该程序提供真实模型调用或完整生产部署。

## 数学算例核对

- 第 1 章的五项独立依赖，0.999^5 约为 0.995，只解释简化组合效应，明确独立假设与真实相关故障的限制。
- 第 2 章的稳定流程，40 单每天乘以 2 工作日，平均在途约 80 单。容量示例 48/50=0.96，不作确定等待时间预测。
- 第 3 章的月释放时间，4000×(16-7-0.15×12)/60=480 小时。转人工率改为 0.5 时得到 200 小时；再将 N 改为 800 得到 40 小时。
- 第 3 章的教学 token 费用，4000×3×(3000×2+600×10)/1000000=144 元。单价不是供应商报价。
- 第 3 章时间成本等价值单独列示，未当作已减少工资或利润。建设分摊及财务确认边界在正文明确说明。
- 第 15 章错误预算速率，教学不合格比例 0.10 除以允许比例 0.01 等于 10，不设通用告警阈值。
- 第 16 章教学漏斗，40/100=40%，40/50=80%。用户与任务、不同分母分开。
- 第 17 章工时收益，n×15-40-20。n 为 3、5、8 时分别为 -15、15、60 小时，没有宣称财务利润。

## 验证记录

已逐章运行 human-writing 的检查器。硬禁标点、固定翻案句及绝对黑话均为零。教程表格和枚举按读者实施需求保留，几处三连句已改写。句长接近的警告保留为人工审阅项，不为追求节奏而制造不必要的口语或假经历。

本组章节没有执行外部业务写入，没有制作客户效果数据，没有删除原版资料。全书版式、PDF、来源总账、发布及伴随项目验证由主任务统一完成。

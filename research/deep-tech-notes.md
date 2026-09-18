# 深入实战版技术研究与复算记录

核对日期为 2026-09-18，对应第 5 至 10 章。李博杰的 AI Agent 开源书用于检查主题覆盖，技术机制分别回读一手论文与官方文档。正文、采购示例、公式参数、SQL 和 Python 代码独立编写，没有复制参考书的段落或实现。

## 来源与适用范围

| 来源 | 支持的内容 | 本书保留的边界 |
| --- | --- | --- |
| [AI Agent 开源书](https://github.com/bojieli/ai-agent-book)及其 Apache-2.0 许可 | 上下文、工具、运行控制、评测的阅读线索 | 不沿用正文、代码或特殊表达 |
| [Transformer 论文](https://arxiv.org/abs/1706.03762) | 缩放点积注意力与模型结构 | 不推定所有当前商业模型的内部结构 |
| [PagedAttention 论文](https://arxiv.org/abs/2309.06180)与 [KV 文档](https://huggingface.co/docs/transformers/main/en/kv_cache) | 历史状态、缓存管理与资源取舍 | 显存公式仅计算指定 KV 张量，非整进程占用 |
| [长上下文位置研究](https://arxiv.org/abs/2307.03172) | 被测模型与任务的证据位置效应 | 不外推为所有模型的固定缺陷 |
| [PostgreSQL 隔离文档](https://www.postgresql.org/docs/current/transaction-iso.html) | 事务隔离、并发冲突与重试 | 隔离保证取决于具体引擎与模式 |
| [SQLite 事务](https://www.sqlite.org/lang_transaction.html) | 本地事务与写入边界 | 不自动保证外部 ERP 的幂等与一致性 |
| [RAG 论文](https://arxiv.org/abs/2005.11401) | 检索与生成结合 | 本书采用独立的企业证据路径设计 |
| [RRF 原论文](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf)与 [Microsoft 排名说明](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking) | 基于排名倒数融合 | 参数 60 只是常用起点，非普适最优配置 |
| [Elasticsearch BM25](https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity) | 词频饱和、长度归一化及该实现默认参数 | 编号分词与参数需在本地任务集检验 |
| [MCP 架构](https://modelcontextprotocol.io/docs/learn/architecture) | host、client、server 与连接责任 | 本轮文档重定向到 2026-07-28，实施时固定版本 |
| [NIST 比例区间](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm) | 二项比例与 Wilson 区间 | 假设采样单位合理，不证明安全攻击零风险 |
| [模型评审研究](https://arxiv.org/abs/2306.05685)与 [G-Eval](https://arxiv.org/abs/2303.16634) | 评分能力及偏差检查线索 | 本地 rubric、语言与任务仍需专家校准 |
| [OWASP 授权建议](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)及 [交易授权](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html) | 默认拒绝、对象权限和具体内容批准 | 不等于企业已完成法律合规或独立安全审计 |
| [CWE 367](https://cwe.mitre.org/data/definitions/367.html) | 检查与使用之间的状态变化 | 执行时需要实际原子边界或明确残余风险 |

## 关键演算的复核

- KV 教学参数为 32 层、8 个 KV 头、128 维、16384 token、每元素 2 字节。公式结果为 2147483648 字节，即 2 GiB，未包含权重及其他工作区。
- 32768 token 窗口中的示例证据预算为 20968；工作坊 16384 token 窗口中的证据预算为 8684。
- 教学计费中 6000 输入 token、800 输出 token，假设百万 token 单价为 2 与 8，模型部分为 0.0184 货币单位。
- BM25 算例采用 IDF 为 2、k1 为 1.2、b 为 0.75。同平均长度时，词频 1、2、10 的贡献分别为 2、2.75、约 3.93；双倍长度且词频为 1 时约为 1.42。
- RRF 原创两份名单融合后为 B、A、D、C，代码含结果断言。
- Wilson 算例在 90/100、z 为 1.96 时下界为 0.8256327，上界为 0.9447715。集中执行发现初稿下界断言误写为约 0.84，已同时修正代码和正文。
- HMAC 使用故意公开的教学密钥，只展示完整性绑定，不能证明认证、审批资格、密钥安全或防伪能力。

## 验证方式

章节 Python 围栏全部接受语法校验；标记 `python runnable` 的独立样例实际执行，并检查结果断言。需要外部连接或既有状态的代码明确作为片段，不声称可以独立启动完整系统。

全书伴随工程另以 31 项内存数据库测试验收，模型与 ERP 扩展未实现，不将规则规划器的成功解释为模型质量实测。正式接入模型以后，应新增真实数据授权、调用状态、任务质量、成本与接口故障测试。

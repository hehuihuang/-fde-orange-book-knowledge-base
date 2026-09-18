# 第 27 章研究与实测记录

## 来源与事实边界

工业物料选题参考 [Datawhale 公开案例](https://fde100.datawhale.cn/cases/cases-024)。该材料属于项目自述，证据等级 C。没有获得原客户完整数据、内部权限规则或独立效果审计。

本章租户、人员、物料、包装、价格、供应商、额度和权限全部为原创合成教学数据，证据等级 D。代码不是该案例复原，也没有复制用户参考仓库中的代码或章节表达。

技术第一方资料用于核验内存 SQLite、参数绑定、显式事务、授权检查和交易内容绑定。

- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [SQLite 事务](https://www.sqlite.org/lang_transaction.html)
- [SQLite 约束](https://www.sqlite.org/lang_conflict.html)
- [OWASP 授权](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP 交易授权](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html)

用户三个技术与理论仓库仅用于主题检视。项目组织与工程示例独立设计，不移植其全文、代码或独有框架。

## 已运行

2026 年 9 月 18 日执行下列命令，演示输出与 31 项单元测试全部通过。

```bash
python3 examples/material_assistant/material_assistant.py
python3 -m unittest discover -s examples/material_assistant -v
```

确认一盒碳钢轴承换算为十个，总额 25000 分，初始额度 100000 分，确认后余额 75000 分。相同幂等请求返回相同订单，未再次扣减额度。订单、授权标识随机，生成时间取系统时间，输出不要求逐字相同。

首次测试确实出现两个失败，同型号澄清与完整演示。别名使碳钢候选得分 130，不锈钢候选 100，旧的仅依赖分差规则没有要求澄清。修复增加同一规范化型号多候选独立触发规则，保留此组数据和全角型号回归输入。

后续复核补充历史回执的当前品类权限检查，新增第 31 项用例。失去品类访问后不能返回旧订单内容，但原订单和额度变更仍保留。

## 重要限制

未实现登录或 HTTP。服务参数中的身份代表可信入口注入的上下文，不能直接接受模型或客户端自报身份。跨租户测试检查已注入身份下的对象隔离，不声称实现认证层。

没有模型调用、网络、真实 ERP、供应商下单、库存预留或真实采购效果。没有多进程并发、数据库恢复和真实用户采用记录。内存回执在进程退出后消失，不构成生产分布式幂等保证。

摘要用于内容变化检测，不证明身份，也不防特权数据库篡改。成功事件与业务事务一起提交，失败请求未进入独立安全日志。审计表不是防篡改平台。

正文的 ERP 发件箱、多明细采购、主数据治理、报价有效期和生产演练属于扩展建议，未包含在已通过测试中。


tool use是agent跨越语言模型和真实世界边界的执行通道，LLM本身只输出token，所有对外部状态的读取、修改等都是通过工具调用完成，所有也是agent中风险密度最高的环节  

<img width="705" height="217" alt="image" src="https://github.com/user-attachments/assets/13db6f14-a7df-4618-8c65-1b289279762a" />  

<img width="661" height="496" alt="image" src="https://github.com/user-attachments/assets/07df287d-f017-40eb-82c6-0d9b1b77ff6e" />  

解决思路  
* 工具描述是prompt工程，不是文档
  * description写 做什么+何时用+何时不用+典型例子，不是写实现细节
  * 参数schema用JSON Schema严格约束（enum，format，required，pattern）
  * 名字本身就是文档：search_internal_docs远好于tool_a
  * A/B测不同描述对对LLM选择准确率的影响，这是隐藏的高ROI优化点
 
* 工具数量控制 + 动态加载
  * 硬上限：单次prompt里暴露不多于20个工具，超过准确率明显下降
  * 分组+路由：先用一个轻量分类器/LLM选工具组，再把对应组的工具暴露给actor
  * 检索式工具加载（RAG-for-tools）：根据用户query检索相关工具子集动态注入prompt
  * 把复合工具封装好替代多个原子工具
* 用schema强校验输入输出
  * 输入：function calling / structured output 已是标配，所有参数必须schema校验，错误信息要可执行（missing required field region）
  * 输出：工具返回也要schema化，避免自由文本里夹错误码
  * TypeScript, Pydantic，Zod自动生成schema，单一真相源

* 错误信息要可学习
  * 工具失败时错误信息要让LLM能据此修正
  * 把错误信息当prompt的一部分设计，它直接决定下一轮LLM能不能改对
 
* 输出截断 + 分页 + 摘要
  * 大输出默认截断，附带“完整结果已存储到X，可用read_artifact查看”
  * 分页接口 让LLM按需取
  * 巨型输出走artifact模式，工具返回引用ID而非内容，下个工具用ID消费
  * claude code，cursor都用这个模式管file_read，shell输出
 
* 副作用分级+权限分层
  * read：自动放行，write：默认放行，可配置确认，inreversible（删数据、付款、外发）：强制human-in-the-loop审批
  * 每个工具配最小权限token，避免一把钥匙开所有锁
 
* 沙箱化高风险执行
  * 代码执行用docker/Firecracker/E2B/Modal Sandbox
  * shell命令限制cwd，环境变量，网络
  * 文件操作限定路径白名单
  * 从设计上让工具无法做超越范围的事，而不是依赖LLM自觉
* 幂等性+缓存
  * 只读工具按（name，args_hash）缓存，避免重复调用
  * 写工具支持idempotency key，重试不会重复扣款、重复发邮件
  * 重要操作日志化，可回访可审计
* 超时+重试+熔断
  * 每个工具配默认超时，可在调用时覆盖
  * 网络错误，5xx走指数退避重试，4xx不重试
  * 熔断：连续N次失败的工具临时下线防止agent死循环消耗资源
* 并行调用和依赖管理
  * 工具调用之间要有显式依赖图DAG，无依赖的并行执行
  * 并行写资源要加锁或拒绝，让LLM改成串行
* 全链路trace
  * 每次工具调用记录：入参，出参，耗时，token消耗，触发它的llm输出+上下文hash，失败原因，重试次数，用OpenTelemetryGenAI语义约定，traceID串起整个agent链路
* 防prompt injection
  * 工具返回内容视为不可信数据，不是指令
  * 用分隔符/结构化字段隔离工具输出与系统指令
  * 高敏感工具，即使LLM想调，也要走独立confirm channel
  * 对MCP远程工具要做来源认证+输出审查

<img width="1238" height="469" alt="image" src="https://github.com/user-attachments/assets/63bb1828-9ff6-4f2d-9ce0-62d4a39021cd" />  

<img width="1652" height="183" alt="image" src="https://github.com/user-attachments/assets/3ac7a03b-35d5-4496-a314-5c68e17eb662" />  

**一句话经验：好的 tool use 系统不是"给 LLM 更多工具"，而是 "让 LLM 在每个时刻只看到该看到的工具，按 schema 调用，按预算执行，按权限放行，按 trace 留痕" —— 工具描述当 prompt 优化、错误信息当训练信号、副作用当风险等级、输出当资产管理。Agent的天花板，往往不在模型，而在工具系统的工程深度**


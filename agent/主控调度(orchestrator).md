Orcherstrator是agent系统的控制面板，处于用户与执行单元（llm，工具，sug-agent）之间，承担：  
* 任务分解和路由：把用户意图拆成子任务，决定交给哪个agent/工具/模型
* 状态与上下文管理：维护对话历史，中间结果，记忆，context window预算
* 控制流：串行/并行调度，循环，条件分支，重试，超时
* 协议转换：在LLM输出（自然语言、json）与工具调用，sub-agent输入间做格式适配
* 可观测与治理：日志，追踪，token计费，权限校验，human-in-the-loop

典型形态  
* 单agent内的ReAct循环
* Supervisor-Worker（主从）
* Hierarchical（分层）
* Graph（如LangGraph）
* Event-driven（消息总线）

主要痛点  
* 上下文爆炸：子agent结果回灌agent，token飙升，成本不可控，信息相互污染
* 决策不稳定：LLM做路由、规划时漂移，同样输入产出不同子任务划分、难复现、难测试
* 错误传播：链路深时一个子步骤偏差被层层放大，最终结果与意图无关
* 并行难：子任务之间隐含依赖（共享文件，状态），并行后冲突，重复劳动
* 可观测差：多层嵌套调用，日志散乱，出问题难定位是prompt，工具调用还是路由的问题
* 状态持久化：长流程中断后无法恢复，记忆、检查点设计缺失
* 权限与安全：子agent越权调用工具，用户授权范围被扩大
* 成本不可控：自由ReAct死循环、无预算约束

解决思路  
* 用结构换自由
  * 能用确定性流程（DAG，状态机，workflow）就别让llm自由plan，把llm限制在节点内做局部决策，全局拓扑由代码定义（langgraph、temporal， 自研FSM）
* 上下文隔离+摘要回传
  * sub-agent用独立context，只把结构化结果回主agent，不回原始过程，
* 显式契约
  * 每个agent/工具定义输入输出schema（JSON schema/pydantic）,orchestrator只做边界校验，把自然语言协调降到最低
* 控制循环要有刹车
  * 最大步数、token预算、wall-clock超时、重复检测、三选一兜底，ReAct必备
* 可观测一等公民
  * 全链路trace（OpenTelemetry/LangSmith/Langfuse）, 每次llm调用，工具调用，路由决策都打点，traceid 串起多agent
* 检查点（checkpoint）与重放
  * 长流程把状态序列化到外部存储，失败从最近的checkpoint恢复，同时支持“在某步骤改输入重放”，调试和评估都靠他
* 评估驱动
  * 给orchestrator本身建评测集（路由正确率，子任务划分质量，端到端任务完成率），改prompt，改拓扑前后跑回归，避免拍脑袋
* 权限分层
  * 工具白名单按agent维度配置，高风险操作（比如写-删-外发）走human-in-the-loop审批节点

工业界主流的实现方式  
<img width="928" height="322" alt="image" src="https://github.com/user-attachments/assets/d271cf4a-1ade-4f93-ad32-73745064a81c" />  

工业界趋势  
1、从自由ReAct退回到半结构化工作流，langgraph，workflow，temporal全是这个方向，让LLM在节点内做事，不让他决定流程拓扑  
2、sub-agent隔离context称为标配，主控只看摘要，原始过程留在sub-agent，避免上下文爆炸  
3、结构化输出+schema校验 替代字符串parsing， pydantic，json schema， function calling是边界契约  
4、持久化工作流引擎下沉，复杂任务用Temporal这类做durable execution，AI框架跑在他上面  
5、可观测先行，Langfuse、LangSmith，Arize Phoenix，OpenTelemetry GenAI语义约定成为生产前置条件  
6、评估驱动迭代，orchestrator有回归测试集，改动靠数据说话  
一句话总结：生产级orchestrator=传统工作流引擎+LLM节点+结构化契约+全链路trace，把ai部分关进笼子里，把工程不分做扎实



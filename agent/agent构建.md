
**构建企业级Agentic Workflow的三大黄金法则**  
* Never Trust LLM Unchecked（永远不信任无约束的大模型）
  * 用硬编码状态机限定边界
  * 用Pydantic约束输入输出
  * 用护栏网拦截风险
* Design For Failure(为失败而设计)
  * 预设超时重试、指数退避、模型降级策略（大模型-》小模型-》规则）
  * 基于checkpoint的崩溃恢复
* Observability Above All（可观测性高于一切）
  * 把每一次工具调用和思考轨迹都当做生产日志留存，只有看得清，才能调的好

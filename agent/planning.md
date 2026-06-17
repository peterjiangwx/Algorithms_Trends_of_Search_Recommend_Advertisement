
planning是Agent把用户意图翻译成可执行步骤序列的环节，处于理解之后，执行之前，和orchestrator的关系如下：  
- planning决定 做什么，按什么顺序做 （what&order）
- Orchestrator决定 怎么调度、谁来执行、出错怎么办（how&control）

<img width="591" height="651" alt="image" src="https://github.com/user-attachments/assets/108a4b0c-827b-4244-94af-3d8d72f9b887" />  

痛点解决思路  
- 按任务复杂度选规划策略，不要一刀切
  * 简单问答，单工具任务：不要planner，直接ReAct或者函数调用
  * 多步但线性：DAG、工作流模板，把“计划”变成“参数化模板填空”
  * 真开放任务：plan&execute+replan
  * 复杂度路由：先用一个轻量LLM判断任务等级，再选不同路径
- 用结构化输出约束规划格式
  * 强制schema，避免幻觉工具名，依赖关系显式化
- 先验证再执行（Plan critic 、 self-refine）
  * plan出规划 -> critic模型/规则审查（工具是否存在，参数是否齐全，是否回答原问题）-> 不通过重规划
- 显式重规划触发条件，避免震荡
  * 设定重规划预算（比如几次）
  * 重规划触发条件结构化（比如触发了什么错误类型），每种走不同的分支
  * 重规划将已尝试且失败的方案显式写入prompt，避免犯同样的错误
- 维护显式世界状态
  * 每步执行后更新一个WorldState对象（已知事实，当前文件状态，已获取数据）
  * 重规划时，基于最新state而非原始query，避免基于幻想做计划
- 分层规划+局部replan
  * 高层目标稳定，仅在低层步骤失败时局部replan，不动全局计划
- 计划即代码（code-as-plan）
  * llm直接生成python代码，交给沙箱执行
  * 天然支持代码逻辑和错误处理
- 把plan和todo list分开
- 评估驱动的planner迭代
- 失败兜底
  * 每步设最大重试次数，超过阈值，降级到更简单方案或者human-in-the-loop
  * 长任务做checkpoint，失败从最近成功步骤恢复，而不是整个replan

<img width="984" height="382" alt="image" src="https://github.com/user-attachments/assets/d3a50b5a-4460-4fa7-bad7-270ef8d12a0e" />  

工业界共识和趋势  
- 全局静态plan在生产里基本不用，现实任务环境会变，纯plan-and-execute太脆，主流是plan + replan + 局部修正
- 代码即计划正在崛起，json计划表达能力有限（不好写循环，条件，异常处理），代码天然胜任，huggingface数据，在多倍benchmark上，CodeAct比Json plan高10-20%的成功率
- Todo list是用户体验标配，暴露todo list给用户看进度，本质是把规划显性化来建立信任
- 分层规划成为复杂agent的标配，单层plan在20+步任务上容易漂移，分层后高层稳定，低层可重规划
- Planner与Executor用不同模型，planner用强模型保证规划质量，executor用便宜模型跑批量步骤，成本和效果平衡的关键技巧
- 少规划胜过多规划，经验上，简单任务直接function calling，不引入planner，端到端成功率更高，延迟更低，有疑问时先不加planner
- plan评测正在标准化，

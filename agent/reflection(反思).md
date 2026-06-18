
**反思**  
反思是agent对自己的输出、过程、结果进行评估，批判和修正的环节，在agent的流程中不是处在一个固定的位置，而是一种可以处在多出的元认知机制  
<img width="597" height="149" alt="image" src="https://github.com/user-attachments/assets/01172cd9-329b-4568-b0f8-96f20cf9a060" />  
与相邻概念的边界：  
* vs planning：planner决定做什么，reflection评估做的对不对，好不好
* vs verification：verification多指外部规则，测试校验，reflection多指llm自己批判自己
* vs memory：reflection的产物可以写进memory形成长期经验

典型范式：  
<img width="828" height="238" alt="image" src="https://github.com/user-attachments/assets/9559323d-90dd-4cbd-bfa0-244f3eb7bf34" />  

主要痛点：  
<img width="560" height="345" alt="image" src="https://github.com/user-attachments/assets/e6bd284d-b49b-45b6-9de3-026897891b47" />  

解决思路：  
* 用外部信号代替自我反思
  * 最有效的反思=外部ground truth反馈：编译错误，单测失败，sql报错，api返回4XX，用户拒绝。有外部信号时不要让llm凭空反思，拿运行结果当critic会更准
* 显式反思维度（Rubric）  
  <img width="405" height="132" alt="image" src="https://github.com/user-attachments/assets/3e90cf00-8e04-4811-88c3-fb6c0843f9a2" />

* 用独立critic模型，避免self-bias
  * actor用sonnet、haiku，critic用opus或者不同家族模型
  * critic只看输入和输出，不看actor的思维过程，避免被合理化叙述带跑
  * 对关键节点才上critic，节省成本
* 收敛准则要硬  
  <img width="507" height="132" alt="image" src="https://github.com/user-attachments/assets/73a52f14-9d5a-49f6-8a8d-209187e44cb6" />
* 选择性触发，不要默认开启
  * 反思贵且不一定有用，仅在以下情况触发：
    * 工具调用返回error
    * 输出未通过schema检验
    * 自评置信度地域阈值
    * 任务被标记为高风险高价值
    * 用户显式要求再想想
  * 普通路径直接走，不绕反思
* 反思震荡检测
  * 保留最近K轮答案的hash/embedding，发现循环立即跳出，返回当前最优解+标记不确定性，让用户决定
* 反思要可执行
  * 强制critic输出修改指定而非评论
  * 把critic的输出做成可被actor直接消费的patch diff 工具调用 建议
* 跨任务反思，经验沉淀
  * 单次任务结束，提炼教训写入长期memory
  * 下次同类任务把相关经验注入system prompt，把反思从运行时成本变成离线资产，reflection的核心贡献就是这个
* 与外部验证组合（verifier-guided reflection）
  * 代码-> 跑单测-> 失败信息喂回给reflection
  * sql-> explain->dry-run ->错误喂回
  * 文档-》拼写/事实校验-> 标注问题喂回
  * 数学-> 符号验算/python跑一遍
* calibration（置信度校准）
  * 让模型同时输出 答案+置信度，反思只对低置信度结果触发，校准好的模型可以减少50%的不必要反思，需要在评测集上专门训练校准

<img width="1030" height="442" alt="image" src="https://github.com/user-attachments/assets/bdfe0f60-4db2-4cce-98dc-933128e29f90" />  

* 工业界共识和趋势
  <img width="1710" height="133" alt="image" src="https://github.com/user-attachments/assets/1b055bd1-54f1-4343-aa81-cfca2c02017b" />  

**一句话经验：好的 reflection 系统不是"让 LLM 多想几遍"，而是 "让正确的信号在正确的时机进入正确的修正路径"——外部 verifier 给确定性，独立 critic 抗 self-bias，硬收敛准则防失控，结构化 rubric
  防空洞，跨任务记忆防重犯。默认关闭，按需开启，永远评测**





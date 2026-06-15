**什么是agent**  
架构特征
<img width="690" height="808" alt="image" src="https://github.com/user-attachments/assets/68a8d1a2-c002-40fa-9bb8-7a97381b5bba" />
* 核心能力  
  * 自主规划：llm自主分解任务，决定执行步骤
  * 调用工具：根据需要自主抽取参数和选择合适的工具
  * 反馈循环：执行后观察结果，动态调整策略
  * 长时任务：可以持续执行复杂的多步骤任务
* agent loop：感知-思考-行动-反馈
* 技术实现范式
  目前业界主流的实现范式
  * ReAct(Reasoning+Acting)
    核心思想：让LLM交替进行思考和行动
    优点：推理过程透明，调试方便
    缺点：每一步都要llm推理，效率低
  * Plan-And-Execute
    核心思想：先制定完整计划，再按计划逐步执行
    优点：复杂任务处理有条理
    缺点：一旦制定计划，就很难改，缺乏灵活性
  * Multi-Agent
    核心思想：多个专业agent分工协作
    优点：专业分工，复杂任务处理能力强
    缺点：系统复杂度高，协调成本大
一般agent不需要对模型进行微调，除非对于专业领域和特殊格式有强烈需求
* agent能力提升的正确路径
  * level1：提示工程，优化system prompt，工具描述，few-shot示例
  * level2：工具生态，丰富工具集，优化工具接口设计和工具组合能力
  * level3：RAG，构建高质量知识库，优化检索策略，知识更新机制
  * level4：模型微调，特定领域术语理解，稳定输出格式，成本优化
* 构建一个完整的agent系统需要的模块
  * agent运行框架，langGraph，AutoGPT，CrewAI，Hermes
  * 工具系统，工具定义（mcp，function calling），工具注册中心，调用指引，错误处理与重试
  * 记忆系统，短期记忆、长期记忆、工作记忆
  * 感知增强，多模态输入处理，RAG，联网搜索
  * 安全控制，输入安全（注入检测），执行安全（权限控制），输出安全（幻觉检测）
**agent技术架构的六大核心模块**  
从成功实现的视角看一个成熟的agent是一套精密的系统工程，它由六大核心模块协作，共同构建了一个完整的智能闭环  
* 模块1 感知
  <img width="1505" height="1006" alt="image" src="https://github.com/user-attachments/assets/35d651b5-2907-48e2-affd-768eda79971c" />
  感知模块通过多来源、多模块，对数据进行预处理，完成去噪和标准化后，给到llm  
* 模块2 llm(大模型)
  <img width="1494" height="1022" alt="image" src="https://github.com/user-attachments/assets/199218e3-fc3a-4f41-8507-6016a853e5f1" />
  这是agent的决策系统，引入了思维连的推理机制，对于一个复杂任务，llm会经过任务拆解，规划和决策
* 模块3 执行
  <img width="999" height="668" alt="image" src="https://github.com/user-attachments/assets/d458ea65-1fdc-4301-a890-7954107adba2" />
  通过将自然语言决策转为精准的计算机指令，通过预定于的tool schema构建参数、调用外部api、运行脚本或者插件，一个优秀的执行系统必须具有高度的鲁棒性，以面对外部各种不确定性，
  为了确定执行的可靠性，工程设计上一般会幂等设计和退避重试策略，这意味着即使网络波动导致请求重试，系统也能保证结果的一致性，遇到超时也会智能重试，甚至在关键时刻引入人工确认
* 模块4 记忆管理
  <img width="992" height="649" alt="image" src="https://github.com/user-attachments/assets/d17b9688-08b3-41a0-8e0f-6aee06024271" />
  <img width="1004" height="675" alt="image" src="https://github.com/user-attachments/assets/8c69699a-e631-4f6d-be26-185e7c3a8f71" />
  成熟的agent拥有完善的分层记忆体系，包括当前上下文的工作记忆、保存近期交互记录的短期记忆、以及存储行业知识，用户偏好和业务事实的长期记忆
  在技术底层，通常通过向量数据库和知识图谱的结合来实现，向量数据库擅长模糊检索，能从海量的非结构化文档或对话历史中找到相似片段，而知识图谱像一张关系网，这种记忆系统实现了RAG模式，让
  智能体在做决策前查阅知识库，避免模型出现幻觉
* 模块5 反馈优化/反思
  <img width="995" height="673" alt="image" src="https://github.com/user-attachments/assets/ee3d65f8-c1b7-422b-b041-85dcc8b7a3b4" />
  反馈优化是agent实现自我进化的关键一环，这一模块赋予了智能体反思的能力，在每次任务结束后，会启动自我评估机制：结果是否达成目标，过程中是否有冗余步骤，哪个环节出问题，这种机制往往通过一个反思agent来实现，更高阶
  的进化则依赖强化学习

**参考文献**  
1、https://cloud.tencent.com/developer/article/2626356  
2、https://yingjiezhao.com/zh/articles/From-LLM-to-Agent-Architecture-Evolution/  

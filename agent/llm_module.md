
**LLM core**
llm是agent的大脑，在流程中承担推理、规划、决策、生成四大角色，也是所有其他模块的核心调用对象  
* 在agent流程中的位置  
  <img width="347" height="448" alt="image" src="https://github.com/user-attachments/assets/e498bab3-978a-4d8e-851d-6ef4edf44f04" />  
* llm core的四个角色
  * Reasoner(推理者)
    * 理解用户意图
    * 分析任务上下文
    * 推断下一步行动
  * Planner(规划者)
    * 拆解复杂任务
    * 生成子目标序列
  * Decider(决策者)
    * 决定调用哪个工具
    * 决定是否结束任务
    * 决定何时求助用户
  * Generator(生成者)
    * 生成自然语言回复
    * 生成结构化输出
    * 生成prompt给sub agent
* llm core的输入输出契约
  * Input
    * system prompt（人设、规则、约束）
    * conversation history （多轮对话历史）
    * Tools Schema （工具列表）
    * Retrieved Context （RAG、memory 召回）
    * User Query （当前请求）
  * Output
    * Reasoning Trace （思考过程，可选）
    * Tool call （工具调用决策）
    * Text Response (自然语言输出)
    * stop Reason（结束原因）
    * Token Usage（token消耗统计）
* LLM core的内部分层
  <img width="352" height="422" alt="image" src="https://github.com/user-attachments/assets/da5ab9e9-93ce-4c76-8c58-28728fc1f48f" />  
* LLM core的核心痛点全景以及对应解法
  * 1、性能与成本痛点
    * 延迟高：单次调用延迟高，流式才能勉强可用，多轮agent任务累积延迟严重
    * 成本失控：agent多步循环，缓存命中率低都会导致成本失控
    * context window局限：长会话超出token限制、长文档放不进去、超过被截断导致信息丢失
    * token浪费：重复system prompt，不必要的工具描述，冗余历史
    针对延迟高和成本失控的痛点  
    * 解法1：prompt cache
      * 原理：标识可缓存部分，服务端复用：system prompt，长rag上下文，工具schema列表
      * 关键设计：把不变部分前置，变化部分后置，5min TTL，关键热路径保持活跃
        <img width="464" height="260" alt="image" src="https://github.com/user-attachments/assets/5a61e675-40b3-4079-9065-5b0e817a7f04" />
    * 解法2：Model Routing（模型分级）
      * 按任务复杂度路由
        * 简单任务（分类、抽取、格式化）：-> claude haiku/deepseek/本地小模型
        * 中等任务 (一般推理)：-> claude sonnet/gpt-4o
        * 复杂任务（多步规划、代码）：-> claude opus/o1
    * 解法3：streaming（流式响应）
      * 不流式：等30s看完整结果，流式：100ms看第一个token，边生成边渲染
      * 副产品：早停机会，发现问题立马中断
    * 解法4：并行调用（独立llm调用并发）
      * 适用场景：多文档摘要、多分支评估、multi-agent同时思考
        <img width="289" height="66" alt="image" src="https://github.com/user-attachments/assets/ed5d454f-0e81-4687-8415-d298019e3e82" />
    * 解法5：batch api（异步批处理）
      * openai和anthropic都支持batch api
      * 适用：离线评估，数据生成，非交互场景
    针对context windows局限和token浪费的痛点解法  
    * 解法1：智能上下文压缩
      * 策略1：sliding window：保留最近N轮+最早system_prompt+关键milestone
      * 策略2：Hierarchical summarization：早起对话-》摘要-》摘要的摘要，类似MemGPT的虚拟context
      * 策略3：Selective Retention：LLM自己决定哪些消息保留全文，哪些进行摘要
        <img width="461" height="215" alt="image" src="https://github.com/user-attachments/assets/a7117f6d-2375-46d1-ab11-37e22afa977d" />
    * 解法2：Token Budget分配
      * 每次LLM提前预算分配：system prompt：1k，tools schema：1k，rag：2k，conversation：3k：response：1k
  * 2、可靠性与稳定性痛点
    * 模型幻觉：编造不存在的api，错误引用工具参数，自信给出错误答案
    * api不稳定：上游限流、服务端错误、超时
    * 输出格式不稳：json格式偶尔出错、字段名出错、必填字段缺失
    * 模型能力波动：不同温度设置导致输出差异大、模型版本升级带来regression
    输出可靠性  
    * 解法1：结构化输出（json mode、Function calling）
      <img width="352" height="362" alt="image" src="https://github.com/user-attachments/assets/6ecfcce6-5e41-4446-968d-7589eaeb0f1c" />
    * 解法2：约束解码（vllm/Outlines):在采样时直接限制token选择，保证输出符合grammer，regex，json schema
    * 解法3：重试和降级
      <img width="430" height="231" alt="image" src="https://github.com/user-attachments/assets/10058641-798d-470e-814a-04ff79fc5198" />

  * 3、决策与编排痛点
    * 工具选择错误：工具太多烟花、选了错的工具、该用工具时直接编答案
    * 参数填错：工具参数schema没有严格遵守，必填漏了，值类型错误
    * 死循环：重复调用同一工具、任务完成后还继续推理、不知道怎么停下来
    * 长程任务退化：多步后忘了初始目标、上下文越长输出质量越差、推理链条断了
    决策准确性
    * 解法1：工具描述精炼
      * 工具分组与动态加载：按场景注入相关工具子集，SkillRouter：先选skill，再展开tools
      * 工具描述优化：用自然语言示例，用few-shot演示参数，明确什么时候用这个工具
        <img width="473" height="145" alt="image" src="https://github.com/user-attachments/assets/3935ddf8-866b-434b-adbd-bcb2cd2ba4a1" />
    * 解法2：思维链（CoT）和显式Reasoning
      * 不带CoT：直接给答案，易出错
      * 带CoT（ReAct风格）
    * 解法3：自一致性
      * 对于关键决策点：采样N次，取多数票，成本翻倍，但关键决策点错误降低
    * 解法4：死循环检测
      <img width="448" height="222" alt="image" src="https://github.com/user-attachments/assets/6a595aa4-3ffe-422d-956a-ebe2885edee7" />

  * 4、工程与运维类痛点
    * 模型供应商深度绑定：代码深度依赖某家api、切换成本高
    * 调试困难：改动prompt行为大变，llm内部推理黑盒，难以定位问题在哪一步
    * 版本管理困难：prompt散落代码各处，模型版本、prompt版本耦合，上线回滚困难
    * 多模态接入不统一：多模块数据处理不一致，不同模型的multimodel接口差异
    * 解法1：Provider抽象层，解耦模型供应商
      <img width="573" height="120" alt="image" src="https://github.com/user-attachments/assets/32610a64-4876-4d1a-a8b9-803c56ee83cf" />
    * 解法2：标准化消息格式
      <img width="532" height="259" alt="image" src="https://github.com/user-attachments/assets/ccc637c6-ddcc-4cb9-a9b1-8e2b27217f99" />
    * 解法3：全链路Tracing
      <img width="523" height="262" alt="image" src="https://github.com/user-attachments/assets/e3a0374f-3d32-469a-a738-4520e9e28860" />
    * 解法4：prompt版本化
      <img width="371" height="204" alt="image" src="https://github.com/user-attachments/assets/2f7620b1-bb48-4081-9255-2ec3093f6319" />
    * 解法5：Replay&snapshot
      <img width="173" height="154" alt="image" src="https://github.com/user-attachments/assets/76607d7f-cae7-4b32-b075-8528cda47233" />
  * 5、安全和合规痛点
    * prompt injection：用户输入污染system prompt，工具结果中藏恶意指令，越权操作
    * 敏感信息泄露：内部数据被model学习，输出包含敏感信息
    * 越权调用：模型决定调用本不该有权限的工具，数据访问范围失控
    * 解法1：Prompt Injection防御
      <img width="419" height="306" alt="image" src="https://github.com/user-attachments/assets/e654bf8f-0b00-4bfd-bcb9-692d9d1b661e" />
    * 解法2：PII脱敏
      <img width="397" height="165" alt="image" src="https://github.com/user-attachments/assets/14969c18-fc5b-4a7f-a170-038098822427" />
    * 解法3：工具调用权限分级
      <img width="410" height="222" alt="image" src="https://github.com/user-attachments/assets/ebcc59a4-c10f-4537-b682-485af81b49b9" />  
<img width="511" height="916" alt="image" src="https://github.com/user-attachments/assets/28b87359-8ed7-4506-8202-f7a88cf6ddb6" />

不同规模的Agent的LLM core的演进路径  
* MVP阶段（最小可行产品），直接调用大模型sdk，
* 中期阶段（关键能力补齐）
  * provider抽象、Streaming、Retry&Fallback、Prompt cache、cost tracking、Json mode
* 生产级阶段（全方位）
  * Model router、context manager、middleware 链、Trace接入、prompt版本化、Safetye guard、replay&Eval、multi-provider容灾、自定义约束解码

最容易被忽视的关键痛点  
* 模型版本升级的regression
  * 应对：版本锁定，升级前回归测试，灰度切换
* tool use的善意失败
  * 痛点：llm看到工具失败就放弃，不重试也不换工具
  * 应对：工具描述里说明“失败时该做什么”，主循环加错误恢复策略，reflection模块介入
* 长system prompt的attention衰减
  * 痛点：system prompt太长，中间内容容易被忽略
  * 应对：关键约束放头部和尾部（primacy+recency），重要规则用强调标记（critical/must），定期把关键规则在user侧重申
* 多轮对话的角色漂移
  * 痛点：多轮对话后llm忘了自己是谁
  * 应对：关键节点强化system prompt，用“Reminder： You are。。。”中插、定期重置+摘要
**一句话总结**  
它的痛点可以归为四大类  
* 性能成本：延迟、成本、context限制 -> 用cache + Router + 压缩 + 流式 解决
* 可靠性：幻觉、格式错、api抖动 -> 用json mode + 重试 + 降级 + Reflection 解决
* 决策力：工具选错、死循环、长程退化 -> 用CoT + 工具精炼 + Loop Detector + Memory 解决
* 工程化：供应商绑定、调试难、安全 -> 用provider抽象 + Tracing + Prompt版本化 + 安全护栏 解决
设计LLM core 模块的核心原则  
* 抽象Provider：解耦模型，支持任意切换
* 中间件化：横切关注点（cache、cost、safety、trace），用装饰器组合
* 预算化管理：Token、成本、延迟都有显式预算
* 可观测性内建：每次调用都可trace，可replay，可eval
* 降级路径：任何环节失败都有兜底，不然agent卡死  

**一个成熟的LLM core模块，应该让上层agent完全不感知模型细节、provider差异、容错处理，他对外提供的就是一个稳定、可靠、可观测的智能调用接口，这是agent系统从原型走向生产的最关键的工程屏障**

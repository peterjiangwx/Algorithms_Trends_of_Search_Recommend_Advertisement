**Agent九层技术选型**

* L1、编排层
  * <img width="957" height="180" alt="image" src="https://github.com/user-attachments/assets/eae98860-97ad-43cb-8b43-e0e38160991f" />
  * LangGraph做agent的大脑（图+HITL+检查点），需要多小时、多天的case用Temporal Activity包括LangGraph子图

* L2、Model Gateway
  * <img width="676" height="203" alt="image" src="https://github.com/user-attachments/assets/cdce79f4-555b-4d8f-8d50-8ee481268451" />
  * 对于特别的行业，比如银行业：数据不出域强制要求->排除OpenRouter和部分Saas，首选LiteLLM自建+私有部署的国产模型

* L3、Vector DB/检索
  * <img width="652" height="202" alt="image" src="https://github.com/user-attachments/assets/2cfbd9a1-2363-446f-8363-f57a53d5f1f4" />
  * <img width="567" height="61" alt="image" src="https://github.com/user-attachments/assets/e685f757-3a1b-4489-afe8-0204d2740cd4" />
  * 检索框架：不用LlamaIndex/Haystack做重活，不灵活，条件允许的话自己写hybrid search（bm25+vector+rerank），Rerank用BGE-reranker-v2-m3，效果与cohere-rerank差不多
    
* L4、Observability（可观测）
  * <img width="593" height="236" alt="image" src="https://github.com/user-attachments/assets/8c0ea7dd-d271-4299-9f54-cd7c5a05bfbf" />
  * 所有LLM trace在Gateway打点、一次埋点全局可见，业务代码不用管trace

* L5、Evaluation
  * <img width="604" height="208" alt="image" src="https://github.com/user-attachments/assets/bc1949b2-a78f-43ed-a4ec-d33456b08f4d" />
  * langfuse Datasets + promptfoo + Ragas + GPT做LLM-as-judge

* L6、Guardrails
  * <img width="508" height="178" alt="image" src="https://github.com/user-attachments/assets/11a7c953-2550-4aff-91ec-d61ef0859b04" />
  * NeMo比较重，把Presidio + Prompt Guard + 自研规则作为Gateway的middleware插件，

* L7、HITL平台
  * <img width="474" height="150" alt="image" src="https://github.com/user-attachments/assets/2d42ddb1-ffa9-4a84-a388-a872365482c6" />
  * 起步就用slack，

* L8、Memory
  * <img width="620" height="126" alt="image" src="https://github.com/user-attachments/assets/7a1ad8a0-72e8-4721-b7bb-b0c10615c974" />
  * 自建

* L9、模型层
  * <img width="649" height="209" alt="image" src="https://github.com/user-attachments/assets/3ef2e453-c232-459f-8688-b937362325d5" />
  * 根据业务类型，分别调用不同的模型，来平衡成本


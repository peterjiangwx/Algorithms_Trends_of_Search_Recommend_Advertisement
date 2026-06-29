
**自然语言处理任务全景和工业界方法**  

* 文本分类类任务
  * 情感分析
    * 任务：判断文本情感极性（正、负、中性）或者细粒度情绪
    * 工业界方法
      * 传统方法：TF-IDF + LR/SVM，给评论实时打标
      * 预训练微调：bert微调，二分类或多分类头
      * 大模型方案：LLM zero-shot/few-shot prompting, 适合细粒度方面情况
      * 典型应用：电商评论分析（淘宝、京东）、舆情监控
  * 意图识别/文本分类
    * 工业界方法
      * 小流量场景：FastText、TextCNN（毫秒级响应）
      * 大流量场景：蒸馏后的bert-tiny/distillbert
      * 冷启动：LLM+prompt+rag检索分类例子
     
* 序列标注类任务
  * 命名实体识别
    * 任务：识别人名、地名、机构名、时间、产品等
    * 工业界方法
      * 主流：bert+crf、bert+span解码
      * 嵌套实体：W2NER、Global Pointer
      * 少样本、零样本：UIE、LLM+结构化输出
      * 多语言：mBert，xlm-r
  * 词性标注、分词
    * 现代方案多用bert端到端做联合任务

* 信息抽取类任务
  * 关系抽取、事件抽取
    * 工业界方法：
      * 管道式：先ner，再进行关系抽取（CasRel、TPLinker）
      * 联合抽取：UIE、GPLinker
      * 大模型时代：llm+function calling或者结构化输出三元组，配合规则后处理
  * 知识图谱构建
    * 抽取-》实体对齐（DeepMatcher、ditto）-》知识融合-》图存储（NebulaGraph）

* 文本匹配、语义检索
  * 语义相似度
    * 工业界方法：
      * 召回层：sentence-bert、simcse、bge、m3e（双塔、向量化后ann检索、faiss、milvus、vespa）
      * 精排层：cross-encoder（bert双句拼接打分）
      * 当前主流：bge-m3、qwen3-embedding、text-embedding-3用于rag
  * 搜索排序
    * 多阶段：召回（向量+bm25混合）-》粗排-》精排（LTR+Colbert+reranker）
    * 典型：各大搜索引擎
   
* 文本生成类任务
  * 机器翻译
    * 工业界方法：
      * 主流：transformer编解码
      * 大模型方案：
      * 评估：BLEU、comet、人工
  * 摘要生成
    * 抽取式：textrank、bert-ext
    * 生成式：bart，t5，gpt系列，claude
    * 长文档：map-reduce、滑窗+层次摘要
  * 对话系统
  * 代码生成
 
* 阅读理解、问答
  * 抽取式QA
    * bert-span起止预测，仍用于客服FQA、合同审阅
  * 开放域QA、RAG
    * 工业界范式
      * query-》改写+扩展-》向量+关键词混合检索-》rerank-》llm生成-》引用回链
      * 框架：langchain，llamaindex，dify，coze
      * 向量库：Milvus、pinecone
      * 企业落地：智能客服、文档回答、法律医疗助手
     
* 文本纠错改写
  * 拼写接错：soft-masked bert，MacBert-csc（输入法、搜索query纠错）
  * 语法纠错：
  * 风格改写：llm few-shot + 风格指令

* 多模态相关NLP任务
  <img width="554" height="43" alt="image" src="https://github.com/user-attachments/assets/b410ec3c-2dbd-43b0-92f9-581027a8e2d0" />

* 工业界整体技术演进
  <img width="479" height="175" alt="image" src="https://github.com/user-attachments/assets/2d28287d-e6ac-4765-a2dc-44e2016a8c07" />

* 当前工业界几个核心趋势
  <img width="616" height="97" alt="image" src="https://github.com/user-attachments/assets/a5a94097-0c90-45a9-907b-4c1cb8556765" />



  

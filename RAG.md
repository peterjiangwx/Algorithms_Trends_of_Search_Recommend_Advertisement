<img width="758" height="793" alt="image" src="https://github.com/user-attachments/assets/dda76c0d-0a2e-49d2-8a05-1a693bd91e18" />  </br>
# 1、llm痛点  
- 幻觉：llm会自信地编造假信息
- 时效性：llm的训练数据决定了模型的知识范围，对于最新的事件llm不知晓
- 私有数据盲区：由于隐私的问题，一般llm不了解企业内部的文档知识

# 2、rag的工作流程
- 索引：将不同的数据源，切分成小的语义块，存储到向量数据库
- 检索：根据query，从索引中检索目标语义块
- 生成：利用检索结果，构造上下文，进行生成

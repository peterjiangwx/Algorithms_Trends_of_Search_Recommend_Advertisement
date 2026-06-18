
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
  * 硬上限：单次prompt里

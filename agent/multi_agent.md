
<img width="1342" height="293" alt="image" src="https://github.com/user-attachments/assets/f11653ca-ee79-4645-a9e9-9f6d02d3dc8a" />  

<img width="1078" height="299" alt="image" src="https://github.com/user-attachments/assets/651b42f3-2494-40e0-ad4c-b7c686b19f2d" />  

<img width="639" height="497" alt="image" src="https://github.com/user-attachments/assets/d779ffe7-2835-4518-b27a-75462d2dfe09" />  

**解决思路**  
<img width="846" height="492" alt="image" src="https://github.com/user-attachments/assets/f2073de6-2844-4022-9f84-b48b8e1ae506" />  

<img width="618" height="375" alt="image" src="https://github.com/user-attachments/assets/94eb7ffb-4e32-46c9-b888-69b4a75bdf22" />  

<img width="598" height="354" alt="image" src="https://github.com/user-attachments/assets/ec0ba803-e2dc-42ce-b48c-616b373d7c7a" />

<img width="1264" height="442" alt="image" src="https://github.com/user-attachments/assets/e5840d37-5af4-4edd-9d78-1635e07c38ca" />

<img width="1559" height="195" alt="image" src="https://github.com/user-attachments/assets/658a2d61-c5c5-483b-b030-56a316739f20" />

**一句话经验：好的 multi-agent 系统不是"养一群 LLM 让它们自由协作"，而是 "用最少的 agent 数、最清晰的契约、最隔离的 context、最严格的预算，把单 agent 解决不了的复杂度切开处理" ——
  拆分有代价（token×N、延迟×N、复杂度×N²），只在收益证据明确时引入；引入后用工程手段（schema、trace、guardrail、budget）兜住下限。Multi-agent 是终极武器，不是默认选项**

query推荐，包括搜推中多个功能模块，query的自动补全，相关query推荐，文末query推荐，query纠错等

1、自动补全

从数据处理流程上来看，搜索引擎的自动补全模块可以看成是一个小的搜索引擎，也包括检索召回模块以及排序模块，召回模块根据用户输入的prefix，从query索引库中召回候选query集合，排序模块可以分为粗排和精排，粗排可以根据一些简单的query纬度特征进行规则排序，精排可以利用模型进行学习，以便更好地提升用户点击率和满意度，降低用户的输入成本

2、长尾前缀问题
传统的方法是通过trie树检索的方式，从历史query数据集中查找满足前缀匹配的候选query集合，但是不是所有前缀都能在历史query中找到，这个时候为了扩大召回覆盖，就需要考虑其他方法，

其中一种方法就是后缀匹配，后缀匹配可以根据业务自身的需求进行调整，比如只对行业实体的后缀补充到query集合中进行构建trie树，利用prefix的最后一个词在trie树中查找。
还有就是通过seq2seq、encoder&decoder模型来进行query补全

3、排序
传统的机器学习模型，比如树模型，通过计算前缀，候选query，用户信息，以及前缀&query对特征，统计特征进行排序
深度学习模型进行排序
基于用户对query的reformulate，session，历史行为数据进行个性化排序


参考文献：

1、https://ceur-ws.org/Vol-3784/short5.pdf

2、https://www.microsoft.com/en-us/research/wp-content/uploads/2022/07/gupta22_ijcai_slides.pdf

3、https://arxiv.org/pdf/2108.04976

4、https://dl.acm.org/doi/pdf/10.1145/2806416.2806599

5、https://www.themoonlight.io/paper/bb45f0e9-db7c-4e85-a481-0cdd60a6430c

6、https://archives.iw3c2.org/www2014/proceedings/proceedings/p971.pdf

7、https://dl.acm.org/doi/pdf/10.1145/1963405.1963424

8、https://staff.fnwi.uva.nl/m.derijke/wp-content/papercite-data/pdf/cai-survey-2016.pdf

9、https://cloud.tencent.com/developer/article/1352701

10、https://www.yuan-meng.com/posts/autocomplete/

11、https://dl.acm.org/doi/pdf/10.1145/2484028.2484076

12、https://arxiv.org/pdf/2403.02609

13、https://aclanthology.org/P18-2111.pdf

# rag
主要包含rag流程中的ragas评价代码，实现评价并可视化
# 主要评估指标
## Context Precision（上下文精度）
检索出来的内容里，真正有用、跟问题相关的比例，**准不准**
## Context Recall（上下召回率）
回答问题必须用到的关键信息，有多少被检索到了，**全不全**
## Faithfulness（忠实度）
答案只说检索到的内容，**不瞎编**
## Answer Relevancy（答案相关性）
答案是不是直接回答问题，**不跑题**
## Answer Correctness（答案正确性）
答案**对不对**

# 运行说明
- RAG/_QA 读取
- RAG/_MAIN 执行

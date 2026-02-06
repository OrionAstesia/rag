# 根据中间文件，组织成四个大列表
# 输出中间文件：process-structured_data.json

import re
import json
import os


def extract_fields_from_file(file_path):
    """
    从处理后的文件中提取所有字段并组织成四个大列表
    """
    questions = []
    answers = []
    contexts = []
    ground_truths = []

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：文件 '{file_path}' 不存在")
        return None

    # 读取文件内容
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 使用正则表达式分割数据块
    blocks = re.split(r"-{100,}", content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # 提取问题
        question_match = re.search(r"(\d+\.问题：.*?)(?=\n|$)", block)
        if question_match:
            question = question_match.group(1).strip()
            question = re.sub(r"^\d+\.\s*问题：", "", question)  # 去掉开头的"x.问题："
            questions.append(question)
        else:
            questions.append("")
            print("警告: 未找到问题部分")

        # 提取实际答案
        answer_match = re.search(
            r"实际答案:(.*?)(?=整合上下文|参考答案|\n|$)", block, re.DOTALL
        )
        if answer_match:
            answer = answer_match.group(1).strip()
            answers.append(answer)
        else:
            answers.append("")
            print("警告: 未找到实际答案部分")

        # 提取整合上下文
        context_match = re.search(
            r"整合上下文:(.*?)(?=参考答案|\n|$)", block, re.DOTALL
        )
        if context_match:
            raw_text = context_match.group(1).strip()
            context = [c.strip() for c in raw_text.split(",") if c.strip()]
            contexts.append(context)
        else:
            contexts.append("")
            print("警告: 未找到整合上下文部分")

        # 提取参考答案
        truth_match = re.search(r"参考答案:(.*?)(?=\n|$)", block, re.DOTALL)
        if truth_match:
            truth = truth_match.group(1).strip()
            truth = re.sub(
                r"（[^）]*?\d+[^）]*?）", "", truth
            )  # 去掉类似“（见表2）”的内容
            ground_truths.append(truth)
        else:
            ground_truths.append("")
            print("警告: 未找到参考答案部分")

    # 构建结果字典
    result = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }

    return result


def save_structured_data(data, output_file):
    """
    将结构化数据保存到文件
    """
    # 准备输出内容
    output_lines = []

    # 添加questions部分
    output_lines.append("question: [")
    for i, question in enumerate(data["question"]):
        prefix = " " * 4  # 4空格缩进
        question_clean = re.sub(
            r"^\s*\d+\.\s*问题：", "", question
        )  # 去掉开头的"x.问题："
        output_lines.append(
            f'{prefix}"{question_clean}"'
            + ("," if i < len(data["question"]) - 1 else "")
        )
    output_lines.append("]")

    # 添加answers部分
    output_lines.append("\nanswers: [")
    for i, answer in enumerate(data["answer"]):
        prefix = " " * 4
        output_lines.append(
            f'{prefix}"{answer}"' + ("," if i < len(data["answer"]) - 1 else "")
        )
    output_lines.append("]")

    # 添加contexts部分
    output_lines.append("\ncontexts: [")
    for i, context in enumerate(data["contexts"]):
        prefix = " " * 4
        # 每个上下文单独放在一个方括号内
        output_lines.append(
            f'{prefix}["{context}"]' + ("," if i < len(data["contexts"]) - 1 else "")
        )
    output_lines.append("]")

    # 添加ground_truths部分
    output_lines.append("\nground_truths: [")
    for i, truth in enumerate(data["ground_truth"]):
        prefix = " " * 4
        output_lines.append(
            f'{prefix}"{truth}"' + ("," if i < len(data["ground_truth"]) - 1 else "")
        )
    output_lines.append("]")

    # 写入文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        # f.write("\n".join(output_lines))

    print(f"结构化数据已保存到: {output_file}")
    print(f"包含 {len(data['question'])} 个问题")


if __name__ == "__main__":
    # 配置输入输出文件路径
    input_file = "_MAIN/middleFile/processed_results.txt"  # 之前处理的输出文件
    output_file = "_MAIN/middleFile/structured_data.json"  # 新的结构化输出文件

    # 提取字段
    structured_data = extract_fields_from_file(input_file)

    if structured_data:
        # 保存结构化数据
        save_structured_data(structured_data, output_file)

        # 打印统计信息
        print("\n数据统计:")
        print(f" - 问题数量: {len(structured_data['question'])}")
        print(f" - 答案数量: {len(structured_data['answer'])}")
        print(f" - 上下文数量: {len(structured_data['contexts'])}")
        print(f" - 参考答案数量: {len(structured_data['ground_truth'])}")

        # 显示输出文件预览
        if os.path.exists(output_file):
            print("\n输出文件预览:")
            with open(output_file, "r", encoding="utf-8") as f:
                # 显示前20行内容
                preview_lines = []
                for i, line in enumerate(f):
                    preview_lines.append(line.rstrip())
                    if i >= 20:
                        break
                print("\n".join(preview_lines))

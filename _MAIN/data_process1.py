# 读取原始半结构化文本文件，解析其中的目标数据块并完成初步格式规整
# 输出中间文件 processed_results.txt

import re
import os


def transform_data(text):
    """
    改进版本：处理特殊格式的实际答案和上下文
    """
    # 查找所有数据块起始位置
    block_matches = list(re.finditer(r"(\n?\d+\.问题：[^\n]*)", text))

    if not block_matches:
        print("未找到任何数据块")
        return []

    # 提取每个数据块的文本范围
    blocks = []
    for i in range(len(block_matches)):
        start_match = block_matches[i]
        start_index = start_match.start()
        end_index = (
            block_matches[i + 1].start() if i + 1 < len(block_matches) else len(text)
        )
        block_text = text[start_index:end_index].strip()
        blocks.append(block_text)

    # 解析每个数据块
    results = []
    for block in blocks:
        try:
            # 提取原始问题（包含编号）
            question_match = re.search(r"(\d+\.问题：[^\n]*)", block)
            if not question_match:
                continue
            original_question = question_match.group(1).strip()

            # 提取参考答案部分 - 更灵活的匹配
            ground_truth_match = re.search(
                r"参考答案：(.*?)(?=实际答案：|\n|$)", block, re.DOTALL
            )
            if not ground_truth_match:
                continue
            ground_truth = ground_truth_match.group(1).strip()

            # 提取实际答案部分 - 处理特殊格式
            answer_match = re.search(
                r"实际答案：(.*?)(?=上下文：|\n|$)", block, re.DOTALL
            )
            if not answer_match:
                continue
            answer = answer_match.group(1).strip()

            # 提取上下文部分 - 处理有无花括号两种情况
            context_match = re.search(r"上下文：\s*(\{?.*?\}?)\s*$", block, re.DOTALL)
            if not context_match:
                continue
            context_str = context_match.group(1).strip()

            # 移除可能的花括号
            if context_str.startswith("{") and context_str.endswith("}"):
                context_str = context_str[1:-1].strip()

            # 处理上下文中的多个question-answer对
            context_pairs = re.findall(
                r"question:(.*?)\s*answer:(.*?)(?=question:|$)", context_str, re.DOTALL
            )
            context_answers = []
            for _, ans in context_pairs:
                clean_ans = re.sub(r"\s+", " ", ans).strip()
                context_answers.append(clean_ans)

            # 合并所有answer作为上下文
            context = ", ".join(context_answers)

            # 构建结果字典
            result = {
                "original_question": original_question,
                "answer": answer,
                "context": context,
                "ground_truth": ground_truth,
            }

            results.append(result)

        except Exception as e:
            print(f"解析数据块时出错: {e}")
            continue

    return results

# 【选项 1】处理单个文件
def process_file(input_file, output_file):
    """
    处理输入文件并将结果写入输出文件
    """
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"错误：输入文件 '{input_file}' 不存在")
        return

    # 读取输入文件内容
    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    # 处理数据
    transformed_data = transform_data(input_text)

    if not transformed_data:
        print("未找到有效数据块，请检查输入文件格式")
        return

    # 准备输出内容 - 保留原始问题格式
    output_lines = []
    for i, data in enumerate(transformed_data, 1):
        # 第一行输出原始问题格式
        output_lines.append(data["original_question"])

        # 添加解析后的字段
        output_lines.append(f"[解析结果 #{i}]")
        output_lines.append(f"实际答案: {data['answer']}")
        output_lines.append(f"整合上下文: {data['context']}")
        output_lines.append(f"参考答案: {data['ground_truth']}")
        output_lines.append("-" * 100)

    # 写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    # 显示解析统计
    found_blocks = len(transformed_data)
    total_blocks = len(re.findall(r"\d+\.问题：", input_text))
    print(f"解析统计: 共{total_blocks}个数据块，成功解析{found_blocks}个")

    # 检查缺失的数据块
    parsed_nums = [
        int(re.search(r"(\d+)\.", d["original_question"]).group(1))
        for d in transformed_data
    ]
    all_nums = set(range(1, total_blocks + 1))
    missing_nums = all_nums - set(parsed_nums)

    if missing_nums:
        print(f"警告: 以下数据块解析失败: {sorted(missing_nums)}")
        print("可能原因: 格式特殊、字段缺失或匹配规则不完善")

# 【选项 2】统一处理文件夹中的所有 txt 文件
def process_folder(input_dir, output_file):
    all_results = []

    if not os.path.isdir(input_dir):
        print(f"错误：'{input_dir}' 不是有效文件夹")
        return

    txt_files = [
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.endswith(".txt")
    ]

    if not txt_files:
        print("文件夹中未找到 txt 文件")
        return

    # 在这个循环中处理每个文件
    for file_path in txt_files:
        print(f"正在处理文件: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        results = transform_data(text)
        all_results.extend(results)

    if not all_results:
        print("未解析出任何有效数据")
        return

    # === 统一写出 ===
    output_lines = []
    for i, data in enumerate(all_results, 1):
        output_lines.append(data["original_question"])
        output_lines.append(f"[解析结果 #{i}]")
        output_lines.append(f"实际答案: {data['answer']}")
        output_lines.append(f"整合上下文: {data['context']}")
        output_lines.append(f"参考答案: {data['ground_truth']}")
        output_lines.append("-" * 100)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"共解析 {len(all_results)} 条数据")
    print(f"结果已保存到: {os.path.abspath(output_file)}")


if __name__ == "__main__":
    # 配置输入输出文件路径
    input_file = "_MAIN/originFile/d1.txt"
    output_file = "_MAIN/middleFile/processed_results.txt"

    # 处理文件
    # process_file(input_file, output_file)
    process_folder("_MAIN/originFile", "_MAIN/middleFile/processed_results.txt")

    # 直接在控制台显示结果路径
    print(f"结果已保存到: {os.path.abspath(output_file)}")

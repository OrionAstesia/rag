# 实现从输入文件中循环读取问题和参考答案，调用 Dify API 获取回答，并将结果写入输出文件。

import requests
import json
import time
import re

API_KEY = "app-Io2oSeqvIQPMAqPFXVyaLj4Z"
URL = "https://api.dify.ai/v1/chat-messages"
MAX_COUNT = 40  # 最大为40


def process_file(input_file, output_file):

    with open(input_file, "r", encoding="utf-8") as infile, open(
        output_file, "w", encoding="utf-8"
    ) as outfile:

        counter = 1

        while True:

            if counter > MAX_COUNT:
                break

            question_line = infile.readline()
            if not question_line:
                break

            question_line = question_line.strip()

            match = re.match(r"^\d+\.\s*问题：(.*)", question_line)
            if not match:
                continue

            question = match.group(1).strip()

            # 读取参考答案
            reference_line = infile.readline()
            if not reference_line:
                break

            reference = reference_line.strip()

            print(f"正在处理第 {counter} 个问题...")

            # 调用 Dify
            payload = {
                "inputs": {},
                "query": question,
                "response_mode": "blocking",
                "conversation_id": "",
                "user": "test",
            }

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            }

            response = requests.post(URL, headers=headers, json=payload)
            result = response.json()

            answer = result.get("answer", "")
            answer = answer.strip()

            # 打印
            print("问题:", question)
            print(reference)
            print("Dify回答:", answer)
            print("---------------")

            # 写入文件
            outfile.write(f"{counter}.问题：{question}\n")
            outfile.write(f"{reference}\n")
            outfile.write(f"{answer}\n")

            counter += 1

            time.sleep(1)


def main():
    input_file = "test_records\\40\\1_chatflow_40_byYZX\\d1.txt"
    output_file = "_MAIN\\originFile\\d1.txt"
    process_file(input_file, output_file)
    print("码魂大悦，没有任何报错，处理完成！")


if __name__ == "__main__":

    input_file = "test_records\\1_chatflow_40_byYZX\\d1.txt"
    output_file = "_MAIN\\originFile\\d1.txt"
    process_file(input_file, output_file)
    print("码魂大悦，没有任何报错，处理完成！")

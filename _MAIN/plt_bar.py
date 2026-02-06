# @file plt_bar.py
# @author ZYC
# @brief 柱状图绘制 RAGAS

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plt_bar():
    # 读取CSV文件（注意文件可能包含BOM头，使用utf-8-sig编码）
    df = pd.read_csv("_MAIN/answer/ragas.csv", encoding="utf-8-sig")

    # 计算各列的平均值（跳过缺失值）
    metrics = [
        "context_precision",
        "context_recall",
        "faithfulness",
        "answer_relevancy",
        "answer_correctness",
    ]
    averages = df[metrics].mean()

    # 创建可视化图表
    plt.figure(figsize=(10, 6))
    bars = plt.bar(
        metrics, averages, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    )

    # 添加数据标签
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{height:.4f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    # 设置图表标题和标签
    plt.title("RAGAS Evaluation Metrics Averages", fontsize=14, pad=20)
    plt.ylabel("Average Score", fontsize=12)
    plt.xticks(fontsize=10)
    plt.ylim(0, 1.0)  # 设置Y轴范围

    # 添加网格线
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # 显示图表
    plt.tight_layout()
    plt.savefig("_MAIN/answer/ragas_bar.png", dpi=300)
    # plt.show()

    # 打印平均值结果
    print("各指标平均值:")
    print(averages.round(4))


if __name__ == "__main__":
    plt_bar()

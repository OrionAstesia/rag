# @file plt_radar.py
# @author ZYC
# @brief 雷达图绘制 RAGAS

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def file_test():
    with open("test.txt", "w", encoding="utf-8-sig"):
        pass


def plt_radar():
    # 读取CSV文件
    df = pd.read_csv("_MAIN/answer/ragas.csv", encoding="utf-8-sig")

    # 计算各列的平均值
    metrics = [
        "context_precision",
        "context_recall",
        "faithfulness",
        "answer_relevancy",
        "answer_correctness",
    ]
    averages = df[metrics].mean().values
    metric_labels = [
        "Context Precision",
        "Context Recall",
        "Faithfulness",
        "Answer Relevancy",
        "Answer Correctness",
    ]

    # 设置雷达图参数
    N = len(metrics)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # 闭合多边形

    # 准备数据
    values = averages.tolist()
    values += values[:1]  # 闭合多边形

    # 创建雷达图
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # 绘制数据
    ax.plot(
        angles,
        values,
        color="#1f77b4",
        linewidth=2,
        marker="o",
        markersize=8,
        markerfacecolor="white",
        markeredgewidth=2,
        markeredgecolor="#1f77b4",
    )
    ax.fill(angles, values, color="#1f77b4", alpha=0.25)

    # 添加标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metric_labels, fontsize=12)

    # 设置Y轴标签位置并添加数值
    ax.set_rlabel_position(30)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=10)
    ax.set_ylim(0, 1.0)

    # 添加数据点标签
    for i, (angle, value) in enumerate(zip(angles[:-1], averages)):
        ax.text(
            angle,
            value + 0.05,
            f"{value:.4f}",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.3", facecolor="white", alpha=0.8, edgecolor="none"
            ),
        )

    # 添加标题
    plt.title(
        "RAGAS Evaluation Metrics Radar Chart\nAverage Scores",
        fontsize=16,
        pad=25,
        fontweight="bold",
    )

    # 添加图例
    ax.legend(["Performance Scores"], loc="upper right", bbox_to_anchor=(1.15, 1.15))

    # 添加网格
    ax.grid(True, linestyle="--", alpha=0.7)

    # 保存并显示图表
    plt.tight_layout()
    plt.savefig("_MAIN/answer/ragas_radar.png", dpi=300, bbox_inches="tight")
    print("雷达图已保存为 'ragas_radar.png'")
    # plt.show()

    # 打印平均值结果
    print("各指标平均值:")
    for label, value in zip(metric_labels, averages):
        print(f"{label}: {value:.4f}")


if __name__ == "__main__":
    # file_test()
    plt_radar()

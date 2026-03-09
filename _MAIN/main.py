import os
import sys

sys.path.append(os.path.dirname(__file__))
import data_process0
import data_process1
import data_process2
import rag
import plt_bar
import plt_radar


def main():
    if 0:
        # process1 Q&A
        data_process1.process_folder(
            "_MAIN/originFile", "_MAIN/middleFile/processed_results.txt"
        )
    else:
        # process0 normal
        data_process0.process_folder(
            "_MAIN/originFile", "_MAIN/middleFile/processed_results.txt"
        )

    # process2
    structured_data = data_process2.extract_fields_from_file(
        "_MAIN/middleFile/processed_results.txt"
    )
    if structured_data:  # 保存结构化数据
        data_process2.save_structured_data(
            structured_data, "_MAIN/middleFile/structured_data.json"
        )

    # rag
    rag.run()

    # Visualization
    plt_bar.plt_bar()
    plt_radar.plt_radar()


if __name__ == "__main__":
    main()
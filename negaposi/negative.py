import pandas as pd
import os

current_path = os.path.dirname(os.path.abspath(__file__))

def main():
    # 元のCSVファイルのパスを指定
    input_file_path = f"{current_path}/csv/choco/01H7Z9XPBDRDH84FYK68J08QM9/01H7Z9XPBDRDH84FYK68J08QM9_review.csv"
    # CSVファイルからデータを読み込む
    data = pd.read_csv(input_file_path)

    # content列の文節に分けた結果を格納する空のリストを作成
    wakati_contents = []

    # content列を文節に分けてリストに格納
    for content in data['content']:
        wakati_content = ' '.join(content.split())  # 空白で分割して文節にし、空白で結合して元に戻す
        wakati_contents.append(wakati_content)

    # 新しいデータフレームを作成
    new_data = pd.DataFrame({
        'useful_count': data['useful_count'],
        'wakati_content': wakati_contents
    })

    # 保存先のCSVファイルが存在する場合は追加で保存する
    try:
        existing_data = pd.read_csv('all_review.csv')  # 既存のファイル名を指定
        combined_data = pd.concat([existing_data, new_data])
        combined_data.to_csv('all_review.csv', index=False)
    except FileNotFoundError:
        # 保存先のCSVファイルが存在しない場合は新しく保存する
        new_data.to_csv('all_review.csv', index=False)

if __name__ == "__main__":
    main()
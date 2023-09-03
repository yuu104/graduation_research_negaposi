import os
from utils.folder_file import get_all_folder_names
from pprint import pprint
from typing import List, TypedDict
import pandas as pd


current_path = os.path.dirname(os.path.abspath(__file__))


class ReviewData(TypedDict):
    useful_count: int
    content: str


def main():
    category_name = "chocolate"

    # 商品のフォルダ名をすべて取得
    item_folder_names = get_all_folder_names(
        f"{current_path}/csv/{category_name}/items"
    )

    # for文で商品を一つずつ走査
    review_data_list: List[ReviewData] = []
    for item_folder_name in item_folder_names:
        # `_review.csv`からデータフレームを作成
        review_df = pd.read_csv(
            f"{current_path}/csv/{category_name}/items/{item_folder_name}/{item_folder_name}_review.csv"
        )
        for i in range(len(review_df)):
            useful_count = int(review_df.loc[i, "useful_count"])
            content = review_df.loc[i, "content"]
            review_data_list.append({"useful_count": useful_count, "content": content})
    # 新しいデータフレームを作成
    new_review_df = pd.DataFrame(review_data_list)


if __name__ == "__main__":
    main()

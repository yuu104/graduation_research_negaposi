import mlask
from pprint import pprint
from typing import TypedDict, List, Optional, Union
from collections import defaultdict
import os
from utils.folder_file import get_all_folder_names
import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))

emotion_analyzer = mlask.MLAsk()


class EmotionResult(TypedDict):
    iya: Optional[List[str]]
    yorokobi: Optional[List[str]]
    kowa: Optional[List[str]]
    yasu: Optional[List[str]]
    suki: Optional[List[str]]
    aware: Optional[List[str]]
    ikari: Optional[List[str]]
    odoroki: Optional[List[str]]
    takabri: Optional[List[str]]
    haji: Optional[List[str]]


class EmotionCount(TypedDict):
    iya: int
    yorokobi: int
    kowa: int
    yasu: int
    suki: int
    aware: int
    ikari: int
    odoroki: int
    takaburi: int
    haji: int


class MlaskResult(TypedDict):
    activation: str
    emoticon: str
    emotion: EmotionResult
    intension: int
    orientation: str
    representative: dict[str, list[str]]
    text: str


def merge_emotion_result(dict1: EmotionResult, dict2: EmotionResult) -> EmotionResult:
    result = {}

    # dict1のキーと値をresultにコピー
    for key, value in dict1.items():
        result[key] = result.get(key, []) + value if value else []

    # dict2のキーと値をresultにコピー
    for key, value in dict2.items():
        result[key] = result.get(key, []) + value if value else []

    return result


def analyze_emotion(sentence: str) -> Union[EmotionResult, None]:
    result = MlaskResult(emotion_analyzer.analyze(sentence))
    result_emotion = result["emotion"]
    return result_emotion


def main():
    category_name = "chocolate"
    item_folder_names = get_all_folder_names(
        f"{current_path}/csv/{category_name}/items"
    )

    result = []
    for item_folder_name in item_folder_names:
        item_review_path = f"{current_path}/csv/{category_name}/items/{item_folder_name}/{item_folder_name}_review.csv"
        review_df = pd.read_csv(item_review_path, sep=",", index_col=0)

        for i in range(len(review_df)):
            review_title = str(review_df.loc[i, "title"]).strip("\n")
            review_content = str(review_df.loc[i, "content"])
            review_sentence_list = review_content.split("\n")
            review_sentence_list.append(review_title)

            emotion_result = EmotionResult({})
            for sentence in review_sentence_list:
                analyzed = analyze_emotion(sentence=sentence)
                emotion_result = (
                    merge_emotion_result(dict1=emotion_result, dict2=analyzed)
                    if analyzed
                    else emotion_result
                )

            result.append(
                {
                    "useful_count": review_df.loc[i, "useful_count"],
                    "emotion_result": {
                        key: len(value) for key, value in emotion_result.items()
                    },
                }
            )

    result_df = (
        pd.DataFrame(data=result).sort_values("useful_count").reset_index(drop=True)
    )
    emotion_result_list = (
        result_df[result_df["useful_count"] == 0].loc[:, "emotion_result"].values
    )

    emotion_count = {
        "iya": 0,
        "aware": 0,
        "haji": 0,
        "ikari": 0,
        "kowa": 0,
        "odoroki": 0,
        "suki": 0,
        "takaburi": 0,
        "yasu": 0,
        "yorokobi": 0,
    }

    for item in emotion_result_list:
        for key, value in item.items():
            emotion_count[key] += value

    pprint(emotion_count)


if __name__ == "__main__":
    main()

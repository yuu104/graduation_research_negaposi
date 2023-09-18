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
    iya: Optional[int]
    yorokobi: Optional[int]
    kowa: Optional[int]
    yasu: Optional[int]
    suki: Optional[int]
    aware: Optional[int]
    ikari: Optional[int]
    odoroki: Optional[int]
    takaburi: Optional[int]
    haji: Optional[int]


# class UsefulCountEmotions(TypedDict):
#     "0人": List[EmotionCount]
#     "1~2人": List[EmotionCount]
#     "3~4人": List[EmotionCount]
#     "5~6人": List[EmotionCount]
#     "7~9人": List[EmotionCount]
#     "10人": List[EmotionCount]


# class UsefulEmotionCount(TypedDict):
#     "0人": int
#     "1~2人": int
#     "3~4人": int
#     "5~6人": int
#     "7~9人": int
#     "10人": int


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


def calc_emotion_rate(useful_count_emotions, emotion: str):
    total_counts = {}
    for key, value in useful_count_emotions.items():
        emotion_count = 0
        for item in value:
            emotion_count += item.get(emotion, 0)
        total_counts[key] = emotion_count / len(value)

    return total_counts


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

    useful_count_emotions = {
        "0人": result_df[result_df["useful_count"] == 0]
        .loc[:, "emotion_result"]
        .values.tolist(),
        "1~2人": result_df[
            (result_df["useful_count"] >= 1) & (result_df["useful_count"] <= 2)
        ]
        .loc[:, "emotion_result"]
        .values.tolist(),
        "3~4人": result_df[
            (result_df["useful_count"] >= 3) & (result_df["useful_count"] <= 4)
        ]
        .loc[:, "emotion_result"]
        .values.tolist(),
        "5~6人": result_df[
            (result_df["useful_count"] >= 5) & (result_df["useful_count"] <= 6)
        ]
        .loc[:, "emotion_result"]
        .values.tolist(),
        "7~9人": result_df[
            (result_df["useful_count"] >= 7) & (result_df["useful_count"] <= 8)
        ]
        .loc[:, "emotion_result"]
        .values.tolist(),
        "10人~": result_df[result_df["useful_count"] >= 10]
        .loc[:, "emotion_result"]
        .values.tolist(),
    }

    useful_emotion_count = calc_emotion_rate(
        useful_count_emotions=useful_count_emotions, emotion="aware"
    )
    useful_emotion_count_df = pd.DataFrame([useful_emotion_count])
    pprint(useful_emotion_count_df)


if __name__ == "__main__":
    main()

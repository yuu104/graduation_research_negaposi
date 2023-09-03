import pandas as pd
import MeCab

# MeCabで辞書としてunidicを使用
mecab = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/unidic")

file_path = '/Users/k20043kk/言語処理/graduation_research_negaposi/negaposi/01H2WF9874HQCEW49H8BPBMH70_review.csv'  # アップロードしたCSVファイルのファイルパスを指定

data = pd.read_csv(file_path)

texts = data['content'].tolist()  # 文章が含まれている列の列名を指定し、リストに変換

sentences = []  # 文章を文節に分けた結果を格納するリスト

for text in texts:
    if pd.notnull(text):  # 欠損値（NaN）でないかチェック
        # 文章を文節に分割してNodeオブジェクトに変換
        node = mecab.parse(text)
        words = []
        for line in node.split('\n'):
            if line == 'EOS':
                break
            surface = line.split('\t')[0]
            if surface != '':
                words.append(surface)
        sentence = ' '.join(words)  # 文節をスペースで区切って1つの文字列にする
        sentences.append(sentence)
    else:
        sentences.append('')  # 欠損値の場合は空文字列として追加

data['sentences'] = sentences  # 文節に分けた結果を新しい列として追加

data.to_csv('result.csv', index=False)  # 結果をCSVファイルに保存

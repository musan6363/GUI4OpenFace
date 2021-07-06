import pandas as pd
import matplotlib.pyplot as plt

'''
グラフに表示する要素を追加するときは，追加箇所1,2を変更すれば良い．
AUは"AUxx_r"が各AUの強度(0〜5)，"AUxx_c"が0 absent, 1 presentを示す．
'''

# 追加箇所1
# columnsに検出の対象にする値を追加．face_id, timestamp, successは必須．
# Openfaceの出力CSVは列によって先頭に空白文字を含むことに注意．ミスが起きやすいので，定数定義で対応を取ると良い．
# 【改善案】csvcolumns.pyで全ての列名とその番号を保持，呼び出しプログラム側で引数を変えるだけでできるようにしたい．
columns = [" face_id", " timestamp", " success", " AU06_r", " AU12_r"]
FACE_ID = 0
TIMESTAMP = 1
SUCCESS = 2
AU06_R = 3
AU12_R = 4


class PlotGlaph:
    def __init__(self, csv: str, save_dir: str, save_name: str):
        self.csv = csv
        self.save_dir = save_dir
        self.save_name = save_name

        self.extract_csv()

    def extract_csv(self):
        df = pd.read_csv(self.csv)
        data = df.loc[:, columns]

        faceid_cnt = []
        for _ in range(data[columns[FACE_ID]].max() + 1):
            faceid_cnt.append(0)

        for line in data.values:
            faceid_cnt[int(line[FACE_ID])] += int(line[SUCCESS])

        target_face_id = faceid_cnt.index(max(faceid_cnt))

        target = []
        for line in data.values:
            # 最も多く登場する顔のうち，処理に成功しているものを抽出
            if line[FACE_ID] == target_face_id and line[SUCCESS] == 1:
                target.append(line)

        self.df = pd.DataFrame(target, columns=columns)
        self.plot()

    def plot(self):
        # 追加箇所2
        # 追加したデータ分，plot命令を追加する．
        # colorはグラフ上で見分けるために変えたほうが良い．
        ax = self.df.plot.scatter(x=columns[TIMESTAMP], y=columns[AU06_R], label='AU06', color='red')
        ax = self.df.plot.scatter(x=columns[TIMESTAMP], y=columns[AU12_R], label='AU12', color='blue', ax=ax)
        # plt.show()
        plt.savefig(self.save_dir + "/" + self.save_name + ".png")
        plt.close()


if __name__ == '__main__':
    # debug
    csvpath = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210702/Girl49394.csv"
    save_dir = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210705"
    save_name = "test"
    PlotGlaph(csvpath, save_dir, save_name)

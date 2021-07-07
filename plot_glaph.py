import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
from multiprocessing import Pool

# columnsに検出の対象にする値を追加．face_id, timestamp, successは必須．
# Openfaceの出力CSVは列によって先頭に空白文字を含むことに注意．ミスが起きやすいので，定数定義で対応を取ると良い．
# 【改善案】csvcolumns.pyで全ての列名とその番号を保持，呼び出しプログラム側で引数を変えるだけでできるようにしたい．
columns = [" face_id", " timestamp", " success", " AU01_r", " AU02_r", " AU04_r", " AU05_r", " AU06_r", " AU07_r",
           " AU09_r", " AU10_r", " AU12_r", " AU14_r", " AU15_r", " AU17_r", " AU20_r", " AU23_r", " AU25_r", " AU26_r", " AU45_r"]
FACE_ID = 0
TIMESTAMP = 1
SUCCESS = 2
AU01_R = 3
AU02_R = 4
AU04_R = 5
AU05_R = 6
AU06_R = 7
AU07_R = 8
AU09_R = 9
AU10_R = 10
AU12_R = 11
AU14_R = 12
AU15_R = 13
AU17_R = 14
AU20_R = 15
AU23_R = 16
AU25_R = 17
AU26_R = 18
AU45_R = 19

colorlist = ['#ff7f7f', '#ff7fbf', '#ff7fff', '#bf7fff', '#7f7fff', '#7fbfff', '#7fffff', '#7fffbf', '#7fff7f', '#bfff7f', '#ffff7f', '#ffbf7f', '#ff0000', '#ff00ff', '#7f00ff', '#007fff', '#00ff7f']


class NoSuccessValue(Exception):
    pass


def PlotGlaph(csv: str, save_dir: str, save_name: str):
    df = pd.read_csv(csv)
    data = df.loc[:, columns]

    target_face_id = get_mode_face_id(data)  # 最も多く登場するface_idを取得する

    # 最も多く登場する顔のうち，処理に成功しているものを抽出
    target = []
    for line in data.values:
        # if line[FACE_ID] == target_face_id and line[SUCCESS] == 1:
        if line[FACE_ID] == target_face_id:
            target.append(line)

    if len(target) == 0:
        raise NoSuccessValue

    df = pd.DataFrame(target, columns=columns)

    # npdata[0]:timestamp, npdata[1]:AU06, npdata[2]:AU12
    npdata = df[[columns[TIMESTAMP], columns[AU01_R], columns[AU02_R], columns[AU04_R], columns[AU05_R], columns[AU06_R], columns[AU07_R], columns[AU09_R], columns[AU10_R],
                 columns[AU12_R], columns[AU14_R], columns[AU15_R], columns[AU17_R], columns[AU20_R], columns[AU23_R], columns[AU25_R], columns[AU26_R], columns[AU45_R]]].values.T
    x_latent = np.linspace(min(npdata[0]), max(npdata[0]), 100)  # 保管用のX軸データ

    liners = [interpolate.interp1d(x=npdata[0], y=npdata[i + 1]) for i in range(17)]

    p = Pool(1)
    p.map(plot, [[x_latent, liners, save_dir, save_name]])
    p.close()


def get_mode_face_id(data):
    faceid_cnt = []
    for _ in range(data[columns[FACE_ID]].max() + 1):
        faceid_cnt.append(0)

    for line in data.values:
        faceid_cnt[int(line[FACE_ID])] += int(line[SUCCESS])

    return faceid_cnt.index(max(faceid_cnt))


def plot(args):
    x_latent, liners, save_dir, save_name = args

    fig = plt.figure(figsize=[16.18, 10])
    _i = 0
    for liner in liners:
        plt.plot(x_latent, liner(x_latent), color=colorlist[_i], label=columns[_i + 3])
        _i += 1
    plt.grid()
    plt.legend()
    # plt.show()

    fig.savefig(save_dir + "/" + save_name + ".png")


if __name__ == '__main__':
    # debug
    csvpath = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210706/cutvideo_output/id0136no01_12/id0136no01_12.csv"
    save_dir = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210707"
    save_name = "id0136no01_12"
    PlotGlaph(csvpath, save_dir, save_name)

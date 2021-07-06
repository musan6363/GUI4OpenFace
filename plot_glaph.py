import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate
import numpy as np
from multiprocessing import Pool

# columnsに検出の対象にする値を追加．face_id, timestamp, successは必須．
# Openfaceの出力CSVは列によって先頭に空白文字を含むことに注意．ミスが起きやすいので，定数定義で対応を取ると良い．
# 【改善案】csvcolumns.pyで全ての列名とその番号を保持，呼び出しプログラム側で引数を変えるだけでできるようにしたい．
columns = [" face_id", " timestamp", " success", " AU06_r", " AU12_r"]
FACE_ID = 0
TIMESTAMP = 1
SUCCESS = 2
AU06_R = 3
AU12_R = 4


def PlotGlaph(csv: str, save_dir: str, save_name: str):
    df = pd.read_csv(csv)
    data = df.loc[:, columns]

    target_face_id = get_mode_face_id(data)  # 最も多く登場するface_idを取得する

    # 最も多く登場する顔のうち，処理に成功しているものを抽出
    target = []
    for line in data.values:
        if line[FACE_ID] == target_face_id and line[SUCCESS] == 1:
            target.append(line)

    df = pd.DataFrame(target, columns=columns)

    # npdata[0]:timestamp, npdata[1]:AU06, npdata[2]:AU12
    npdata = df[[columns[TIMESTAMP], columns[AU06_R], columns[AU12_R]]].values.T
    x_latent = np.linspace(min(npdata[0]), max(npdata[0]), 100)  # 保管用のX軸データ

    liner_au06 = interpolate.interp1d(x=npdata[0], y=npdata[1])
    liner_au12 = interpolate.interp1d(x=npdata[0], y=npdata[2])

    p = Pool(1)
    p.map(plot, [[x_latent, liner_au06, liner_au12, save_dir, save_name]])
    p.close()


def get_mode_face_id(data):
    faceid_cnt = []
    for _ in range(data[columns[FACE_ID]].max() + 1):
        faceid_cnt.append(0)

    for line in data.values:
        faceid_cnt[int(line[FACE_ID])] += int(line[SUCCESS])

    return faceid_cnt.index(max(faceid_cnt))


def plot(args):
    x_latent, liner_au06, liner_au12, save_dir, save_name = args

    fig = plt.figure()
    plt.plot(x_latent, liner_au06(x_latent), c="red", label="AU06")
    plt.plot(x_latent, liner_au12(x_latent), c="blue", label="AU12")
    plt.grid()
    plt.legend()
    # plt.show()

    fig.savefig(save_dir + "/" + save_name + ".png")


if __name__ == '__main__':
    # debug
    csvpath = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210702/Girl49394.csv"
    save_dir = "/Users/mrkm-cmc/GoogleDrive/NU/cmc/210706"
    save_name = "test"
    PlotGlaph(csvpath, save_dir, save_name)

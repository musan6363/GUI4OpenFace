import pandas as pd
import matplotlib.pyplot as plt

FACE_ID = 0
TIMESTAMP = 1
SUCCESS = 2
AU06_R = 3
AU12_R = 4
AU06_C = 5
AU12_C = 6

columns = [" face_id", " timestamp", " success", " AU06_r", " AU12_r", " AU06_c", " AU12_c"]


def save_glaph_au6_au12(csv: str, save_dir: str, save_name: str):
    df = pd.read_csv(csv)
    data = df.loc[:, columns]  # Openfaceの出力CSVは列によって先頭に空白文字を含むことに注意

    faceid_cnt = []
    for i in range(data[columns[FACE_ID]].max() + 1):
        faceid_cnt.append(0)

    for line in data.values:
        faceid_cnt[int(line[FACE_ID])] += int(line[SUCCESS])

    target_face_id = faceid_cnt.index(max(faceid_cnt))

    target = []
    for line in data.values:
        # 最も多く登場する顔のうち，処理に成功しているものを抽出
        if line[FACE_ID] == target_face_id and line[SUCCESS] == 1:
            target.append(line)

    target_df = pd.DataFrame(target, columns=columns)

    au06 = target_df.plot.scatter(x=columns[TIMESTAMP], y=columns[AU06_R], label='AU06', color='red')
    au12 = target_df.plot.scatter(x=columns[TIMESTAMP], y=columns[AU12_R], label='AU12', color='blue', ax=au06)
    # plt.show()
    plt.savefig(save_dir + "/" + save_name + ".png")

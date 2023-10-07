

import numpy as np
import io
import gzip
import cv2
import sys

import binascii
import pandas as pd
from sklearn.cluster import AffinityPropagation
from difflib import SequenceMatcher
import jellyfish
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import itertools

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def ld(s, t):
    if not s:
        return len(t)
    if not t:
        return len(s)
    if s[0] == t[0]:
        return ld(s[1:], t[1:])
    l1 = ld(s, t[1:])
    l2 = ld(s[1:], t)
    l3 = ld(s[1:], t[1:])
    return 1 + min(l1, l2, l3)

# img_1 = img_2 = np.full((250, 250), 2)
# img_3 = img_4 = np.full((250, 250), 5)
# img_5 = img_6 = np.full((250, 250), 9)
# imgs = [img_1, img_2, img_3, img_4, img_5, img_6]

imgs = []
imgs_idx = [5001, 5002, 10000, 10001, 50001, 50002, 1, 2]
cap = cv2.VideoCapture('/Users/simon/Downloads/BOX1-20230806T100926-110927_grayscale.mp4')
for idx in imgs_idx:
    cap.set(1, idx)
    _, img = cap.read()
    imgs.append(img)
    cv2.imwrite(f'/Users/simon/Desktop/envs/troubleshooting/asdasd/images/{idx}.png', img)
#
# cx_len = np.full((len(imgs_idx)), np.nan)
# cx = np.full((len(imgs_idx)), dtype="S100000", fill_value='NaN')
# for cnt, img in enumerate(imgs):
#     cx[cnt] = str(gzip.compress(bytes(img)))
#     cx_len[cnt] = len(cx[cnt])
#
# for (idx_1, idx_2) in itertools.combinations(list(range(0, len(cx_len))), 2):
#     Cx1 = len(gzip.compress(bytes(imgs[idx_1], 'utf-8')))
#


#results = KMeans(n_clusters=4).fit_predict(compressed_img_sizes.reshape(-1, 1))




list_dfs = []
df = pd.DataFrame()
for idx, x1 in enumerate(imgs):
    Cx1 = len(gzip.compress(binascii.hexlify(x1.tobytes())))
    distance_from_x1 = []
    for idy, x2 in enumerate(imgs):
        Cx2 = len(gzip.compress(binascii.hexlify(x2.tobytes())))
        x1x2 = gzip.compress(binascii.hexlify(x1.tobytes()) + binascii.hexlify(x2.tobytes()))
        # Cx1x2 = len(x1x2)
        # ncd = (Cx1x2 - min(Cx1,Cx2)) / max(Cx1 ,Cx2)
        # distance_from_x1.append(float(ncd))
    # df['dist'] = distance_from_x1
    # df = df.sort_values(by='dist')
    # print(df)
    # list_dfs.append(df)

# neighbours =
# sub_arr = np.abs(compressed_img_sizes[:,None] - compressed_img_sizes)

# """
# 1,
# 0
# 3,
# 2,
# 5,
# 4,
# 7
# 6
#
# """
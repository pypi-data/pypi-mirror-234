import numpy as np


def kendall_tau(sample_1: np.ndarray,
                sample_2: np.ndarray) -> (float, float):

    rnks = np.argsort(sample_1)#[::-1]
    s1_rnk, s2_rnk = sample_1[rnks], sample_2[rnks]
    cncrdnt_cnts, dscrdnt_cnts = np.full((s1_rnk.shape[0]-1), np.nan), np.full((s1_rnk.shape[0]-1), np.nan)
    for i in range(s2_rnk.shape[0]-1):
        cncrdnt_cnts[i] = np.argwhere(s2_rnk[i+1:] > s2_rnk[i]).flatten().shape[0]
        dscrdnt_cnts[i] = np.argwhere(s2_rnk[i+1:] < s2_rnk[i]).flatten().shape[0]
    t = (np.sum(cncrdnt_cnts) - np.sum(dscrdnt_cnts)) / (np.sum(cncrdnt_cnts) + np.sum(dscrdnt_cnts))
    z = 3 * t * (np.sqrt(s1_rnk.shape[0] * (s1_rnk.shape[0]-1))) / np.sqrt( 2 * ((2 * s1_rnk.shape[0]) + 5))

    return t, z


        #print(cncrdnt_cnts)

sample_1 = np.array([1, 2, 3, 4, 5])
sample_2 = np.array([1, 2, 3, 4, 5])


kendall(sample_1=sample_1, sample_2=sample_2)
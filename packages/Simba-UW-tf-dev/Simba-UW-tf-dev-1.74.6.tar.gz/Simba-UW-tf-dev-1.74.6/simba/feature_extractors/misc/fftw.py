import numpy as np
try:
    from typing import Literal
except:
    from typing_extensions import Literal
import pandas as pd
import glob

def dominant_frequencies(data: np.ndarray,
                         fps: float,
                         k: int,
                         window_function: Literal['Hann', 'Hamming', 'Blackman'] = None):

    if window_function == 'Hann':
        data = data * np.hanning(len(data))
    elif window_function == 'Hamming':
        data = data * np.hamming(len(data))
    elif window_function == 'Blackman':
        data = data * np.blackman(len(data))
    fft_result = np.fft.fft(data)
    frequencies = np.fft.fftfreq(data.shape[0], 1 / fps)
    magnitude = np.abs(fft_result)
    return frequencies[np.argsort(magnitude)[-(k + 1):-1]]


def sliding_dominant_frequencies(data: np.ndarray,
                                 fps: float,
                                 k: int,
                                 time_windows: np.ndarray,
                                 window_function: Literal['Hann', 'Hamming', 'Blackman'] = None):

    results = np.full((data.shape[0], time_windows.shape[0]), 0.0)
    for time_window_cnt in range(time_windows.shape[0]):
        window_size = int(time_windows[time_window_cnt] * fps)
        for left, right in zip(range(0, data.shape[0] + 1), range(window_size, data.shape[0] + 1)):
            window_data = data[left:right]
            if window_function == 'Hann':
                window_data = window_data * np.hanning(len(window_data))
            elif window_function == 'Hamming':
                window_data = window_data * np.hamming(len(window_data))
            elif window_function == 'Blackman':
                window_data = window_data * np.blackman(len(window_data))
            fft_result = np.fft.fft(window_data)
            frequencies = np.fft.fftfreq(window_data.shape[0], 1 / fps)
            magnitude = np.abs(fft_result)
            top_k_frequency = frequencies[np.argsort(magnitude)[-(k + 1):-1]]
            results[right-1][time_window_cnt] = top_k_frequency[0]
    return results


df_lst = []
file_paths = glob.glob('/Users/simon/Downloads/Self_groom_targets_inserted' + '/*.csv')
for file in file_paths:
    print(file)
    df = pd.read_csv(file, index_col=0)
    df_lst.append(df)
    # for column in df.columns[0:-1]:
    #     data = df[column].values
    #     values = sliding_dominant_frequencies(data=data, fps=30, k=1, time_windows=np.array([0.5, 1.0, 1.5, 2.0]), window_function='Blackman')
    #     cols = [f'{column}_{x}_fft_blackman' for x in [0.5, 1.0, 1.5, 2.0]]
    #     data_df =  pd.DataFrame(values, columns=cols)
    #     df = pd.concat([df, data_df], axis=1)
    # df.to_csv(file)

df = pd.concat(df_lst, axis=0)

df.corrwith(df['Self_groom']).sort_values(ascending=False)





# for i in range(1):
#     print(
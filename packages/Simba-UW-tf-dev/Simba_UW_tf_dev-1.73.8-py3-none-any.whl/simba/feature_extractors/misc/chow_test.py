import numpy as np

def chow_test(data: np.ndarray,
              time_windows: np.ndarray,
              fps: int):

    results = np.full((data.shape[0]), -1.0)
    time_window = int(fps * time_windows[0])
    for r in range(time_window, data.shape[0]):
        mid_point, l = int(r - time_window/2), int(r-time_window)
        y1, y2 = data[l:mid_point], data[mid_point:r]
        A = np.vstack([np.arange(l, r), np.ones(len(np.arange(l, r)))]).T
        y = np.append(y1, y2)
        rss_total = np.linalg.lstsq(A, y, rcond=None)[1]

        A = np.vstack([np.arange(l, mid_point), np.ones(len(np.arange(l, mid_point)))]).T
        rss_1 = np.linalg.lstsq(A, y1, rcond=None)[1]

        A = np.vstack([np.arange(mid_point, r), np.ones(len(np.arange(mid_point, r)))]).T
        rss_2 = np.linalg.lstsq(A, y2, rcond=None)[1]

        chow_nom = (rss_total - (rss_1 + rss_2)) / 2
        chow_denom = (rss_1 + rss_2) / (y1.shape[0] + y2.shape[0] - 4)
        c = chow_nom / chow_denom
        print(c)


import numpy as np
from scipy.stats import f

def f_value(y1, x1, y2, x2):
    """This is the f_value function for the Chow Break test package
    Args:
        y1: Array like y-values for data preceeding the breakpoint
        x1: Array like x-values for data preceeding the breakpoint
        y2: Array like y-values for data occuring after the breakpoint
        x2: Array like x-values for data occuring after the breakpoint

    Returns:
        F-value: Float value of chow break test
    """
    def find_rss (y, x):
        """This is the subfunction to find the residual sum of squares for a given set of data
        Args:
            y: Array like y-values for data subset
            x: Array like x-values for data subset

        Returns:
            rss: Returns residual sum of squares of the linear equation represented by that data
            length: The number of n terms that the data represents
        """
        A = np.vstack([x, np.ones(len(x))]).T
        rss = np.linalg.lstsq(A, y, rcond=None)[1]
        length = len(y)
        return (rss, length)


    rss_total, n_total = find_rss(np.append(y1, y2), np.append(x1, x2))
    rss_1, n_1 = find_rss(y1, x1)
    rss_2, n_2 = find_rss(y2, x2)

    chow_nom = (rss_total - (rss_1 + rss_2)) / 2
    chow_denom = (rss_1 + rss_2) / (n_1 + n_2 - 4)
    return chow_nom / chow_denom






data = [x for x in list([10]*90)]
# time_windows = np.array([10.0])
# fps = 10
#
# chow_test(data=data, time_windows=time_windows, fps=fps)


f_val = f_value(data[0:50], np.arange(0, 50), data[0:50], np.arange(50, 100))
print(f_val)
df1 = 2
df2 = len(data[0:50]) + len(data[0:50]) - 4
p_val = f.sf(f_val[0], df1, df2)



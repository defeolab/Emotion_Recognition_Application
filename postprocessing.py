import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter
import pandas as pd


def myplot(x, y, s, bins=1000):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent


def process(path):
    fig, axs = plt.subplots(2, 2)
    pd.options.mode.chained_assignment = None
    #path = "/Users/victorseguin/Desktop/2021_Apr_22_1717.csv"
    df= pd.read_csv(path, sep=";")
    #print(df)

    wanted_df = df[["left_gaze_point_on_display_area_x", "left_gaze_point_on_display_area_y"]]
    #print(wanted_df.size)
    wanted_df['left_gaze_point_on_display_area_y'].replace('', np.nan, inplace=True)
    wanted_df.dropna(subset=['left_gaze_point_on_display_area_y'], inplace=True)

    wanted_df['left_gaze_point_on_display_area_x'].replace('', np.nan, inplace=True)
    wanted_df.dropna(subset=['left_gaze_point_on_display_area_x'], inplace=True)

    #print(wanted_df.size)

    x,y = wanted_df[1:]["left_gaze_point_on_display_area_x"], wanted_df[1:]["left_gaze_point_on_display_area_y"]

    sigmas = [0, 16, 32, 64]

    for ax, s in zip(axs.flatten(), sigmas):
        if s == 0:
            ax.plot(x, y, 'k.', markersize=5)
            ax.set_title("Scatter plot")
        else:
            img, extent = myplot(x, y, s)
            ax.imshow(img, extent=extent, origin='lower', cmap=cm.jet)
            ax.set_title("Smoothing with  $\sigma$ = %d" % s)

    plt.savefig('heatmaps.png')
    plt.show()

process("/Users/victorseguin/Desktop/2021_Apr_22_1717.csv")
from cv2 import cv2
from shapely.geometry import Point
from sklearn.cluster import KMeans
import numpy as np


def kmeans_xy(points: set[tuple]):
    xset = set()
    yset = set()
    for point in points:
        xset.add(point[0])
        yset.add(point[1])

    xdata = np.array(list(xset))
    ydata = np.array(list(yset))
    kmeansx = KMeans(n_clusters=12).fit(xdata.reshape(-1, 1))
    kmeansx.predict(xdata.reshape(-1, 1))

    kmeansy = KMeans(n_clusters=38).fit(ydata.reshape(-1, 1))
    kmeansy.predict(ydata.reshape(-1, 1))

    x_centers = set()
    for item in kmeansx.cluster_centers_:
        x_centers.add((int(item[0]), 0))
    y_centers = set()
    for item in kmeansy.cluster_centers_:
        y_centers.add((0, int(item[0])))
    return x_centers, y_centers


def write_points(image, points: set[tuple], color):
    for point in points:
        cv2.circle(image, (point[0], point[1]), radius=5, color=color, thickness=-1)
    return image

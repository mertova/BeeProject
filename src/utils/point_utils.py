import cv2
import numpy as np


# Cluster a set of numbers based on the distance from each other
def clustering_eps(points, eps):
    clusters = []
    points_sorted = sorted(points)

    curr_point = points_sorted[0]
    curr_cluster = [curr_point]
    for point in points_sorted[1:]:
        if curr_point - eps <= point <= curr_point + eps:
            curr_cluster.append(point)
        else:
            clusters.append(np.median(curr_cluster))
            curr_cluster = [point]
        curr_point = point
    clusters.append(np.median(curr_cluster))
    print(clusters)
    return clusters


def write_points(image, points: list[tuple], color: tuple):
    for point in points:
        if point is not None:
            cv2.circle(image, (point[0], point[1]), radius=5, color=color, thickness=-1)
    return image

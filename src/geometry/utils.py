import numpy as np


def cluster(numbers: list, eps):
    """
    Cluster a set of numbers based on the distance from each other
    :param numbers: numbers to be clustered
    :param eps: allowed distance from each other
    :return: clusters, list of lists of numbers
    """
    if numbers is None or len(numbers) == 0:
        return None
    clusters = []
    points_sorted = sorted(numbers)
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
    return clusters


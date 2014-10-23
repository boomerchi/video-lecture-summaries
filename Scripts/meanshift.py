'''
Created on Oct 22, 2014

@author: hijungshin
'''

import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
import matplotlib.pyplot as plt
from itertools import cycle
from sklearn.datasets.samples_generator import make_blobs


def cluster(data):
    ms = MeanShift()
    ms.fit(data)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    plt.figure(1)
    plt.clf()    
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(data[my_members, 0], data[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
    
    return labels, cluster_centers



if __name__ == "__main__":
    X = [(0,1), (0,3), (0,2.5), (0,33), (0,2.6), (0,30), (2,10)]
    print X
    mydata = np.array(X)
    print mydata
    cluster(mydata)
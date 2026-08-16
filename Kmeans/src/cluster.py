import numpy as np
def distance(a, b):
    return np.sqrt(
        np.sum((a-b)**2)
    )

def hierarchical(X,k):
    #解决None无法迭代问题
    n = len(X)
    if not isinstance(k, int) or k <= 0:
        raise ValueError(f"k must be a positive integer, got {k}")
    if k > n:
        raise ValueError(f"k cannot be greater than the number of samples ({n}), got {k}")
    clusters=[]
    for i in range(n):
        clusters.append([i])
    while len(clusters)>k:
        min_dist=float("inf")
        pair=None
        for i in range(len(clusters)):
            for j in range(i+1,len(clusters)):
                center1=X[clusters[i]].mean(axis=0)
                center2=X[clusters[j]].mean(axis=0)
                d=distance(center1,center2)
                if d<min_dist:
                    min_dist=d
                    pair=(i,j)
        if pair is None:
            break
        a,b=pair
        clusters[a]+=clusters[b]
        clusters.pop(b)
    labels = np.zeros(
        n,
        dtype=int
    )
    for i,cluster in enumerate(clusters):
        for index in cluster:
            labels[index]=i
    return labels
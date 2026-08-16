import numpy as np

def distance(a, b):
    return np.sqrt(np.sum((a-b)**2))

def kmeans(X,k,epochs=100):
    index=np.random.choice(len(X),k,replace=False)
    centers=X[index]
    labels=None
    for i in range(epochs):
        labels=[]
        for x in X:
            distances=[]
            for center in centers:
                d=distance(x,center)
                distances.append(d)
            label=np.argmin(distances)
            labels.append(label)
        labels=np.array(labels)
        new_centers=[]
        for j in range(k):
            points=X[labels==j]
            new_center=np.mean(points,axis=0)
            new_centers.append(new_center)
        new_centers=np.array(new_centers)
        if np.allclose(centers,new_centers):
            break
        centers=new_centers
    return centers,labels


class KMeans:
    def __init__(self,k=3,epochs=1000):
        self.k=k
        self.epochs=epochs

    def fit(self,X):
        n_samples=X.shape[0]
        index=np.random.choice(n_samples,self.k,replace=False)
        self.centers=X[index]
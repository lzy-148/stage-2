# 2026-08-18
# KNN的实现
# 自己实现
import numpy as np
class KNN:
    def __init__(self,k=3):
        self.k=k

    def fit(self,X,y):
        self.X_train=X
        self.y_train=y

    def distance(self,x,y):
        return np.sqrt((x-y)**2)

    def predict(self,X):
        result=[]
        for x in X:
            distances=[]
            for i,train in enumerate(self.X_train):
                d=self.distance(
                    x,
                    train
                )
                distances.append(
                    (d,self.y_train)
                )
            distances.sort()
            neighbors=distances[:self.k]
            labels=[label for _,label in neighbors]
            labels=[]
            for distance,label in neighbors:
                labels.append(label)
            pred=max(
                set(labels),
                key=labels.count
            )
            result.append(pred)
        return np.array(result)
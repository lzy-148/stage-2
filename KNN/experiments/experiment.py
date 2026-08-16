import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

dimensions=[2,5,10,20,50,100]
results=[]
for dim in dimensions:
    X,y=make_classification(
        n_samples=1000,
        n_features=dim,
        n_informative=2,#增加一定噪音
        n_redundant=0,#无重复信息
        random_state=42
    )
    X_train,X_test,y_train,y_test=train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42
    )
    model=KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train,y_train)
    pred=model.predict(X_test)
    ac=accuracy_score(y_test,pred)
    results.append(ac)#储存结果
    print("维度：",dim,"准确率：",ac)

    
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

import numpy as np
from src.logistic_regression.sigmoid import sigmoid
class SelfLogisticRegression:
    def __init__(self,l=0.01,epoch=10000):
        self.l=l
        self.epoch=epoch

    def fit(self,x,y):
        m,n=x.shape
        self.w=np.zeros((n,1))
        self.b=0
        for i in range(self.epoch):
            z=x@self.w+self.b
            y_hat=sigmoid(z)
            dw=(1/m)*x.T@(y_hat-y.reshape(-1,1))
            db=np.mean(y_hat-y.reshape(-1,1))
            self.w-=self.l*dw
            self.b-=self.l*db

    def predict_p(self,x):
        return sigmoid(x@self.w+self.b)

    def predict(self,x,threshold=0.7):
        prob=self.predict_p(x)
        return (prob>=threshold).astype(int)

##X 第一列学习时间 第二列学习次数
X_train=np.array([
    [1,1],
    [2,1],
    [2,2],
    [3,2],
    [4,3],
    [5,4],
    [6,5],
    [7,6]
])

##Y标签 0不通过 1通过
y_train=np.array([
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    1
])

##测试用例
X_test=np.array([
    [1,2],
    [3,3],
    [6,4],
    [8,7]
])

y_test=np.array([
    0,
    0,
    1,
    1
])
self_model=SelfLogisticRegression(l=0.1,epoch=10000)
self_model.fit(X_train,y_train)
print("自己实现模型:")
print("权重 w:")
print(self_model.w)
print("偏置 b:")
print(self_model.b)
print("预测概率:")
print(self_model.predict_p(X_test))
print("预测类别:")
print(self_model.predict(X_test))


##库实现
from sklearn.linear_model import LogisticRegression
model=LogisticRegression()
model.fit(X_train,y_train)
pred=model.predict(X_test)
print("\nsklearn预测:")
print(pred)
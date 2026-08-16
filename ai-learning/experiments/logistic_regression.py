## 2026-08-14
## purpose
## 构造类别不平衡数据；证明准确率可能产生误导;比较不同阈值下的误报和漏报。

import numpy as np

#构造类别不平衡数据
from sklearn.datasets import make_classification
import sys
from pathlib import Path
project_root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(project_root))

from src.logistic_regression.logistic import SelfLogisticRegression
from sklearn.model_selection import train_test_split
from src.logistic_regression.metrics import *
model=SelfLogisticRegression(l=0.01,epoch=100000)


X,y=make_classification(n_samples=1000,n_features=5,weights=[0.95,0.05],random_state=42)
print("类别数量:")
print("0类:", np.sum(y==0))
print("1类:", np.sum(y==1))


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

pred=model.predict(
    X_test,
    threshold=0.1
)
prob=model.predict_p(
    X_test    
)
print("\n默认阈值0.1:")
print("Accuracy:",accuracy(y_test,pred))
print("Precision:",precision(y_test,pred))
print("Recall:",recall(y_test,pred))
print("F1:",f1_score(y_test,pred))
print("AUC:",auc(y_test,prob))
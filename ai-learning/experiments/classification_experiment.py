import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

import numpy as np
from src.logistic_regression.metrics import *

y_true=np.array([1,0,1,1,0])
y_pred=np.array([1,0,0,1,1])

print("混淆矩阵:")
print(confusionmatrix(y_true,y_pred))

print("Accuracy:")
print(accuracy(y_true,y_pred))

print("Precision:")
print(precision(y_true,y_pred))

print("Recall:")
print(recall(y_true,y_pred))

print("F1:")
print(f1_score(y_true,y_pred))
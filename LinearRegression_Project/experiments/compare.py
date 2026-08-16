import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.gradient_descent import gradient
from src.normal_equation import normal_equation

NUM = 100

np.random.seed(0)
X = np.random.rand(NUM, 1)
y = 3 * X + 2 + np.random.randn(NUM, 1) * 0.1
X_b = np.c_[np.ones((NUM, 1)), X]

##theta_gd, loss = gradient(X_b, y)
##theta_ne = normal_equation(X_b, y)

theta_none,_=gradient(X_b,y)
theta_l1,_=gradient(X_b,y,reg='l1',lam=0.001)
theta_l2,_=gradient(X_b,y,reg='l2',lam=0.001)

'''
print("梯度下降:")
print(theta_gd)
print("解析解:")
print(theta_ne)
'''
print("无正则:")
print(theta_none)
print("L1:")
print(theta_l1)
print("L2:")
print(theta_l2)

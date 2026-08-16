import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LinearRegression

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.gradient_descent import gradient
np.random.seed(0)
X=np.random.rand(100,1)
Y=3*X+2+np.random.randn(100,1)*0.1
X_b=np.c_[np.ones((100,1)),X]
theta_gd, _ = gradient(X_b,Y,lr=0.01,epochs=10000)
print("梯度下降:")
print(theta_gd)

##sklearn:
model = LinearRegression()
model.fit(X,Y)
theta_sklearn = np.array([[model.intercept_],[model.coef_[0]]])
print("sklearn:")
print(theta_sklearn)

from sklearn.linear_model import Ridge,Lasso
ridge = Ridge(alpha=0.01)
ridge.fit(X,Y)
print("L2:")
print(ridge.intercept_)
print(ridge.coef_)
lasso=Lasso(alpha=0.01)

lasso.fit(X,Y)
print("L1:")
print(lasso.intercept_)
print(lasso.coef_)
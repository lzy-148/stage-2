import numpy as np
def normal_equation(X,y):
    theta=np.linalg.inv(X.T@X)@X.T@y #正规方程
    return theta
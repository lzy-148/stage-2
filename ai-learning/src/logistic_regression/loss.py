import numpy as np

def binary_cross(y,p):
    eps=1e-8  ##防止log（0）
    loss=-np.mean(y*np.log(p+eps)+(1-y)*np.log(1-p+eps))
    return loss

from sklearn.metrics import log_loss
y_true=[0, 1, 0, 1]
y_prob=[0.1, 0.9, 0.2, 0.8]
loss = log_loss(y_true, y_prob)
print(loss)##库函数


y = np.array([0, 1, 0, 1])
p = np.array([0.1, 0.9, 0.2, 0.8])
loss2=binary_cross(y,p)
print(loss2)##实现

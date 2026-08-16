import numpy as np


def gradient(X, y, lr=0.01, epochs=10000,reg=None,lam=0.1):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    m = X.shape[0]
    theta = np.zeros((X.shape[1], 1), dtype=float)
    losslist = []

    for _ in range(epochs):
        pred=X@theta
        error=pred-y
        grad=(1/m)* X.T @error
        if reg=="l2":##惩罚偏置项b
            reg_term=np.copy(theta)
            reg_term[0]=0
            grad+=lam*reg_term
        if reg=="l1":
            reg_term=np.copy(np.sign(theta))
            reg_term[0]=0
            grad+=lam*reg_term
        theta -= lr * grad
        loss = np.mean(error**2)
        losslist.append(loss)

    return theta, losslist

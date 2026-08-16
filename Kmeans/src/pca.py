import numpy as np

def pca(X, n_components):
    mean = np.mean(X, axis=0)
    X_center = X - mean
    cov = np.dot(X_center.T, X_center) / (len(X) - 1)
    values, vectors = np.linalg.eigh(cov)
    idx = np.argsort(values)[::-1]
    values = values[idx]
    vectors = vectors[:, idx]
    components = vectors[:, :n_components]
    X_new = np.dot(X_center, components)
    return X_new

def pca_full(X):
    mean = np.mean(X, axis=0)
    X_center = X - mean
    cov = np.dot(X_center.T, X_center) / (len(X) - 1)
    values, vectors = np.linalg.eigh(cov)
    idx = np.argsort(values)[::-1]
    values = values[idx]
    vectors = vectors[:, idx]
    total = np.sum(values)
    explained_ratio = values / total
    return values, vectors, explained_ratio

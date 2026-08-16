import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(project_root))
import numpy as np
#自我实现
from src.pca import pca
X=np.array([
    [1,2],[2,3],[3,4],
    [8,9],[9,10],[10,11]
])
X_new=pca(X,n_components=1)
print("自己实现PCA:")#linalg.eig可能返回复数
print(X_new)
#sklearn库实现
from sklearn.decomposition import PCA
model_pca=PCA(n_components=1)
X_pca2=model_pca.fit_transform(X)
print("sklearn PCA:")
print(X_pca2)
print("解释方差比例:",model_pca.explained_variance_ratio_)

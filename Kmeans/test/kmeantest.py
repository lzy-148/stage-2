import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(project_root))
from src.kmeans import kmeans
import numpy as np
#自己实现
X=np.array([
    [1,2],[1,3],[2,2],
    [8,9],[9,8],[10,9]
])
centers,labels1=kmeans(X,k=2)#两个簇
print("中心点:")
print(centers)
print("分类结果:")
print(labels1)
#sklearn库实现
from sklearn.cluster import KMeans
model=KMeans(n_clusters=2,random_state=42)
labels2=model.fit_predict(X)
print("sklearn分类结果:")
print(labels2)
#轮廓系数实现比较
from sklearn.metrics import silhouette_score
score1=silhouette_score(X,labels1)
print("自己实现轮廓系数:",score1)
score2 = silhouette_score(X,labels2)
print("sklearn轮廓系数:", score2)
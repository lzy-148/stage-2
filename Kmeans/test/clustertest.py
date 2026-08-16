import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(project_root))
import numpy as np
#自我实现
from src.cluster import hierarchical
X=np.array([
    [1,2],[1,3],[2,2],
    [8,9],[9,8],[10,9]
])
X2=np.array([
    [1, 100],[2, 200],[3, 300],
    [8, 800],[9, 900],[10, 1000]
])
my_labels=hierarchical(X2,k=2)
print("自己实现层次聚类:")
print(my_labels)
#sklearn库实现
from sklearn.cluster import AgglomerativeClustering
model=AgglomerativeClustering(n_clusters=2)
labels=model.fit_predict(X2)
print("sklearn层次聚类:")
print(labels)
#聚类效果比较
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
#用尺度差别大的数据
score1=silhouette_score(X2,my_labels)
score2=silhouette_score(X2,labels)
print("自己实现轮廓系数:",score1)
print("sklearn轮廓系数:",score2)
model=KMeans(n_clusters=2,random_state=42)
labels_before=model.fit_predict(X2)
score_before=silhouette_score(X2,labels_before)
print("标准化前:",score_before)
scaler=StandardScaler()#标准化
X_scaled=scaler.fit_transform(X2)
model = KMeans(n_clusters=2,random_state=42)
labels_after = model.fit_predict(X_scaled)
score_after = silhouette_score(X_scaled,labels_after)
print("标准化后:",score_after)


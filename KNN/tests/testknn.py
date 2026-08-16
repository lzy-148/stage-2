
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
import numpy as np
from src.decision_tree.cart import DecisionTree
# 数据
X=np.array([[1,2],[2,3],[3,4],[8,9],[9,10],[10,11]])
y=np.array([0,0,0,1,1,1])
# 创建模型
tree=DecisionTree(
    max_depth=2
)
# 训练
tree.fit(
    X,
    y
)
# 测试
X_test=np.array([
    [2,4],
    [9,8]
])
pred=tree.predict(
    X_test
)
print(pred)

import numpy as np
class Node:
    def __init__(self,feature=None,threshold=None,left=None,right=None,value=None):
        self.feature=feature
        self.threshold=threshold
        self.left=left
        self.right=right
        self.value=value

class DecisionTree:
    def __init__(self,max_depth=3):
        self.max_depth=max_depth

    def gini(self,y):
        classes=np.unique(y)
        impure=1
        for i in classes:
            p=np.sum(y==i)/len(y)
            impure-=p**2
        return impure

    def split(self,X,feature,threshold):
        left=X[:,feature]<threshold
        right=~left
        return left,right

    def bestsplit(self,X,y):
        bestgini=1
        bestfeature=None
        bestthres=None
        n_features = X.shape[1]
        for feature in range(n_features):
            thresholds=np.unique(X[:,feature])
            for threshold in thresholds:
                left,right = self.split(X,feature,threshold)
                n_left=np.sum(left)
                n_right=np.sum(right)
                if n_left==0 or n_right==0:
                    continue
                g=(n_left*self.gini(y[left])+n_right*self.gini(y[right]))/len(y)
                if g<bestgini:
                    bestgini = g
                    bestfeature=feature
                    bestthres=threshold
        return (bestfeature,bestthres)

    def majority(self,y):
        values,counts=np.unique(y,return_counts=True)
        return values[np.argmax(counts)]

    #建立树
    def build_tree(self,X,y,depth=0):
        if depth>=self.max_depth:
            return Node(value=self.majority(y))
        feature,threshold=self.bestsplit(X,y)
        if feature is None:#无法继续划分
            return Node(value=self.majority(y))
        leftindex,rightindex=self.split(X,feature,threshold)
        #创建左右子树
        lefttree=self.build_tree(X[leftindex],y[leftindex],depth+1)
        rightree=self.build_tree(X[rightindex],y[rightindex],depth+1)
        return Node(feature,threshold,lefttree,rightree)

    def fit(self,X,y):
        self.root=self.build_tree(X,y)

    #单个预测
    def predict_one(self,X,node):
        if node.value is not None:
            return node.value
        if X[node.feature]<node.threshold:#判断走哪边
            return self.predict_one(X,node.left)
        else:
            return self.predict_one(X,node.right)

    #批量预测
    def predict(self,X):
        result=[]
        for x in X:
            result.append(self.predict_one(x,self.root))
        return np.array(result)
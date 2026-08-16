import numpy as np
def confusionmatrix(y_true, y_pred):
    TP=0
    TN=0
    FP=0
    FN=0
    for true,pred in zip(y_true,y_pred):
        if true==1 and pred==1:
            TP+=1
        elif true==0 and pred==0:
            TN+=1
        elif true==0 and pred==1:
            FP+=1
        elif true==1 and pred==0:
            FN+=1
    return TP,TN,FP,FN

def precision(y_true,y_pred):

    TP,TN,FP,FN=confusionmatrix(y_true,y_pred)
    if TP+FP==0:
        return 0
    return TP/(TP+FP)

def recall(y_true,y_pred):
    TP,TN,FP,FN=confusionmatrix(y_true,y_pred)
    if TP+FN==0:
        return 0
    return TP/(TP+FN)

def f1_score(y_true,y_pred):
    p=precision(y_true,y_pred)
    r=recall(y_true,y_pred)
    if p+r==0:
        return 0
    return 2*p*r/(p+r)

def accuracy(y_true,y_pred):
    TP,TN,FP,FN=confusionmatrix(y_true,y_pred)
    return (TP+TN)/(TP+TN+FP+FN)

def binary_cross_entropy(y_true,y_prob):
    eps=1e-8
    m=len(y_true)
    loss=0
    for y,p in zip(y_true,y_prob):
        loss+=(y*np.log(p)+(1-y)*np.log(1-p))
    return -loss/m

def auc(y_true,y_prob):
    pos=[]
    neg=[]
    for y,p in zip(y_true,y_prob):
        if y==1:
            pos.append(p)
        else:
            neg.append(p)
    count=0
    total=len(pos)*len(neg)
    for p in pos:
        for n in neg:
            if p>n:
                count+=1
            elif p==n:
                count+=0.5
    return count/total
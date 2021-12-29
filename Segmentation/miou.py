import torch
import numpy as np
def Miou(result, target):
    true = target.numpy().astype(np.bool)
    pred = result.numpy().astype(np.bool)
    TP = (true & pred).sum()
    TN = (~true & ~pred).sum()
    FP = (~true & pred).sum()
    FN = (true & ~pred).sum()
    return  float(TP)/float(FP + FN + TP)
def Dice(result,target):
    true = target.numpy().astype(np.bool)
    pred = result.numpy().astype(np.bool)
    TP = (true & pred).sum()
    TN = (~true & ~pred).sum()
    FP = (~true & pred).sum()
    FN = (true & ~pred).sum()
    return  float(2*TP)/float(FP + FN + 2*TP)

def Precision(result,target):
    true = target.numpy().astype(np.bool)
    pred = result.numpy().astype(np.bool)
    TP = (true & pred).sum()
    TN = (~true & ~pred).sum()
    FP = (~true & pred).sum()
    FN = (true & ~pred).sum()
    if FP + TP == 0:
        return 0
    return  float(TP)/float(FP + TP)
def TPR(result,target):
    true = target.numpy().astype(np.bool)
    pred = result.numpy().astype(np.bool)
    TP = (true & pred).sum()
    TN = (~true & ~pred).sum()
    FP = (~true & pred).sum()
    FN = (true & ~pred).sum()
    return  float(TP)/float(FP + FN)


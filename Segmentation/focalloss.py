import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np

class FocalLoss(nn.Module):
    def __init__(self, gamma=0, alpha=None, size_average=True):
        super(FocalLoss, self).__init__()
        self.gamma = gamma
        self.alpha = alpha
        if isinstance(alpha,(float,int)): self.alpha = torch.Tensor([alpha,1-alpha])
        if isinstance(alpha,list): self.alpha = torch.Tensor(alpha)
        self.size_average = size_average

    def forward(self, input, target):
        if input.dim()>2:
            input = input.view(input.size(0),input.size(1),-1)  # N,C,H,W => N,C,H*W
            input = input.transpose(1,2)    # N,C,H*W => N,H*W,C
            input = input.contiguous().view(-1,input.size(2))   # N,H*W,C => N*H*W,C
        target = target.view(-1,1)
        #print("target.shape",target.shape)
        #print("target.sum",target.sum())
        weight = target.sum().to(dtype=torch.float) / float(target.shape[0])
        #print("weight",weight)
        #print(input[0])

        logpt = F.log_softmax(input)
        #print(logpt.shape)
        #print(logpt[0])
        #print(target.shape)
        #print(logpt.shape)
        #print(target)
        logpt = logpt.gather(1,target) #寻找target对应位置的prediction
        #print(logpt.shape)
        target = target.view(-1)
        logpt = logpt.view(-1)
        #print(logpt)

        #print(logpt.shape)
        pt = Variable(logpt.data.exp())
        #if(target.sum() > 0 and weight != 1):
        #    logpt[target == 1] = logpt[target == 1] * (1 - weight) * 1000
         #   logpt[target == 0] = logpt[target == 0] * weight * 1000
        #else:
         #   logpt = logpt * 100
        #print("logpt",logpt)

        #print(pt[0])

        if self.alpha is not None:
            if self.alpha.type()!=input.data.type():
                self.alpha = self.alpha.type_as(input.data)
            at = self.alpha.gather(0,target.data.view(-1))
            logpt = logpt * Variable(at)

        loss = -1 * (1-pt)**self.gamma * logpt
        #loss = -1 * logpt

        #print(loss.shape)
        #print(loss)

        #rint(loss.sum())
        #print(loss.mean())
        if self.size_average: return loss.mean()
        else: return loss.sum()


if __name__ == "__main__":
    criterion = FocalLoss(gamma=5)
    #result_1 = torch.zeros((1,1,3,3)) + 1
    #result_2 = torch.zeros((1,1,3,3))
    #result = torch.cat((result_1,result_2),dim=1)
    #target = torch.zeros((3,3)).to(dtype=torch.long)
    #target = torch.tensor([[1,1,1],[0,0,1],[1,0,1]]).to(dtype=torch.long)
    #target = torch.ones((3,3)).to(dtype=torch.long)




    pred = torch.from_numpy(np.load("100.npyoutput77.npy").astype(np.bool))
    true = torch.from_numpy(np.load("100.npytarget77.npy").astype(np.bool))
    TP = (true & pred).float().sum()
    TN = (~true & ~pred).float().sum()
    FP = (~true & pred).float().sum()
    FN = (true & ~pred).float().sum()
    print(TP,TN,FP,FN)
    print(TP/(FP + FN + TP))



    #loss = criterion(result, target)
    #print(loss)

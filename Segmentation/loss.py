import torch
import torch.nn.functional as F
import torch.nn as nn
import numpy as np



# Recommend
class CrossEntropyLoss2d(nn.Module):
    def __init__(self, weight=None, size_average=True):
        super(CrossEntropyLoss2d, self).__init__()
        self.nll_loss = nn.NLLLoss2d(weight, size_average)

    def forward(self, inputs, targets):
        #print(inputs.size())
        return self.nll_loss(F.log_softmax(inputs,dim=1), targets)


class BinaryDiceLoss(nn.Module):
    def __init__(self, smooth=1, p=2, reduction='mean'):
        super(BinaryDiceLoss, self).__init__()
        self.smooth = smooth
        self.p = p
        self.reduction = reduction

    def forward(self, pred, target):
        """
        :param pred: (B, H, W)
        :param target: (B, H, W)
        :return:
        """
        assert pred.size(0) == target.size(0), "predicion and target batch size don't match"
        pred = pred.contiguous().view(pred.size(0), -1)
        target = target.contiguous().view(target.size(0), -1)

        # num = torch.sum(torch.mul(pred, target), dim=1) + self.smooth
        # den = torch.sum(pred.pow(self.p) + target.pow(self.p), dim=1) + self.smooth

        intersection = 2. * torch.sum(torch.mul(pred, target)) + self.smooth
        sum = torch.sum(pred.pow(self.p) + target.pow(self.p)) + self.smooth

        loss = 1 - intersection / sum
        # pdb.set_trace()
        return loss



class BCE_Loss(nn.Module):
    def __init__(self):
        super(BCE_Loss,self).__init__()
        self.bce=nn.BCELoss()
    def forward(self,inputs,targets):
        return self.bce(inputs,targets)

class DiceLoss(nn.Module):
    def __init__(self):
        super(DiceLoss, self).__init__()
        self.dice = BinaryDiceLoss()

    def forward(self, input, target):
        """
        :param input:  (B, C, H, W)
        :param target:  (B, C, H, W)
        :return:
        """

        C = target.size(1)
        # dice = BinaryDiceLoss()
        res = 0
        for i in range(0, C):
            diceloss = self.dice(input[:, i, :, :, :], target[:, i, :, :, :])
            res += diceloss

        return res / C

if __name__ == "__main__":
    pred = torch.from_numpy(np.load("100.npyoutput77.npy"))
    true = torch.from_numpy(np.load("100.npytarget77.npy"))
    print(pred.shape)
    #input = torch.zeros((4,2,3,3,3))
    #target = torch.zeros((4,2,3,3,3))
    criterion = DiceLoss()
    loss = criterion(pred,true)
    print(loss)
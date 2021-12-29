import argparse
import os
import shutil
import time
import logging
import numpy as np

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
from torch.utils.data import DataLoader
from focalloss import FocalLoss
from vnet import VNet
from miou import Miou
from loss import DiceLoss
from Vnetdataset import BasicDataset


index = 3
device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
#device = torch.device("cpu")
print(device)

def main():
    model = VNet().to(device)

    ckpts = 'ckpts'
    if not os.path.exists(ckpts): os.makedirs(ckpts)


    train_loader = DataLoader(
        BasicDataset("train_data/img","train_data/gt"),
        batch_size=10,shuffle=True)


    valid_loader = DataLoader(
        BasicDataset("valid_data/img","valid_data/gt"),
        batch_size=2)


    #criterion = nn.CrossEntropyLoss()
    criterion = FocalLoss(gamma=0).to(device)
    #criterion = DiceLoss()

    optimizer = torch.optim.SGD(model.parameters(), 1e-1,
                                momentum=0.9,
                                weight_decay=5e-4)

    for epoch in range(0, 500):
        print('epoch',epoch)

        train(train_loader, model, criterion, optimizer, valid_loader)

        file_name = os.path.join(ckpts, 'model_epoch_%d.pt' % (epoch + 1, ))
        if((epoch + 1) % 10 == 0):
            torch.save(model.state_dict(),file_name)


def train(train_loader, model, criterion, optimizer, valid_loader):

    model.train()

    for i, data in enumerate(train_loader):
        #print(i)
        x1, target= data
        #print(target)
        #print(x1.shape)
        #print(x2.shape)
        #print(target.shape)
        target = target.to(device)
        #x1 = x1.permute((1, 0, 2, 3, 4))
        x1 = x1.view(-1, 1, x1.shape[-3], x1.shape[-2], x1.shape[-1])
        print("x1.shape:",x1.shape)
        #x2 = x2.view(-1, 1, x2.shape[-3], x2.shape[-2], x2.shape[-1])
        target = target.view(-1, 1, target.shape[-3], target.shape[-2], target.shape[-1])
        #x2 = x1
        #x3 = x1
        #x1 = torch.cat((x1,x2,x3), dim=1)
        #x2 = x2.view(-1, 1, , 19, 19)
        #target = target.permute((1, 0, 2, 3, 4))

        #print("target.sum():", target.sum())
        x1 = x1.to(device)
        #x2 = x2.cuda()
        #print("x1.shape",x1.shape)
        #print("x2.shape",x2.shape)
        #x2 = x2.cuda()
        output = model(x1) # nx2x9x9x9
        target = target.to(dtype = torch.long)
        output = output.to(dtype = torch.float)
        miou = Miou(output.argmax(dim=1).cpu(), target.cpu().squeeze())

        loss = criterion(output, target)
        print("train loss:  ", loss, "miou: ", miou)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        for i, data in enumerate(valid_loader):
            #print(i)
            x1,target = data
            #print(x1.shape)
            #print(x2.shape)
            #print(target.shape)
            target = target.to(device)
            #print("target.sum",target.sum())
            #x1 = x1.permute((1, 0, 2, 3, 4))
            x1 = x1.view(-1, 1, x1.shape[-3], x1.shape[-2], x1.shape[-1])
            #x2 = x2.view(-1, 1, x2.shape[-3], x2.shape[-2], x2.shape[-1])
            target = target.view(-1, 1, target.shape[-3], target.shape[-2], target.shape[-1])
            #print("target.sum():", target.sum())
            x1 = x1.to(device)
            #x2 = x2.cuda()
            output = model(x1) # nx2x9x9x9
            #print("output.sum():", output.sum())
            #output = output.permute(0, 2, 3, 4, 1).contiguous()
            #output = output.view(-1, 2)
            #target = target.view(-1)
            target = target.to(dtype=torch.long)
            output = output.to(dtype=torch.float)
            miou = Miou(output.argmax(dim=1).cpu(), target.cpu().squeeze())
            loss = criterion(output, target)
            #print("#############################")
            print("valid loss: ",loss, "miou: ", miou)
            #print("valid loss: ",loss)





def save_checkpoint(state,  filename='checkpoint.pth.tar'):
    torch.save(state, filename)
    #shutil.copyfile(filename, 'model_best.pth.tar')


class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def adjust_learning_rate(optimizer, epoch):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""
    lr = 1e-1 * (0.1 ** (epoch // 1))
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


if __name__ == '__main__':
    main()
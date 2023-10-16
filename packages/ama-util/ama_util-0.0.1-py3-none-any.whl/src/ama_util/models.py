
import torch.nn as nn
import torch
import numpy as np
from torch.nn import functional as F
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
class ModelSE3d1_Neu150_ST_Exp(nn.Module):
    def __init__(self):
        super(ModelSE3d1_Neu150_ST_Exp,self).__init__()
        self.numoffea=16 #number of features
        self.sizeoffea=28*24 #36*32 # 28*24 #size of feature
        self.numofneuron=86 #number of neurons
        #
        #spatial kernel, self.kernel_size=9 #odd number
        self.conv1_ss=nn.Parameter(torch.zeros(self.numoffea,2,1,9,9))
        std=1. / np.sqrt(2*1*9*9)
        #self.conv1_ss.data.uniform_(-1e-4, 1e-4)
        self.conv1_ss.data.uniform_(-std*0.1, std*0.1) #(-std*0.001, std*0.001)
        self.conv1_ss_bias=nn.Parameter(torch.zeros(self.numoffea))
        self.conv1_ss_bias.data.uniform_(-std, std)
        #temporal kernel
        self.conv1_st=nn.Conv3d(self.numoffea,self.numoffea,kernel_size=(50,1,1),stride=1)
        #
        self.fc1=nn.Linear(self.numoffea*self.sizeoffea,self.numofneuron)
    #
    def forward(self, x):
        #encoded = self.conv1_ss(x)
        encoded = F.conv3d(x, self.conv1_ss, bias=self.conv1_ss_bias,stride=1,padding=(0,0,0))
        encoded = self.conv1_st(encoded)
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea)
        encoded = torch.exp(self.fc1(encoded))
        return encoded
        
class AC_1(nn.Module):
    def __init__(self):
        super(AC_1,self).__init__()
        self.numoffea=16 # number of features
        self.sizeoffea=28*24 #(36-9+1)*(32-9+1) ->28*24 #size of feature
        self.numofneuron=86 #number of neurons
        self.ones = torch.ones(1,1,1,1).to('cuda')
        self.conv1_ss=nn.Parameter(torch.zeros(self.numoffea,2,1,9,9))
        std=1. / np.sqrt(2*1*9*9)
        self.conv1_ss.data.uniform_(-std*0.1, std*0.1) #(-std*0.001, std*0.001)
        self.conv1_ss_bias=nn.Parameter(torch.zeros(self.numoffea))
        self.conv1_ss_bias.data.uniform_(-std, std)
        
        # represent the strength of lateral inhibition
        self.inhib_alpha = nn.Parameter(torch.zeros((16,1)))
        
        # the gaussian kernel
        tmp_gau = torch.zeros((1,1,5,5));tmp_gau[0,0] = cal_gau(5,1.0,0)
        self.gaussian_kernel_2d = tmp_gau.to('cuda')
        
        self.conv1_st=nn.Conv3d(self.numoffea,self.numoffea,kernel_size=(50,1,1),stride=1)
        self.fc1=nn.Linear(self.numoffea*self.sizeoffea,self.numofneuron)
        
    def forward(self, x):
        # input: 200, 16, 50, 28, 24
        encoded = F.conv3d(x, self.conv1_ss, bias=self.conv1_ss_bias,stride=1,padding=(0,0,0))
        encoded = self.conv1_st(encoded)
        for f_m in range(16):
            feature_channel = encoded[:, f_m, :, :, :]
            
            center = F.conv2d(feature_channel,self.ones)
            surround = F.conv2d(feature_channel,self.gaussian_kernel_2d,padding=2)
            
            encoded[:,f_m] = center-self.inhib_alpha[f_m]*surround 
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea)
        encoded = torch.exp(self.fc1(encoded))
        return encoded

class AC_1_cpu(nn.Module):
    def __init__(self):
        super(AC_1_cpu,self).__init__()
        self.numoffea=16 # number of features
        self.sizeoffea=28*24 #(36-9+1)*(32-9+1) ->28*24 #size of feature
        self.numofneuron=86 #number of neurons
        self.ones = torch.ones(1,1,1,1).to('cuda')
        self.conv1_ss=nn.Parameter(torch.zeros(self.numoffea,2,1,9,9))
        std=1. / np.sqrt(2*1*9*9)
        self.conv1_ss.data.uniform_(-std*0.1, std*0.1) #(-std*0.001, std*0.001)
        self.conv1_ss_bias=nn.Parameter(torch.zeros(self.numoffea))
        self.conv1_ss_bias.data.uniform_(-std, std)
        
        # represent the strength of lateral inhibition
        self.inhib_alpha = nn.Parameter(torch.zeros((16,1)))
        
        # the gaussian kernel
        tmp_gau = torch.zeros((1,1,5,5));tmp_gau[0,0] = cal_gau(5,1.0,0)
        self.gaussian_kernel_2d = tmp_gau.to('cuda')
        
        self.conv1_st=nn.Conv3d(self.numoffea,self.numoffea,kernel_size=(50,1,1),stride=1)
        self.fc1=nn.Linear(self.numoffea*self.sizeoffea,self.numofneuron)
        
    def forward(self, x):
        # input: 200, 16, 50, 28, 24
        encoded = F.conv3d(x, self.conv1_ss, bias=self.conv1_ss_bias,stride=1,padding=(0,0,0))
        encoded = self.conv1_st(encoded)
        for f_m in range(16):
            feature_channel = encoded[:, f_m, :, :, :]
            
            center = F.conv2d(feature_channel,self.ones)
            surround = F.conv2d(feature_channel,self.gaussian_kernel_2d,padding=2)
            
            encoded[:,f_m] = center-self.inhib_alpha[f_m]*surround 
        encoded = encoded.view(-1,self.numoffea*self.sizeoffea)
        encoded = torch.exp(self.fc1(encoded))
        return encoded
import numpy as np
import torch
import datetime
import torch.nn as nn
from torch.nn import functional as F
from scipy.stats import pearsonr
def model_train(model,data,optimizer,device,EPOCH,loss_func,valdata,alpha=None,beta=None,alpha2=None,\
                earlystop=False,verbose=True):
    print(datetime.datetime.now())
    loss=0.0
    trainlosses=np.zeros((EPOCH))
    vallosses  =np.zeros((EPOCH)) # save validation losses of all epochs until early stopping
    for epoch in range(EPOCH):
        model=model.to(device)
        model=model.train()
        for step, (x,y) in enumerate(data):
            #some preprocessing
            #x=preprocess_np(x,model,pre_method,region)
            x=torch.from_numpy(x).float()
            y=torch.from_numpy(y).float()
            b_x = x.to(device) 
            b_y = y.to(device)

            encoded = model(b_x)
            loss=loss_func(encoded, b_y,alpha,alpha2,beta,[model.conv1_ss],[model.conv1_st],[model.fc1])
            
            # last epoch to get the training loss, keep the same sample size as validation
            trainlosses[epoch]=trainlosses[epoch]+loss.detach().clone().cpu().data.numpy()
            #
            optimizer.zero_grad()               # clear gradients for this training step
            loss.backward()                     # backpropagation, compute gradients
            optimizer.step()                    # apply gradients
            #
            if step % 100 == 0 and verbose==True:
                print('Model: ',model.__class__.__name__,'|Epoch: ', epoch,\
                      '| train loss: %.4f' % loss.cpu().data.numpy())
        # one epoch done
        # scheduler.step()
        
        # validation
        vallosses[epoch]=model_val(model,valdata,1,device)
        trainlosses[epoch] =trainlosses[epoch]/len(data)
        
        if epoch>10 and earlystop==True: # epoch>20, early stopping check after each epoch, use CC as a metric
            if epoch-np.argmax(vallosses)>4: # >4
                break
    print ('Epoch: {:} val loss: {:.4f}, finish training!'.format(epoch,vallosses[epoch]))
    print(datetime.datetime.now())
    return trainlosses,vallosses

def Ploss_L2L1_SE_ST(recon_x, x, alpha1, alpha2, beta, alpha_x1, alpha_x2, beta_y): # for spatial and temporal separable model
    tempB, tempN =x.size()
    Ploss = F.poisson_nll_loss(recon_x, x,log_input=False, reduction='sum')
    l2temp=0.0
    for temp in alpha_x1:
        l2temp = l2temp+ temp.norm(2)
    l2temp2=0.0
    for temp in alpha_x2:
        l2temp2 = l2temp2+ temp.weight.norm(2)
    L2loss=alpha1*l2temp+alpha2*l2temp2
    #
    l1temp=0.0
    for temp in beta_y:
        l1temp = l1temp+ temp.weight.norm(1)
    L1loss=beta*l1temp
    return Ploss+L2loss+L1loss

def model_val(model,data,val_eg,device,loss_func=None):
    model=model.to(device)
    model=model.eval()
    if 'AC' in model.__class__.__name__:
        model.gaussian_kernel_2d = model.gaussian_kernel_2d.to(device)
        model.ones = model.ones.to(device)
    (x,y)=data
    x=torch.from_numpy(x).float()
    b_x = x.to(device) 
    with torch.no_grad():
        encoded = model(b_x)
    # CC as metric
    encoded_np=encoded.cpu().data.numpy()

    numCell = y.shape[-1]
    valcc,valpV = np.zeros(numCell),np.zeros(numCell)
    for cell in range(numCell):
        testccs[cell],valps[cell] = pearsonr(encoded_np[x.shape[2]-1:,cell],y[x.shape[2]-1:,cell])
        if valps[cell]>0.05:
            testccs[cell]=0
    return valccs,valps


def model_test(model,data,device,use_pad0_sti=True):
    model=model.to(device)
    model=model.eval()
    if 'AC' in model.__class__.__name__:
        odel.gaussian_kernel_2d = model.gaussian_kernel_2d.to(device)
        model.ones = model.ones.to(device)

    (x,y)=data
    x=torch.from_numpy(x).float()
    b_x = x.to(device) 
    encoded = model(b_x)
    encoded_np=encoded.cpu().data.numpy()

    if use_pad0_sti==False:
        encoded_np=encoded_np[7:,:]
        y=y[7:,:]

    numCell = y.shape[-1]
    testccs,testps = np.zeros(numCell),np.zeros(numCell)
    for cell in range(numCell):
        testccs[cell],testps[cell] = pearsonr(encoded_np[x.shape[2]-1:,cell],y[x.shape[2]-1:,cell])
    return testccs,testps


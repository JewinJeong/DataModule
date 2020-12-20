import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import csv
import numpy as np
import time


class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        # self.fc1 = nn.Linear(6, 6, True)
        # self.fc2 = nn.Linear(6, 6, True)
        # self.fc3 = nn.Linear(6, 6, True)
        self.fc4 = nn.Linear(6, 5, True)
        self.fc5 = nn.Linear(5, 4, True)

        self.hidden = nn.Sequential(
            # self.fc1,
            # nn.Tanh(),
            # self.fc2,
            # nn.Tanh(),
            # self.fc3,
            # nn.Tanh(),
            self.fc4,
            nn.Tanh(),
            self.fc5,
        )

    def forward(self, x):
        return self.hidden(x).view(-1)


def dnngo(ccc) :

    EPOCHS_TO_TRAIN = 1000
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


    net = Net()
    net = torch.load("haksoop.pth")
    net.eval()
    #net.to(device)
    haksoop = 0.8



    f = open('gunlight.csv','r')
    rdr1 = list(csv.reader(f))
    rdr1 = np.array(rdr1)
    #rdr1_tr = rdr1[0:int(len(rdr1 * haksoop))]
    #rdr1_ts = rdr1[int(len(rdr1 * haksoop)):len(rdr1)]

    rdr1_target = np.random.randint(1, 2, size=(len(rdr1)))
    rdr1_target = np.array([rdr1_target,np.zeros(len(rdr1)),np.zeros(len(rdr1)) ,np.zeros(len(rdr1)) ])
    rdr1_target = np.transpose(rdr1_target)



    f = open('laser.csv','r')
    rdr2 = list(csv.reader(f))
    rdr2 = np.array(rdr2)
    #rdr2_tr = rdr2[0:int(len(rdr2 * haksoop))]
    #rdr2_ts = rdr2[int(len(rdr2 * haksoop)):len(rdr2)]
    rdr2_target = np.random.randint(1, 2, size=(len(rdr2)))
    rdr2_target = np.array([np.zeros(len(rdr2)), rdr2_target, np.zeros(len(rdr2)), np.zeros(len(rdr2))])
    rdr2_target = np.transpose(rdr2_target)

    f = open('trash.csv','r')
    rdr3 = list(csv.reader(f))
    rdr3 = np.array(rdr3)
    #rdr3_tr = rdr3[0:int(len(rdr3 * haksoop))]
    #rdr3_ts = rdr3[int(len(rdr3 * haksoop)):len(rdr3)]
    rdr3_target = np.random.randint(1, 2, size=(len(rdr3)))
    rdr3_target = np.array([np.zeros(len(rdr3)), np.zeros(len(rdr3)), rdr3_target, np.zeros(len(rdr3)) ])
    rdr3_target = np.transpose(rdr3_target)


    f = open('lighttest.csv','r')
    rdr4 = list(csv.reader(f))
    rdr4 = np.array(rdr4)
    #rdr3_tr = rdr3[0:int(len(rdr3 * haksoop))]
    #rdr3_ts = rdr3[int(len(rdr3 * haksoop)):len(rdr3)]
    rdr4_target = np.random.randint(1, 2, size=(len(rdr4)))
    rdr4_target = np.array([np.zeros(len(rdr4)),np.zeros(len(rdr4)), np.zeros(len(rdr4)), rdr4_target ])
    rdr4_target = np.transpose(rdr4_target)


    f.close()



    tru_data=np.r_[rdr1,rdr2,rdr3,rdr4]
    tru_data = tru_data.astype(float)



    tru_max = np.max(tru_data, axis=0)
    tru_min = np.min(tru_data, axis=0)
    nano = tru_max-tru_min
    tru_data = tru_data - tru_min
    tru_data = tru_data / nano


    #tru_target=np.r_[rdr1_target,rdr2_target,rdr3_target]
    tru_target = np.vstack([rdr1_target, rdr2_target, rdr3_target, rdr4_target])

    # test
    #tru_target = tru_target * 0.5
    #test
    tru_data = tru_data.tolist()
    tru_target = tru_target.tolist()


    tru_data = list(map(lambda s: Variable(torch.Tensor([s])), tru_data))
    tru_target = list(map(lambda s: Variable(torch.Tensor([s])), tru_target))
    #tru_data = torch.FloatTensor(tru_data)
    #tru_target = torch.FloatTensor(tru_target)


    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=0.002)

    def ggakugi(a):
        return (a - tru_min)/nano




    '''
    print("Training loop:")
    for idx in range(0, EPOCHS_TO_TRAIN):
        for input, target in zip(tru_data, tru_target):
            optimizer.zero_grad()   # zero the gradient buffers
            output = net(input)
            if idx%30 ==0:
                print("input " + str(input.data.numpy()))
                print(" output : " + str(output.data.numpy()))
                print("target :" + str(target.data.numpy()))
    
    
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()    # Does the update
        if idx % 100 == 0:
            print("Epoch {: >8} Loss: {}".format(idx, loss.data.numpy()))
            torch.save(net, "haksoop.pth")
    
    
    
    
    start = time.time()
    print("")
    print("Final results:")
    for input, target in zip(tru_data, tru_target):
        output = net(input)
        print("input ::::")
        print(input)
        print("Input:[{},{}] Target:[{}] Predicted:[{}]".format(
            int(input.data.numpy()[0][0]),
            int(input.data.numpy()[0][1]),
            str(target.data.numpy()),
            str(output.data.numpy())
            #round(float(abs(target.data.numpy()[0] - output.data.numpy()[0])), 4)
        ))
    '''



    #print("time : "+ str((time.time() - start)*200/425))


    #ccc = list(map(lambda s: Variable(torch.Tensor([s])), ccc))
    print("Ccc : ")

    print(ccc)
    ccc = (ccc-tru_min)/nano
    ccc2 = net(torch.from_numpy(np.array(ccc)).type(dtype=torch.float32))
    #ccc2 = torch.unsqueeze(ccc2, 0)
    print("ccc2 : ")
    print(ccc2)

    #output = net(ccc2)


    p = ccc2.data.numpy()
    pp = np.argmax(p, axis= 0)
    str = ""
    if pp == 0 :
        str = "_gun"
    if pp == 1 :
        str = "_laser"
    if pp == 2 :
        str = "_none"
    if pp == 3 :
        str = "_flash"

    #print("str : " + str)

    return str



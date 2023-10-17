import scipy as sc
import scipy.sparse as sp
import numpy as np
import pandas as pd
import os
import re
import matplotlib.pyplot as plt


def timereport(path, file):
    data = pd.read_csv(path + "report/" + file)
    data = data.to_numpy()
    fig = plt.figure()
    plt.plot(data)
    plt.xlabel("Generation")
    plt.ylabel("Compute time")
    plt.show()  

def basic_plotter(num, c, mutlim, path, select=0):
    # path = "E:/Simulations/Pos Neg Evolution/x5 Test/Test1/%5Ctest"
    
    y = [0 for i in range(num)]
    x = [i for i in range(num)]
    
    for i in range(num):
        a = sc.sparse.load_npz(path + "_" + str(i) + ".npz")
        y[i] = a._shape[0]
        if i % c == 0:
            temp = []
            if select:
                temp= a[:,1].toarray() + a[:,2].toarray()
            else:
                temp = a[:,1].toarray()
            fig = plt.figure()
            plt.hist(temp)
            plt.xlim(mutlim)
            plt.xlabel("Mutation number")
            plt.ylabel("Cells number")
            plt.show()
            
            # temp = a[:,0].toarray()
            # fig = plt.figure()
            # plt.hist(np.log10(temp))
            # plt.xlim(mutlim)
            # plt.xlabel("Fitness parameter [log10]")
            # plt.ylabel("Cells number")
            # plt.show()
    
    fig = plt.figure()
    plt.plot(x,y)
    plt.xlabel("Generation")
    plt.ylabel("Population size")
    plt.show()   
  
def npztotxt(path_in, fname):
    a = sc.sparse.load_npz(path_in + fname)
    df = pd.DataFrame(a.toarray())
    if a._shape[1] == 3:
        df.columns = ["fitness", "positive mutation number", "negative mutation number"]
        os.makedirs(path_in + "/CSV/", exist_ok=True)
        df.to_csv(path_in + "/CSV/" + fname.rstrip(".npz") + ".csv", index=False)
    else:
        columns = ["fitness", "mutation number"]
        # for i in range(a._shape[0] - 1):
        #     columns.append(str(i))
        df.columns = columns      
        os.makedirs(path_in + "/CSV/", exist_ok=True)
        df.to_csv(path_in + "/CSV/" + fname.rstrip(".npz") + ".csv", index=False)
 
def stoalfafit(path, folders, mi, ma, step, name, analytical=False):
    dt = []
    _filter = (lambda x: [a.endswith('.npz') for a in x])
    columns = []
    for i in folders:
        # columns = np.append(columns, np.repeat("%.4f" % ((i-1)*step + mi*(i-1==0)), 3))
        # columns = np.append(columns, np.repeat(i, 3))
        files = np.array(os.listdir(path + i))
        files = files[_filter(files)]
        a = np.zeros((3, 2))
        for j in files:
            # idx = int(float(re.search(r'\d+.\d+', j[::1]).group())/50)
            idx = int(float(re.search(r'\d+.\d+', j[int(len(j)/2):len(j)]).group()))
            if idx == 2500 or idx == 5000 or idx == 7500:
                idx = int(idx / 2500 - 1)
                file = sp.load_npz(path + str(i) + '/' + j).toarray()
                if analytical:
                    a[idx,0] = np.sum(file[:,1] * file[:,0]) / np.sum(file[:,1])
                    a[idx,1] = np.sum(file[:,1] * ((file[:,0] - a[idx,0]))**2) / np.sum(file[:,1]) 
                else:
                    a[idx,0] = np.sum(file, axis=0)[1] / len(file)
                    a[idx,1] = np.std(file[:,1])**2
                    # a[idx,2] = np.median(file[:,1])
        if dt == []:
            dt = a
        else:
            dt = np.append(dt, a, axis=0)
            
    
    df = pd.DataFrame(dt)
    # df.columns = columns
    df.columns = ["mean" , "variance"]
    df.to_csv(path + name + '.csv')

def plot3DSP(s, p, data):
    # S = pd.read_csv(s, sep='\t', header=None)
    # P = pd.read_csv(p, sep='\t', header=None)
    data = pd.read_csv(data, sep='\t', header=None)
    
    S = np.array([x for x in range(11)]) * 0.0005
    S[0] = 0.0001
    P = np.array([x for x in range(11)]) * 0.005
    P[0] = 0.001
    data = data.to_numpy()
    
    fig = plt.figure(figsize=(8, 3))
    ax1 = fig.add_subplot(121, projection='3d')
    
    ss, pp = np.meshgrid(S, P)
    top = data.ravel()
    bottom = np.zeros_like(top)
    width = depth = 0.01

    ax1.scatter3D(ss.ravel(), pp.ravel(), top)
    
    # _x = np.arange(4)
    # _y = np.arange(5)
    # _xx, _yy = np.meshgrid(_x, _y)
    # x, y = _xx.ravel(), _yy.ravel()
    
    # top = x + y
    # bottom = np.zeros_like(top)
    # width = depth = 1
    
    # ax1.bar3d(x, y, bottom, width, depth, top, shade=True)
    # ax1.set_title('Shaded')
    
    # df = pd.DataFrame({'s' : ss.ravel(),
    #                    'p' : pp.ravel(),
    #                    'data' : top})
    # df.to_csv("E:/Simulations/S_P_test/data.csv")
    
    plt.show()

def varAprox(path):
    data = pd.read_csv(path)
    a = 0

if __name__ == "__main__":
    path = 'E:/Simulations/Alfa test/Normal/'
    files = np.array(os.listdir(path))
    files = files[np.array(list(map(lambda x: not x.endswith('.csv'), files)))]
    _filter = list(map(lambda x: x.endswith('3'), files))
    var = files[_filter]
    stoalfafit(path, var, 0, 0, 0, "normal_3_chart_data", False)
    
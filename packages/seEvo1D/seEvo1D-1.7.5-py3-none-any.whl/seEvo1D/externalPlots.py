import scipy as sc
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import os

alfa_state = []
alfa_var = []

def readPaths(file_path):
    path = file_path.split("/")
    out = ""
    name = ""
    number = ""
    
    for i in path:
        if i.endswith(".npz"):
            i = i.split('_')
            for x in i:
                if x.endswith(".npz"):
                    number = x.rstrip(".npz")
                else:
                    name = name + x + '_'
            name.lstrip('_')
        else:
            out = out + i + '/'
    out = out + "Figures/"
    return [file_path, out, name, float(number)]        
    
def mutationWave(file_path):
    # print(file_path)
    for x in file_path:
        _in, _out, _name, _num = readPaths(x)
        fig = plt.figure(figsize=(40,20))
        ax = fig.add_subplot() 
        pop = sc.sparse.load_npz(_in)
        popSize = 0
        
        if 'analytical' in _name:
            popSize = sum(pop[:,1].toarray())
            ax.plot(pop[:,0].toarray(), pop[:,1].toarray(), 'k', linewidth='10')
            
        elif 'binned' in _name:
            popSize = sum(pop[:,1].toarray())
            ax.bar(pop[:,0].toarray().T[0], pop[:,1].toarray().T[0], width=1, color='blue')   
            
        elif 'normal' in _name:                    
            popSize = pop._shape[0]
            _min = int(min(pop[:,1].toarray()))
            _max = int(max(pop[:,1].toarray()))
            data = np.zeros((int(_max - _min) + 1, 2))
            data[:,0] = np.array([x for x in range(_min, _max+1, 1)])
            for i in pop[:,1].toarray():
                data[int(i) - _min, 1] = data[int(i) - _min, 1] + 1
            ax.bar(data[:,0], data[:,1], width=1, color='red')
            
        # ax.legend(prop={'size':30})
        
        ax.set_xlabel("Mutation number", labelpad=50, fontdict={'fontsize':50})
        ax.set_ylabel("Cells", labelpad=50, fontdict={'fontsize':50})
        ax.set_title("Mutation Wave, N(t), t=%s, Population: %i" % (_num, popSize), pad=50, fontdict={'fontsize':70})
        
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(40) 
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(40) 
        
        try:
            os.makedirs(_out + "mutation_wave/", exist_ok=True) 
        except OSError as error:
            print(error)
        finally:
            if os.path.exists(_out + "mutation_wave/%s_mutation_wave.eps" % _num):
                os.remove(_out + "mutation_wave/%s_mutation_wave.eps" % _num)
            if os.path.exists(_out + "mutation_wave/%s_mutation_wave.jpg" % _num):
                os.remove(_out + "mutation_wave/%s_mutation_wave.jpg" % _num)
                
            fig.savefig(_out + "mutation_wave/%s_mutation_wave.jpg" % _num)
            fig.savefig(_out + "mutation_wave/%s_mutation_wave.eps" % _num)
            plt.close(fig)            
    
def fitnessWave(file_path):
    for x in file_path:
        _in, _out, _name, _num = readPaths(x)
        fig = plt.figure(figsize=(40,20))
        ax = fig.add_subplot() 
        pop = sc.sparse.load_npz(_in)
        popSize = 0
        
        if 'analytical' in _name:
            print('same as mutation wave')
            continue
        
        if 'binned' in _name:
            print('same as mutation wave')
            continue
        
        elif 'normal' in _name:        
            popSize = pop._shape[0]            
            ax.hist(pop[:,0].toarray(), color='red')
            
        # ax.legend(prop={'size':30})
        
        ax.set_xlabel("Fitness", labelpad=50, fontdict={'fontsize':50})
        ax.set_ylabel("Cells", labelpad=50, fontdict={'fontsize':50})
        ax.set_title("Fitness Wave, Population: %i" % (popSize), pad=50, fontdict={'fontsize':70})
        
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(40) 
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(40) 
        
        try:
            os.makedirs(_out + "fitness_wave/", exist_ok=True)
        except OSError as error:
            print(error)
        finally:
            if os.path.exists(_out + "fitness_wave/%s_fitness_wave.eps" % _num):
                os.remove(_out + "fitness_wave/%s_fitness_wave.eps" % _num)
            if os.path.exists(_out + "fitness_wave/%s_fitness_wave.jpg" % _num):
                os.remove(_out + "fitness_wave/%s_fitness_wave.jpg" % _num)
            fig.savefig(_out + "fitness_wave/%s_fitness_wave.jpg" % _num)
            fig.savefig(_out + "fitness_wave/%s_fitness_wave.eps" % _num)
            plt.close(fig)            

def combainedMutWave(file_path):
    _out = ''
    fig = plt.figure(figsize=(40,20))
    ax = fig.add_subplot() 
    ax.clear()
    for x in file_path:
        _in, _out, _name, _num = readPaths(x)
        
        pop = sc.sparse.load_npz(_in)
        popSize = 0
        
        if 'analytical' in _name:
            ax.plot(pop[:,0].toarray(), pop[:,1].toarray(), 'k', linewidth='10')
            
        elif 'binned' in _name:
            ax.bar(pop[:,0].toarray().T[0], pop[:,1].toarray().T[0], width=0.5, color='blue')
            
        elif 'normal' in _name:       
            temp = pop.toarray()
            _min = int(min(pop[:,1].toarray()))
            _max = int(max(pop[:,1].toarray()))
            data = np.zeros((_max - _min + 1, 2))
            data[:,0] = np.array([x for x in range(int(_min), int(_max)+1, 1)])
            for i in pop[:,1].toarray():
                data[int(i) - _min, 1] = data[int(i) - _min, 1] + 1
            ax.bar(data[:,0], data[:,1], width=1, color='red')
                    
    ax.set_xlabel("Mutation number", labelpad=50, fontdict={'fontsize':50})
    ax.set_ylabel("Population size", labelpad=50, fontdict={'fontsize':50})
    ax.set_title("Mutation waves", pad=50, fontdict={'fontsize':70})
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(40) 
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(40)  
    
    try:
        os.makedirs(_out, exist_ok=True) 
    except OSError as error:
        print(error)
    finally:
        if os.path.exists(_out + "combined_mutation_wave.eps"):
            os.remove(_out + "combined_mutation_wave.eps")
        if os.path.exists(_out + "combined_mutation_wave.jpg"):
            os.remove(_out + "combined_mutation_wave.jpg")
        fig.savefig(_out + "combined_mutation_wave.jpg")
        fig.savefig(_out + "combined_mutation_wave.eps")
        plt.close(fig)  

def popGrowth(file_path):
    data = []
    _out = ''
    for x in file_path:
        _in, _out, _name, _num = readPaths(x)
        
        pop = sc.sparse.load_npz(_in)
        popSize = 0
        
        if 'analytical' in _name:
            popSize = int(sum(pop[:,1].toarray())[0])
        
        elif 'normal' in _name:       
            popSize = pop._shape[0]
            
        elif 'binned' in _name:
            popSize = int(sum(pop[:,1].toarray())[0])
        
        data.append([_num, popSize])
        
    df = pd.DataFrame(data)
    df.columns = ["id","size"]
    
    ax = df.plot.line(x='id', y='size', figsize=(40,20), linewidth='10')
    
    ax.set_xlabel("Generation", labelpad=50, fontdict={'fontsize':50})
    ax.set_ylabel("Population size", labelpad=50, fontdict={'fontsize':50})
    ax.set_title("Population growth, N(t)", pad=50, fontdict={'fontsize':70})
    
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(40) 
    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(40) 
    
    fig = ax.get_figure()    
    
    try:
        os.makedirs(_out, exist_ok=True) 
    except OSError as error:
        print(error)
    finally:
        if os.path.exists(_out + "population_growth.eps"):
            os.remove(_out + "population_growth.eps")
        if os.path.exists(_out + "population_growth.jpg"):
            os.remove(_out + "population_growth.jpg")
        fig.savefig(_out + "population_growth.jpg")
        fig.savefig(_out + "population_growth.eps")
        plt.close(fig)  

def evolutionDynamics(an_path, norm_path, binned = False, out="", var = 0):
    an = np.array(list(map(readPaths, an_path)))
    an = an[np.array(list(map(lambda x: float(x), an[:,3]))).argsort()]
    name_an = an[0,2].rstrip('_analytical_')    
    _out_an = an[0,1]
    
    norm = np.array(list(map(readPaths, norm_path)))
    norm = norm[np.array(list(map(lambda x: float(x), norm[:,3]))).argsort()]
    
    norm_id = 'normal' * (not binned) + 'binned' * (binned)
    norm_col = 'red' * (not binned) + 'blue' * (binned)
    
    name_norm = norm[0,2].rstrip('_'+ norm_id +'_')
    _out_norm = norm[0,1]
    
    ind = int(min(len(an[:,0]), len(norm[:,0]))/3)
    ix1 = ind
    ix2 = ind * 2
    ix3 = ind * 3
    ix = np.array([[ix1], [ix2], [ix3]])
    mWave = np.append(an[ix,[0,2,3]], norm[ix,[0,2,3]], axis=0)
    mWave = np.array(list(map(lambda x: [sc.sparse.load_npz(x[0]), x[2], 'analytical' in x[1]], mWave)))
    
    fig, ax = plt.subplots(3,2, figsize=(30,30))
    fig.tight_layout(pad=10.0)
    
    ax[0,0].plot(mWave[0,0][:,0].toarray(), mWave[0,0][:,1].toarray(), 'k', linewidth='4')
    ax[0,0].set_xlim(0,max(mWave[2,0][:,0].toarray()))
    ax[1,0].plot(mWave[1,0][:,0].toarray(), mWave[1,0][:,1].toarray(), 'k', linewidth='4')
    ax[1,0].set_xlim(0,max(mWave[2,0][:,0].toarray()))
    ax[2,0].plot(mWave[2,0][:,0].toarray(), mWave[2,0][:,1].toarray(), 'k', linewidth='4')
    ax[2,0].set_xlim(0,max(mWave[2,0][:,0].toarray()))
    
    if binned:
        ax[0,0].bar(mWave[3,0][:,0].toarray().T[0], mWave[3,0][:,1].toarray().T[0], color=norm_col, width=0.5)
        ax[1,0].bar(mWave[4,0][:,0].toarray().T[0], mWave[4,0][:,1].toarray().T[0], color=norm_col, width=0.5)
        ax[2,0].bar(mWave[5,0][:,0].toarray().T[0], mWave[5,0][:,1].toarray().T[0], color=norm_col, width=0.5)
    else:
        _min = int(min(mWave[3,0][:,1].toarray()))
        _max = int(max(mWave[3,0][:,1].toarray()))
        data = np.zeros((int(_max - _min) + 1, 2))
        data[:,0] = np.array([x for x in range(_min, _max+1, 1)])
        for i in mWave[3,0][:,1].toarray():
            data[int(i) - _min, 1] = data[int(i) - _min, 1] + 1
        ax[0,0].bar(data[:,0], data[:,1], width=1, color=norm_col)
        
        _min = int(min(mWave[4,0][:,1].toarray()))
        _max = int(max(mWave[4,0][:,1].toarray()))
        data = np.zeros((int(_max - _min) + 1, 2))
        data[:,0] = np.array([x for x in range(_min, _max+1, 1)])
        for i in mWave[4,0][:,1].toarray():
            data[int(i) - _min, 1] = data[int(i) - _min, 1] + 1
        ax[1,0].bar(data[:,0], data[:,1], width=1, color=norm_col)
        
        _min = int(min(mWave[5,0][:,1].toarray()))
        _max = int(max(mWave[5,0][:,1].toarray()))
        data = np.zeros((int(_max - _min) + 1, 2))
        data[:,0] = np.array([x for x in range(_min, _max+1, 1)])
        for i in mWave[5,0][:,1].toarray():
            data[int(i) - _min, 1] = data[int(i) - _min, 1] + 1
        ax[2,0].bar(data[:,0], data[:,1], width=1, color=norm_col)
    
    an = np.array(list(map(lambda x: [sc.sparse.load_npz(x[0]), x[3]], an)))
    norm = np.array(list(map(lambda x: [sc.sparse.load_npz(x[0]), x[3]], norm)))
    
    if binned:
        pop = np.array(list(map(lambda x, y, z: [float(z), float(sum(x[:,1]).toarray()[0]), sum(y[:,1].toarray().T[0])], an[:,0], norm[:,0], an[:,1])))
        
        mean = np.array(list(map(lambda x, y, z: [float(z), \
            float(sum(x[:,0].multiply(x[:,1])).toarray()[0])/float(sum(x[:,1]).toarray()[0]), \
            float(sum(y[:,0].multiply(y[:,1])).toarray()[0])/float(sum(y[:,1]).toarray()[0])], an[:,0], norm[:,0], an[:,1])))
        
        an_war = np.array(list(map(lambda x, y: sum(x[:,1].toarray()*((x[:,0].toarray()-float(y))*(x[:,1].toarray() > 0))**2)/(sum(x[:,1].toarray())), \
                                  an[:,0] , mean[:,1])))
        norm_war = np.array(list(map(lambda x, y: sum(x[:,1].toarray()*((x[:,0].toarray()-float(y))*(x[:,1].toarray() > 0))**2)/(sum(x[:,1].toarray())), \
                                norm[:,0], mean[:,2])))
        war = np.array(list(map(lambda x, y, z: [float(x), float(y), float(z)], an[:,1], an_war, norm_war)))   

    else:
        pop = np.array(list(map(lambda x, y, z: [float(z), float(sum(x[:,1]).toarray()[0]), len(y[:,1].toarray())], an[:,0], norm[:,0], an[:,1])))
        
        mean = np.array(list(map(lambda x, y, z: [float(z), \
            float(sum(x[:,0].multiply(x[:,1])).toarray()[0])/float(sum(x[:,1]).toarray()[0]), \
            sum(y[:,1].toarray())[0]/len(y[:,1].toarray())], an[:,0], norm[:,0], an[:,1])))
        
        an_war = np.array(list(map(lambda x, y: sum(x[:,1].toarray()*((x[:,0].toarray()-float(y))*(x[:,1].toarray() > 0))**2)/(sum(x[:,1].toarray())), \
                                  an[:,0] , mean[:,1])))
        norm_war = np.array(list(map(lambda x, y: sum((x[:,1].toarray()-float(y))**2)/len(x[:,1].toarray()), \
                                norm[:,0], mean[:,2])))
        war = np.array(list(map(lambda x, y, z: [float(x), float(y), float(z)], an[:,1], an_war, norm_war)))   
    
    R2 = np.corrcoef(mean[:,1], mean[:,2])
    R2 = R2[0,1]
    R2 = R2**2
    
    if not var:    
        alfa_state.append(mean[ix1,1:3])
        alfa_state.append(mean[ix2,1:3])
        alfa_state.append(mean[ix3,1:3])
    else:
        alfa_var.append(mean[ix1,1:3])
        alfa_var.append(mean[ix2,1:3])
        alfa_var.append(mean[ix3,1:3])
    
    ax[0,1].plot(mean[:,0], mean[:,1], 'k', linewidth='4')
    ax[0,1].plot(mean[:,0], mean[:,2], norm_col, linewidth='2')
    ax[1,1].plot(war[:,0], war[:,1], 'k', linewidth='4')
    ax[1,1].plot(war[:,0], war[:,2], norm_col, linewidth='2')
    ax[2,1].plot(pop[:,0], pop[:,1], 'k', linewidth='4')
    ax[2,1].plot(pop[:,0], pop[:,2], norm_col, linewidth='2')
    
    for tx in ax: 
        for rx in tx:
            for tick in rx.xaxis.get_major_ticks():
                tick.label.set_fontsize(20) 
            for tick in rx.yaxis.get_major_ticks():
                tick.label.set_fontsize(20) 
    
    ax[0,0].set_title("mutation wave, N(t), t=%s" % an[ix1,1], fontdict={'fontsize':50})
    ax[1,0].set_title("mutation wave, N(t), t=%s" % an[ix2,1], fontdict={'fontsize':50})
    ax[2,0].set_title("mutation wave, N(t), t=%s" % an[ix3,1], fontdict={'fontsize':50})
    ax[2,0].set_xlabel("mutation number", fontdict={'fontsize':30})
    ax[0,1].set_title("mean number of mutations, $\chi(t)$, $R^{2}$=%.3f" % (R2), fontdict={'fontsize':50})
    ax[1,1].set_title("variance number of mutations, $\sigma^{2}(t)$", fontdict={'fontsize':50})
    ax[2,1].set_title("population size, N(t)", fontdict={'fontsize':50})
    ax[2,1].set_xlabel("time, t", fontdict={'fontsize':30})

    if not out == "":
        _out_norm = out

    try:
        os.makedirs(_out_an, exist_ok=True) 
        os.makedirs(_out_norm, exist_ok=True) 
    except OSError as error:
        print(error)
    finally:
        if os.path.exists(_out_an + "evolution_dynamics_" + name_an + ".jpg"):
            os.remove(_out_an + "evolution_dynamics_" + name_an + ".jpg")
        if os.path.exists(_out_norm + "evolution_dynamics_" + name_norm + ".jpg"):
            os.remove(_out_norm + "evolution_dynamics_" + name_norm + ".jpg")
        fig.savefig(_out_an + "evolution_dynamics_" + name_an + ".jpg")
        fig.savefig(_out_norm + "evolution_dynamics_" + name_norm + ".jpg")
        if os.path.exists(_out_an + "evolution_dynamics_" + name_an + ".eps"):
            os.remove(_out_an + "evolution_dynamics_" + name_an + ".eps")
        if os.path.exists(_out_norm + "evolution_dynamics_" + name_norm + ".eps"):
            os.remove(_out_norm + "evolution_dynamics_" + name_norm + ".eps")
        fig.savefig(_out_an + "evolution_dynamics_" + name_an + ".eps", format='eps')
        fig.savefig(_out_norm + "evolution_dynamics_" + name_norm + ".eps", format='eps')
        plt.close(fig)  
    
if __name__ == '__main__':
    path_b = "E:/Simulations/t_b"
    path = np.array(os.listdir(path_b))
    path = np.array(list(map(lambda x,y: (y + '/' + x)*x.endswith('.npz'), path, np.repeat(path_b, len(path)))))
                    
    path_a = "E:/Simulations/S_0.0025_A"
    path_an = np.array(os.listdir(path_a))
    path_an = np.array(list(map(lambda x,y: (y + '/' + x)*x.endswith('.npz'), path_an, np.repeat(path_a, len(path_an)))))
                 
    evolutionDynamics(path_an[path_an!=''], path[path!=''], binned=True)
    # name_an = "E:/Simulations/Alfa test/Analytical/"
    # a = os.listdir(name_an)
    # norm_name = "E:/Simulations/Alfa test/Normal/"
    # b = os.listdir(norm_name)
    # xx = 0
    # for i in a:
    #     var = 0
    #     fname = name_an + '/' + i
    #     name = ""
    #     fname_an = np.array(os.listdir(fname))
    #     fname_an = np.array(list(map(lambda x,y: (y + '/' + x)*x.endswith('.npz'), fname_an, np.repeat(fname, len(fname_an)))))
    #     fname_an = fname_an[fname_an != '']
    #     if 'var' in i:
    #         out = "E:/Simulations/Alfa test/Alfa var figures/"
    #         name = i.rstrip('_var')
    #         var = 1
    #     else:
    #         out = "E:/Simulations/Alfa test/Alfa state figures/"
    #         name = i
    #     for j in b:
    #         if name in j:
    #             fname = norm_name + '/' + j
    #             fname_norm = np.array(os.listdir(fname))
    #             fname_norm = np.array(list(map(lambda x,y: (y + '/' + x)*x.endswith('.npz'), fname_norm, np.repeat(fname, len(fname_norm)))))
    #             fname_norm = fname_norm[fname_norm != '']
    #             xx = xx + 1
    #             print(xx)
    #             evolutionDynamics(fname_an, fname_norm, out, var)
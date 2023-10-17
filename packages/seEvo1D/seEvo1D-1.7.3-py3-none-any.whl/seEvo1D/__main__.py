from seEvo1D.mainView import run
from seEvo1D.seEvo_evolution_init import seEvoInit
# from seEvo_evolution_init import seEvoInit
import numpy as np
import scipy as sc
import pandas as pd
import copy
from pathlib import Path
from multiprocessing import Process, Queue
import sys

def main():
    run()
    
def console(omit, range_p, range_s, range_n):
    if ('-h' in sys.argv) or ('--help' in sys.argv):
        print('COMMANDS')
        print('---------------------------------------------------')
        print('COMMANDS WITH OBLIGATORY ARGUMENT')
        print('-N \t cells number')
        print('-C \t cells capacity')
        print('-P \t mutation probability')
        print('-S \t mutation effect')
        print('-A \t death exponent')
        print('-tau \t tau step')
        print('-skip \t skip size (save generation)')
        print('-steps \t max steps')
        print('-path \t save file (add path)')
        print('---------------------------------------------------')
        print('COMMANDS WITHOUT ARGUMENT')        
        print('--save \t save to file (parametr path is obligatory)')
        print('--save_params \t save params to file (parametr path is obligatory')
        print('--normal | --analytical | --binned \t choose method (default normal)')
        print('---------------------------------------------------')
    else:
        try:
            N = sys.argv[sys.argv.index('-N') + 1]
        except:
            N = 10000
            
        try:    
            C = sys.argv[sys.argv.index('-C') + 1]
        except:
            C = 10000
            
        try: 
            P = sys.argv[sys.argv.index('-P') + 1]
        except:
            P = 0.005
            
        try: 
            S = sys.argv[sys.argv.index('-S') + 1]
        except:
            S = -0.0025
            
        try: 
            A = sys.argv[sys.argv.index('-A') + 1]
        except:
            A = 1
            
        try: 
            tau = sys.argv[sys.argv.index('-tau') + 1]
        except:
            tau = 0.005
            
        try: 
            skip = sys.argv[sys.argv.index('-skip') + 1]
        except:
            skip = 50
            
        try: 
            steps = sys.argv[sys.argv.index('-steps') + 1]
        except:
            steps = 7500
            
        try: 
            path = sys.argv[sys.argv.index('-path') + 1]
        except:
            path = ""
        
        print(path)
        save = '--save' in sys.argv
        save_p = '--save_params' in sys.argv
        method = 1 * ('--analytical' in sys.argv) + 2 * ('--binned' in sys.argv)
        if not omit:            
            params = [int(N), int(C), int(steps), float(tau), int(skip), float(P), float(S), float(A)]
            if save_p:
                dfp = pd.DataFrame(params)
                
                filepath = Path(path + '/params'  + ".csv")  
                filepath.parent.mkdir(parents=True, exist_ok=True)  
                dfp.to_csv(filepath)
            
            select = 0
            name = ""
            if method == 1:
                iPop = np.array([[0],[float(N)]])
                select = 1
                name = 'analytical'
            elif method == 2:
                iPop = np.array([[0],[int(N)]])
                select = 2
                name = 'binned'
            else:
                iPop = np.ones(int(N))
                iMuts = np.zeros(int(N))
                iPop = sc.sparse.csr_matrix(np.array([iPop, iMuts]).T)
                select = 0
                name = 'normal'
            
            plots = 16*save
        
            th = Process(target=seEvoInit, args=(copy.deepcopy(iPop), 
                                                        copy.deepcopy(params), 
                                                        'console_' + name, 
                                                        path,
                                                        plots, None, 1, select, 0))
            th.start()
            th.join()
        else:
            idx_n = 1
            for i in range_n:
                idx_p = 1
                for j in range_p:
                    th = []
                    idx_s = 1
                    for k in range_s:
                        params = [i, i, int(steps), float(tau), int(skip), j, -k, float(A)]
                        print(params)
                        if save_p:
                            dfp = pd.DataFrame(params)
                            
                            filepath = Path(path + '/N_' + str(i) + '/P_' + str(j) + '/S_' + str(k) + '/params'  + ".csv")  
                            filepath.parent.mkdir(parents=True, exist_ok=True)  
                            dfp.to_csv(filepath)
                        
                        select = 0
                        name = ""
                        if method == 1:
                            iPop = np.array([[0],[float(N)]])
                            select = 1
                            name = 'analytical'
                        elif method == 2:
                            iPop = np.array([[0],[int(N)]])
                            select = 2
                            name = 'binned'
                        else:
                            iPop = np.ones(int(N))
                            iMuts = np.zeros(int(N))
                            iPop = sc.sparse.csr_matrix(np.array([iPop, iMuts]).T)
                            select = 0
                            name = 'normal'
                        
                        plots = 16*save
                        
                        th.append(Process(target=seEvoInit, args=(copy.deepcopy(iPop), 
                                                                    copy.deepcopy(params), 
                                                                    'console_' + name, 
                                                                    path + '/N_' + str(i) + '/P_' + str(j) + '/S_' + str(k),
                                                                    plots, None, idx_s, select, 0)))
                        th[idx_s-1].start()
                        idx_s = idx_s + 1
                    
                    for w in th:
                        w.join()
                    del th
                    print("p: %.3f DONE" % j)
                    idx_p = idx_p + 1
                idx_n = idx_n + 1

def omit_map(r):
    r = r.split(',')
    r = [float(x) for x in r]
    return np.array(r)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        omit = '--superuser' in sys.argv
        r_p = 0
        r_s = 0
        r_n = 0
        if omit:
            r_p = sys.argv[sys.argv.index('-r_p') + 1]
            r_s = sys.argv[sys.argv.index('-r_s') + 1]
            r_n = sys.argv[sys.argv.index('-r_n') + 1]
            r_p = omit_map(r_p)
            r_s = omit_map(r_s)
            r_n = omit_map(r_n)
            last = r_p[1]
            r_p = np.arange(r_p[0], r_p[1], r_p[2])
            r_p[1::] = r_p[1::] - r_p[0]
            r_p = np.append(r_p, last)
            r_p = np.round(r_p, 3)
            last = r_s[1]
            r_s = np.arange(r_s[0], r_s[1], r_s[2])
            r_s[1::] = r_s[1::] - r_s[0]
            r_s = np.append(r_s, last)
            r_s = np.round(r_s, 4)
            last = r_n[1]
            r_n = 10**np.arange(r_n[0], r_n[1], r_n[2])
            r_n = np.append(r_n, 10**last)
            print(r_p)
            print(r_s)
            print(r_n)
        console(omit, r_p, r_s, r_n)
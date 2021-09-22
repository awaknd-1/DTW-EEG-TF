

import numpy as np
import scipy as sp
from sklearn import preprocessing
from scipy import signal 
import glob
from sklearn.preprocessing import StandardScaler
import scipy.io as sio
from scipy.spatial import distance
from scipy import stats
import os.path

#=================================================================================================================
# Distance measure für DTW, inner product distance ist gebraucht hier.
#=================================================================================================================

def vector_difference(tv,rv):
    result = distance.correlation(tv,rv)
    

    return result

#=================================================================================================================
# Hier beginnt der dynamic Programmierung
#=================================================================================================================
    
def func(t,r,trell,step,path,diff):
    global cnt
    global path_var
    global min_var
                    
    t1=1000000000
    t2=1000000000
    t3=1000000000
    
    
    if (r>0):
        t1 = trell[t][r-1]+diff[t][r] # slop constrant has been added to the algorithm in terms of +1's
        
    if (t>0) and (r>0):
        t2 = trell[t-1][r-1]+2*diff[t][r]
        
    if (t>0):
        t3 = trell[t-1][r]+diff[t][r]
        
        
    if ((t1<t2) and (t1<t3)):
        min_var = t1
        path_var = 1
        if (r-1>-1) :
            
            cnt = step[t][r-1]
    
    elif (t2<t3):
        min_var = t2
        path_var = 2
        if ((t>0) and (r>0)):
                cnt = step[t-1][r-1]+1
    else:
        min_var = t3
        path_var = 3
        if(t>0):
            cnt = step[t-1][r]
            
    return (path_var,cnt,min_var)
        
#===================================================================================================================
# Das ist the DTW code
#===================================================================================================================
# input size: times x frequncy (2D matrix)
def DTW(train,test):
    a, b = train.shape
    path = (np.zeros([a,b])).tolist()
    step = (np.zeros([a,b])).tolist()
    trell = (np.zeros([a,b])).tolist()
    diffmat = (np.zeros([a,b])).tolist()        
    lp = np.arange(a)
    
    
    for t in lp:
        tv = test[:,t]
        for r in lp:                
            rv = train[:,r]       
            diffmat[t][r] = (vector_difference(tv,rv))
    
    
    
    trell[0][0] = diffmat[0][0]
     

    for t in range(0,a):     
         for r in range(0,b):
            if ((t>0) or (r>0)):
                path_var,cnt,min_var = func(t,r,trell,step,path,diffmat)
                path[t][r] = path_var
                step[t][r] = (cnt+1)
                trell[t][r] = min_var
                 
    
    return (np.asarray(trell),np.asarray(step),np.asarray(path),min_var,tv,rv)

#==================================================================================================================
# Diese ist der wrap path
#==================================================================================================================
    
def wrap_path(paths, train) :  
    a, b = train.shape
    indx = []
    qmap = (np.zeros([a,b])).tolist()
    i = a-1
    j = b-1
    while (i>=0 and j>=0):
        
        if paths[i,j] ==1:
            j = j-1
            i = i
        elif paths[i,j] == 2:
            i = i-1
            j = j-1
        elif paths[i,j] == 3:
            i = i-1
            j = j
        else:
            break
        indx.append(paths[i,j])
        qmap[i][j] = paths[i,j]
        
    indx1 = indx[::-1]
    indx1.pop(1)
    indx1 = np.asarray(indx1)
    return (indx1,np.asarray(qmap))


 





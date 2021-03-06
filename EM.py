import csv
from sklearn import tree
from sklearn import preprocessing
import numpy as np
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier
from math import ceil
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D


fn = "AP_Analytics.csv"
writeFn = fn[:-4] + "_EM_output.csv"
print(writeFn)

covs = ['full','tied','diag','spherical']
n_inits = [5,10,15,20]
max_iters = [100,200,300,500]
norms = [True,False]
#fig = plot.figure(1)
#ax = Axes3D(fig)

def runEverything():
    data,x,y,normx,normy = preProcessData(fn)
    results = []
    for cov in covs:
        for n_init in n_inits:
            for max_iter in max_iters:
                for norm in norms:
                    err,log = classify(x,y,normx,normy,cov,n_init,max_iter,norm)
                    print(cov,n_init,max_iter,norm,":",err,log)
                    results.append([cov,n_init,max_iter,norm,err,log])
                    
    file = open(writeFn,"w",newline="")
    csvW = csv.writer(file)
    csvW.writerow(["Cov","n_init","max_iter","norm","error","log-lklhd"])
    csvW.writerows(results)
    print("Open your file")
    #fig.show()

    fig2 = plot.figure(2)
    ax2 = Axes3D(fig2)
    labels = np.array(y)
    X = np.array(x)
    ax2.scatter(X[:,0],X[:,1],X[:,3],c=labels.astype(np.float),edgecolor='k')
    fig2.show()
                    

def norm(vec):
    dist = max(vec) - min(vec)
    new = []
    for item in vec:
        if dist != 0:
            new.append(item/dist)
        else:
            new.append(0)
    return new

def preProcessData(fn):
    data = []
    f = open(fn)

    csvReader = csv.reader(f,delimiter=",")
    for row in csvReader:
        data.append(row)

    data = data[1:]
    i = 0
    for col0 in data[0]:
        try:
            float(col0)
            for row in data:
                row[i] = float(row[i])
        except:
            col = []
            for row in data:
                col.append(row[i])
            le = preprocessing.LabelEncoder()
            le.fit(col)
            a = le.transform(col)
            newCol = np.array(a).tolist()
            #print(newCol)

            for row in data:
                #print(i)
                row[i] = newCol[i]
        i = i + 1
    
    x = []
    y = []
    for row in data:
        x.append(row[:-1])
        y.append(row[-1])

    #print(x[5:10])

    ## normalize every vector ###
    arrx = np.array(x)
    for i in range(len(x[0])):
        arrx[:,i] = np.array(norm(np.ndarray.tolist(arrx[:,i])))
    normx = np.ndarray.tolist(arrx)
    normy = norm(y)
    return (data,x,y,normx,normy)

def classify(x,y,normx,normy,cov,n_init,max_iter,norm):
    if norm:
        x = normx
        y = normy
        
    fitter = GaussianMixture(n_components=2,covariance_type=cov,n_init=n_init,max_iter=max_iter).fit(x)
    print(fitter.means_)
    #X = np.array(x)
    #labels = fitter.labels_
    #ax.scatter(X[:,0],X[:,1],X[:,2],c=labels.astype(np.float),edgecolor='k')
    return (min(sum(abs(fitter.predict(x)-y)),sum(abs((1 - fitter.predict(x)) - y)))/len(x),fitter.lower_bound_)

runEverything()













    

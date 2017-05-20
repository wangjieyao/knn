import numpy as np
import knn
import time


## Data (were modified) downloaded from here:
## https://archive.ics.uci.edu/ml/datasets/Qualitative_Bankruptcy

## last column is classification, others are attributes
data = np.genfromtxt('Qualitative_Bankruptcy.txt', delimiter=',',dtype='f')

## classification
dataCl = data[:,-1]

## attributes
data = data[:, :-1]

procList = ['CPU','GPU']
rateDict = dict.fromkeys(procList)

nPoints = len(data)

knn = knn.knn()

pretxt = str(nPoints)+" training data examples with "+str(len(data[0]))+" features"
print len(pretxt)*'*'
print len(pretxt)*'*'
print "Bankruptcy prediction"
print pretxt

for proc in procList:
    errorRate = 0
    knn.procList = [proc]
    start_time = time.time()

    print '********** Result of using '+proc+' **********'

    for point in range(1,nPoints-1):

        dataPoint = data[point]

        knn.data = np.append(data[:][0:point],data[:][point+1:nPoints],axis=0)
        knn.dataCl = np.append(dataCl[:][0:point],dataCl[:][point+1:nPoints],axis=0)
        knn.testPt = dataPoint 
    
        result = knn.getPred()
        
        errorRate+=float(result==dataCl[point])

    timeToRun = time.time() - start_time 
    rateDict[proc] = timeToRun   
    timeUnit = ' seconds'
    if timeToRun>60:
        timeToRun*=1/60.
        timeUnit = ' minutes'
    if timeToRun>60:
        timeToRun*=1/60.
        timeUnit = ' hours'
        if timeToRun>24:
            timeToRun*=1/24.
            timeUnit = ' days'
    timeToRun = round(timeToRun,3)

    print '--- '+str(timeToRun) +timeUnit+' to run  ---'
    errorRate = errorRate/(nPoints-2)
    print '--- '+ str( round(errorRate*100,3)) + ' percent correctly predicted ---' 

if ( 'GPU' in procList and 'CPU' in procList):
    perfIncrease = round(rateDict['CPU']/rateDict['GPU'],1)
    st = '****** GPU processing was '+str(perfIncrease)+' times faster ******'

    print len(st)*'*'
    print st
    print len(st)*'*'

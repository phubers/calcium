'''
Created on 6 mei 2014

@author: Patrick.Hubers
'''
from math import pow, factorial, exp, ceil, trunc

def PowerFactorial(valueA, valueB):
    fct = factorial(valueA)
    #print "Factorial %d is %d" % (valueA, fct)
    pw = pow(valueB, valueA)
    #print "%d to the power %d is %d" % (valueB, valueA, pw)
    answer = pw / fct
    return( answer )

def Workload(volume, avgHandleTime, intervalLength=60):
    return( (volume*avgHandleTime)/(60.0*intervalLength) )

def Occupancy(numAgents, workload):
    return( workload/numAgents )

def ErlangC(numAgents, workload):
    term = PowerFactorial(numAgents, workload)
    totalsum = 0
    for k in range (0,numAgents):
        totalsum += PowerFactorial(k, workload)
    erlangc = term / (term+(1-Occupancy(numAgents,workload))*totalsum)
    return( erlangc )

def AverageWaitingTime(numAgents, volume, avgHandleTime, intervalLength):
    workload = Workload(volume, avgHandleTime, intervalLength)
    return( (ErlangC(numAgents,workload)*avgHandleTime)/(numAgents-workload) )

def ServiceLevel(numAgents, volume, avgHandleTime, intervalLength, maxWaitingTime):
    workload = Workload(volume, avgHandleTime, intervalLength)
    return( 1-ErlangC(numAgents,workload)* exp(-(numAgents-workload)*(maxWaitingTime/avgHandleTime)) )

def AgentsForServiceLevel(volume, avgHandleTime, intervalLength, maxWaitingTime, serviceGoal):
    workload = Workload(volume, avgHandleTime, intervalLength)
    agents = trunc(ceil(workload))
    print "Starting with %d agents" % agents
    while( ServiceLevel(agents, volume, avgHandleTime, intervalLength, maxWaitingTime) < serviceGoal ):
        agents += 1
    return( agents )
    
if __name__ == '__main__':
    calls = 620
    aht = 415
    wload = Workload(calls, aht)
    svgoal = 0.8
    waittime = 20
    print "Workload for %d calls with %d seconds of AHT is %f" % (calls, aht, wload)
    agents = AgentsForServiceLevel(calls, aht, 60, waittime, svgoal)
    print "%d Agents are needed to achieve a %d/%d service level" % (agents, svgoal*100, waittime)
    sl = ServiceLevel(agents, calls, aht, 60, waittime)
    print "In that case, you'll get a service level of %f%%" % (sl*100)
    print "Your occupancy will be %f%%" % (wload/agents*100)
    

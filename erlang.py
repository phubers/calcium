'''
Created on 6 mei 2014

Erlang functions for use in calculators

@author: Patrick.Hubers
'''
from math import pow, factorial, exp, ceil, trunc

def Poisson(actual, mean):
    # naive:   math.exp(-mean) * mean**actual / factorial(actual)
    # iterative, to keep the components from getting too large or small:
    p = exp(-mean)
    for i in xrange(actual):
        p *= mean
        p /= i+1
    return p

def Workload(volume, avgHandleTime, intervalLength=60):
    return( (volume*avgHandleTime)/(60.0*intervalLength) )

def Occupancy(numAgents, workload):
    return( workload/(numAgents*1.0) )

def ErlangC(numAgents, workload):
    pois_discrete = Poisson(numAgents, workload)
    pois_cum = 0.0
    for k in range (0, numAgents):
        pois_cum += Poisson(k, workload)
    erlangc = pois_discrete / (pois_discrete + (( 1.0 - Occupancy(numAgents,workload)) * pois_cum))
    return( erlangc )

def AverageWaitingTime(numAgents, volume, avgHandleTime, intervalLength):
    workload = Workload(volume, avgHandleTime, intervalLength)
    return( (ErlangC(numAgents,workload)*avgHandleTime)/(numAgents-workload) )

def ServiceLevel(numAgents, volume, avgHandleTime, intervalLength, maxWaitingTime):
    workload = Workload(volume, avgHandleTime, intervalLength)
    return( 1-ErlangC(numAgents,workload)* exp(-(numAgents-workload)*((maxWaitingTime*1.0)/avgHandleTime)) )

def AgentsForServiceLevel(volume, avgHandleTime, intervalLength, maxWaitingTime, serviceGoal):
    workload = Workload(volume, avgHandleTime, intervalLength)
    agents = trunc(ceil(workload))
    while( ServiceLevel(agents, volume, avgHandleTime, intervalLength, maxWaitingTime) < serviceGoal ):
        agents += 1
    return( agents )

if __name__ == '__main__':
    vol = 400
    aht = 180
    wl = Workload(vol, aht, 60)
    print 'Workload for %d calls/hour with an AHT of %d seconds is %d' % (vol, aht, wl)
    sgoal = 0.8
    stime = 20
    agents = AgentsForServiceLevel(vol, aht, 60, stime, sgoal)
    print 'Required agents for a service level of %d/%d is %d' % (sgoal*100, stime, agents)
    print 'Waiting chance for a caller is %f ' % ErlangC(agents, wl)
    print 'Service level is %f ' % ServiceLevel(agents, vol, aht, 60, stime)
    print 'Occupancy is %f' % Occupancy(agents, wl)
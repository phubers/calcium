'''
Created on 6 mei 2014

Erlang functions for use in calculators

@author: Patrick.Hubers
'''
from math import exp, ceil, trunc

def Workload(volume, avgHandleTime, intervalLength=60):
    return( (volume*avgHandleTime)/(60.0*intervalLength) )

def Occupancy(numAgents, workload):
    return( workload/(numAgents*1.0) )

def ErlangB(numAgents, workload):
    inverse_b = 1.0
    for k in range(1, numAgents):
        inverse_b = 1.0 + inverse_b * k / workload
    return(1.0 / inverse_b)
    
def ErlangC(numAgents, workload):
    erlangc = numAgents * ErlangB(numAgents, workload) / (numAgents - workload * (1 - ErlangB(numAgents, workload)))
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
    print('Workload for %d calls/hour with an AHT of %d seconds is %d' % (vol, aht, wl))
    sgoal = 0.8
    stime = 20
    agents = AgentsForServiceLevel(vol, aht, 60, stime, sgoal)
    print('Required agents for a service level of %d/%d is %d' % (sgoal*100, stime, agents))
    print('Waiting chance for a caller is %f ' % ErlangC(agents, wl))
    print('Service level is %f ' % ServiceLevel(agents, vol, aht, 60, stime))
    print('Occupancy is %f' % Occupancy(agents, wl))


import time
import random
import math
def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3]*60 + x[4]

people = [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]

destination = 'LGA'

flights = {}

for line in file('schedule.txt'):
    origin,dest,depart,arrive,price = line.strip().split(',')
    flights.setdefault((origin,dest),[])

    flights[(origin,dest)].append((depart,arrive,int(price)))

def printschedule(r):
    for d in range(len(r)/2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin,destination)][r[d]]
        ret = flights[(destination,origin)][r[d+1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,out[0],out[1],out[2],ret[0],ret[1],ret[2])

def schedulecost(solution):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24*60

    for d in range(len(solution)/2):
        origin = people[d][1]
        outbound = flights[(origin,destination)][int(solution[d])]
        returnf = flights[(destination,origin)][int(solution[d+1])]

        totalprice+=outbound[2]
        totalprice+=returnf[2]

        if (latestarrival<getminutes(outbound[1])): latestarrival=getminutes(outbound[1])
        if (earliestdep>getminutes(returnf[0])): earliestdep=getminutes(returnf[0])

    totalwait = 0
    for d in range(len(solution)/2):
        origin = people[d][1]
        outbound = flights[(origin,destination)][int(solution[d])]
        returnf = flights[(destination,origin)][int(solution[d+1])]
        totalwait+=latestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep

    if (latestarrival>earliestdep): totalprice+=50
    return totalprice+totalwait

def randomoptimize(domain,costf):
    best = 999999999
    bestr = None
    for i in range(1000):
        #Create random solution
        r = [random.randint(domain[j][0],domain[j][1]) for j in range(len(domain))]
        cost = costf(r)
        if (cost < best) :
            best = cost
            bestr = r
    return bestr

def hillclimb(domain,costf):
    solution = [random.randint(domain[j][0],domain[j][1]) for j in range(len(domain))]

    while 1:
        neighbors = []
        for j in range(len(domain)):

            if (solution[j]>domain[j][0]):
                neighbors.append(solution[0:j] + [solution[j]+1] + solution[j+1:])
            if (solution[j]<domain[j][1]):
                neighbors.append(solution[0:j] + [solution[j]-1] + solution[j+1:])

        current = costf(solution)
        best = current
        for j in range(len(neighbors)):
            cost = costf(neighbors[j])
            if (cost < best):
                best = cost
                solution = neighbors[j]

        if best == current: break

    return solution

def simulated_annealing(domain,costf,T=10000.0,cool=0.95,step=1):
    # Initialize the values randomly
    vec = [random.randint(domain[j][0],domain[j][1]) for j in range(len(domain))]
    while T>0.1:
        #random indices
        i = random.randint(0,len(domain)-1)
        #choose a direction to change it
        dir = random.randint(-step,step)
        #create new list
        newvec = vec[:]
        newvec[i]+=dir
        if (newvec[i] < domain[i][0]): newvec[i] = domain[i][0]
        elif (newvec[i] > domain[i][1]): newvec[i] = domain[i][1]

        e = costf(vec)
        enew = costf(newvec)
        p = pow(math.e,(-enew-e)/T) #probability

        # is it a better or does it make the probability
        if ((enew < e) or (random.random() < p)):
            vec = newvec

        # decrease the temperature
        T = T*cool

    return vec

def genetic_algorithms(domain,costf,popsize=50,step=1,mutprob=0.15,elite=0.2,maxiter=100):
    #mutate operation
    def mutate(vec):
        i = random.randint(0,len(domain)-1)
        if ((random.random()<0.5) and vec[i] > domain[i][0]):
            return (vec[0:i] + [vec[i]+step] + vec[i+1:])
        elif vec[i] <= domain[i][1]:
            return (vec[0:i] + [vec[i]-step] + vec[i+1:])
    #crossover operation
    def crossover(r1,r2):
        i = random.randint(0, len(domain) - 2)
        return r1[0:i]+r2[i:]
    #build the initialize population
    pop = []
    for i in range(popsize):
        vec = [random.randint(domain[j][0],domain[j][1]) for j in range(len(domain))]
        pop.append(vec)

    #how many winner for each gen
    topelite = int(elite*popsize)

    #main loop
    for i in range(maxiter):
        #top winner
        scores = [(costf(v),v) for v in pop]
        scores.sort()
        ranked = [v for (i,v) in scores]
        pop = ranked[0:topelite]

        while(len(pop)<popsize):
            if (random.random()<mutprob):
                c = random.randint(0,topelite)
                pop.append(mutate(ranked[c]))

            else:
                c1 = random.randint(0,topelite)
                c2 = random.randint(0,topelite)
                pop.append(crossover(ranked[c1],ranked[c2]))


        #print scores[0][0]

    return scores[0][1]


#domain = [(0,8)]*(len(people)*2)
#r = genetic_algorithms(domain,schedulecost)
#print schedulecost(r)
#print r
#printschedule(r)
import socialnetwork
sol = randomoptimize(socialnetwork.domain,socialnetwork.crosscount)
print sol
print socialnetwork.crosscount(sol)
sol = simulated_annealing(socialnetwork.domain,socialnetwork.crosscount,step=50,cool=0.99)
print socialnetwork.crosscount(sol)
print sol
socialnetwork.drawnetwork(sol)
sol = [324, 190, 241, 329, 298, 237, 117, 181, 88, 106, 56, 10, 296, 370, 11, 312]
print socialnetwork.crosscount(sol)
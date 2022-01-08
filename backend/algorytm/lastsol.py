import numpy as np
import copy
def secalgo(initialsolution, init_val, kadencja, cl_serv,maxint, cost ):

    cl_serv_k = list(cl_serv.keys())
    depot = list(cl_serv.keys())[0]
    solution_clientes={}
    best_found = 0
    init_move_val =0 

    for liczba in range (maxint):
        tabulist=[]
        for i in range(len(initialsolution)):
            for j in range(len(initialsolution[i])):
                solution_clientes[initialsolution[i][j]]=(i,j)
        del solution_clientes["K0"]

        cl_serv_knd = cl_serv_k[1:]
        sumd = sum([cl_serv[k]["demand"] for k in cl_serv])
        prob_cust= [cl_serv[k]["demand"]/sumd  for k in cl_serv]
        prob_nar = np.zeros((len(prob_cust)))
        for ind  in range(1,len(prob_nar)):
            prob_nar[ind]=prob_nar[ind-1] + prob_cust[ind]

        los = np.random.random()
        klient=""

        for ind, val in enumerate(prob_nar):
            if los >= val :
                klient= cl_serv_knd[ind]

        qty_trucks= len(initialsolution)

        neighbours=[]
        neigbours_val =[]

        neig=copy.deepcopy(solution_clientes)
        clnd = cl_serv_k[1:]
        cl_items=[]
        for item in clnd:
            if item != klient and [klient,item] not in tabulist:
                a = neig[item]
                b = neig[klient]
                neig[klient]= a 
                neig[item] = b
                neighbours.append(neig)
                cl_items.append(item)


        val = copy.deepcopy(neighbours)
        for iter in val:
            val_sort = {k: v for k, v in sorted(iter.items(), key=lambda item: item[1])}


        iletru = max([j[0] for j  in [ i[1] for i in list(val_sort.items())]])

        neig_cost=[]
        for i_n in range(0,len(neighbours)):
            trucks=[]
            for i in range(0,iletru+1):
                truck =[depot]
                for item in val_sort:
                    if val_sort[item][0]== i :
                        truck.append(item)
                truck.append(depot)
                trucks.append(truck)

            cost_solution=0
            for t in trucks:
                for i in range(1,len(t)):
                    cost_solution+=cost[(t[i-1],t[i])]
            neig_cost.append(cost_solution)


        best_now = (trucks[neig_cost.index(min(neig_cost))][1:-1])

        if min(neig_cost) < init_val:
            tabulist.append([klient,cl_items[neig_cost.index(min(neig_cost))]])
            initialsolution = best_now
            init_val = min(neig_cost)
            if len(tabulist)  > kadencja:
                del tabulist[0]

    solution_clientes2={}
    for i in range(len(initialsolution)):
        for j in range(len(initialsolution[i])):
            solution_clientes2[initialsolution[i][j]]=(i,j)

    del solution_clientes2[depot]
    return solution_clientes2,init_val
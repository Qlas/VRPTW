import copy

import numpy as np


def secalgo(initialsolution, init_val, kadencja, cl_serv, maxint, cost, odl, max_capacity):

    if len(cl_serv) == 2:
        return initialsolution, init_val

    cl_serv_k = list(cl_serv.keys())
    depot = list(cl_serv.keys())[0]
    solution_clientes = {}
    best_found = 0
    init_move_val = 0

    for liczba in range(maxint):

        tabulist = []
        for i in range(0, len(initialsolution)):
            for j in range(0, len(initialsolution[i])):
                solution_clientes[initialsolution[i][j]] = (i, j)

        try:
            del solution_clientes[depot]
        except:
            pass
        cl_serv_knd = cl_serv_k[1:]

        sumd = sum([cl_serv[k]["demand"] for k in cl_serv])
        prob_cust = [cl_serv[k]["demand"] / sumd for k in cl_serv]
        prob_nar = np.zeros((len(prob_cust)))
        for ind in range(1, len(prob_nar)):
            prob_nar[ind] = prob_nar[ind - 1] + prob_cust[ind]

        los = np.random.random()
        klient = ""

        for ind, val in enumerate(prob_nar):
            if los >= val:
                klient = cl_serv_knd[ind]
        if len(cl_serv_knd) == 1:
            klient = cl_serv_knd[0]
        qty_trucks = len(initialsolution)

        neighbours = []
        neigbours_val = []

        neig = copy.deepcopy(solution_clientes)

        clnd = cl_serv_k[1:]

        cl_items = []
        for item in clnd:
            if item != klient and [klient, item] not in tabulist:  # spradzić okna czaswe i max pojemność
                a = neig[item]
                b = neig[klient]
                neig[klient] = a
                neig[item] = b

                negsort = {k: v for k, v in sorted(neig.items(), key=lambda item: item[1])}

                iletru = max([jj[0] for jj in [ii[1] for ii in list(negsort.items())]])

                trucks = []
                for i in range(0, iletru + 1):
                    truck = [depot]
                    for item in negsort:
                        if negsort[item][0] == i:
                            truck.append(item)
                    truck.append(depot)
                    trucks.append(truck)

                stime = 0
                sdemand = 0
                for t in trucks:
                    for i in range(1, len(t)):
                        if (
                            stime + odl[(t[i - 1], t[i])] >= cl_serv[t[i]]["start"]
                            and stime + odl[(t[i - 1], t[i])] <= cl_serv[t[i]]["end"]
                            and sdemand + cl_serv[t[i]]["demand"] <= max_capacity
                        ):
                            stime += odl[(t[i - 1], t[i])]
                            sdemand += cl_serv[t[i]]["demand"]
                        elif (
                            stime + odl[(t[i - 1], t[i])] <= cl_serv[t[i]]["start"]
                            and sdemand + cl_serv[t[i]]["demand"] <= max_capacity
                        ):
                            stime = odl[(t[i - 1], t[i])]
                            sdemand += cl_serv[t[i]]["demand"]
                        else:
                            neig[klient] = b
                            neig[item] = a
                            break

                neighbours.append(neig)
                cl_items.append(item)

        val = copy.deepcopy(neighbours)
        if len(clnd) == 1:
            val = clnd
            val_sort = clnd

        else:
            for iter in val:
                val_sort = {k: v for k, v in sorted(iter.items(), key=lambda item: item[1])}

                iletru = max([jj[0] for jj in [ii[1] for ii in list(val_sort.items())]])

        neig_cost = []

        for i_n in range(0, len(neighbours)):
            trucks = []
            for i in range(0, iletru + 1):
                truck = [depot]
                for item in val_sort:
                    if val_sort[item][0] == i:
                        truck.append(item)
                truck.append(depot)
                trucks.append(truck)

            cost_solution = 0
            for t in trucks:
                for i in range(1, len(t)):
                    cost_solution += cost[(t[i - 1], t[i])]
            neig_cost.append(cost_solution)

            # best_now = (trucks[neig_cost.index(min(neig_cost))][1:-1])

            if sum(neig_cost) < init_val:
                tabulist.append([klient, cl_items[neig_cost.index(min(neig_cost))]])
                if len(trucks) > 1:
                    initialsolution = trucks
                else:
                    initialsolution = trucks
                init_val = min(neig_cost)

                if len(tabulist) > kadencja:
                    del tabulist[0]

    solution_clientes2 = {}
    for i in range(0, len(initialsolution)):
        for j in range(0, len(initialsolution[i])):
            solution_clientes2[initialsolution[i][j]] = (i, j)
    try:
        del solution_clientes2[depot]
    except:
        pass

    solsort = {k: v for k, v in sorted(solution_clientes2.items(), key=lambda item: item[1])}
    iletru = max([jj[0] for jj in [ii[1] for ii in list(solsort.items())]])

    trucks = []
    for i in range(0, iletru + 1):
        truck = [depot]
        for item in solsort:
            if solsort[item][0] == i:
                truck.append(item)
        truck.append(depot)
        trucks.append(truck)

    times = {}

    for t in trucks:
        stime = 0
        for i in range(1, len(t)):

            if stime + odl[(t[i - 1], t[i])] > cl_serv[t[i]]["start"]:
                stime = stime + odl[(t[i - 1], t[i])]
                times[t[i]] = stime
            elif stime + odl[(t[i - 1], t[i])] <= cl_serv[t[i]]["start"]:
                stime = cl_serv[t[i]]["start"]
                times[t[i]] = stime

    return solution_clientes2, init_val, times

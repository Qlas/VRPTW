import copy

from .error import TWerror


def init_solution(max_capacity, cl_serv, odl, cost):

    cl_serv_k = list(cl_serv.keys())
    depot = list(cl_serv.keys())[0]
    cl_serv_k.sort()
    ro = [depot]
    rr = []
    while len(ro) != len(cl_serv_k):
        r = [depot]
        current_capacity = 0
        current_time = 0
        while current_capacity != max_capacity:
            cl_r = 10 ** 1000
            bkey = ""
            for item in list(cl_serv.keys()):
                if item == r[-1]:
                    continue
                if (
                    (odl[item, r[-1]] <= cl_r)
                    and (odl[item, r[-1]] != 0)
                    and (item not in bkey)
                    and item not in ro
                    and current_time + odl[item, r[-1]] <= cl_serv[item]["end"]
                    and current_capacity + cl_serv[item]["demand"] <= max_capacity
                ):
                    cl_r1 = odl[item, r[-1]]
                    crcap = current_capacity + cl_serv[item]["demand"]
                    crtime = current_time + odl[item, r[-1]]
                    bkey = item

            if bkey != r[-1] and bkey != "" and crcap <= max_capacity and crtime <= cl_serv[bkey]["end"]:
                cl_r = cl_r1
                current_capacity = current_capacity + cl_serv[bkey]["demand"]
                if current_time + odl[bkey, r[-1]] <= cl_serv[bkey]["start"]:
                    current_time += cl_serv[bkey]["start"]
                else:
                    current_time += odl[bkey, r[-1]]

                r.append(bkey)
                ro.append(bkey)
            else:
                break

        if len(r) == 1 and len(ro) != len(cl_serv_k):
            raise TWerror(list(set(cl_serv_k).difference(ro)))
        rr.append(r)
        rc = copy.deepcopy(rr)

        cost_solution = 0
        for t in rc:
            t.append(depot)
            for i in range(1, len(t)):
                cost_solution += cost[(t[i - 1], t[i])]

    return rr, cost_solution

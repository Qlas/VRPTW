from .check import verify
from .error import client_capacity_error
from .initsol import init_solution
from .lastsol import secalgo


def run_VRTW_algorithm(cl_serv, max_capacity, odl, cost, kadencja, maxint):

    data_test = verify(cl_serv, max_capacity)
    if data_test[0]:
        raise client_capacity_error(data_test[1])
    inisol = init_solution(max_capacity, cl_serv, odl, cost)
    initialsolution = inisol[0]
    init_val = inisol[1]
    sol = secalgo(initialsolution, init_val, kadencja, cl_serv, maxint, cost, odl, max_capacity)

    sol1 = sol[0]
    sol2 = sol[1]
    sol3 = sol[2]

    return sol1, sol2, sol3

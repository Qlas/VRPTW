from check import verify
from initsol import init_solution
from main_al import secalgo
from error import klient_capacity_error

def przelicz(cl_serv,max_capacity,odl,cost, kadencja,maxint):

        data_test = verify(cl_serv,max_capacity)
        if data_test[0] : raise klient_capacity_error(data_test[1])
        inisol = init_solution(max_capacity,cl_serv,odl,cost)
        initialsolution = inisol[0]
        init_val = inisol[1]
        sol = secalgo(initialsolution, init_val, kadencja, cl_serv,maxint, cost )

        sol1 =sol[0]
        sol2 = sol[1]

        return sol1, sol2



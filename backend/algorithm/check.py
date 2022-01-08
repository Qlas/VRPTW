def verify(cl_serv, max_capacity):
    bad_clients = []
    for klient in cl_serv:
        if cl_serv[klient]["demand"] > max_capacity:
            bad_clients.append(klient)
    if len(bad_clients) > 0:
        return True, bad_clients
    return False, None

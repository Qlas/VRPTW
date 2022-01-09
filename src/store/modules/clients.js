import clientService from "@/services/clientService";
import clientDistanceService from "@/services/clientDistanceService";
import { jsonConcat } from "@/utils/utils.js";

const state = {
    clients: [],
    clientDistance: [],
};

const getters = {
    clients: (state) => {
        return state.clients;
    },
    clientDistance: (state) => {
        return state.clientDistance;
    },
};

const actions = {
    getClientDistance({ commit }, params) {
        return new Promise((resolve, reject) => {
            clientDistanceService
                .fetchClients(params)
                .then((clients) => {
                    commit("setClientDistance", clients);
                    resolve();
                })
                .catch((err) => reject(err));
        });
    },

    getClients({ commit }, params) {
        return new Promise((resolve, reject) => {
            clientService
                .fetchClients(params)
                .then((clients) => {
                    commit("setClients", clients);
                    resolve();
                })
                .catch((err) => reject(err));
        });
    },

    addClient({ commit }, client) {
        return new Promise((resolve, reject) => {
            clientService
                .postClient(client)
                .then(() => {
                    commit("addClient", client);
                    resolve();
                })
                .catch((err) => reject(err));
        });
    },

    updateClient({ commit }, data) {
        return new Promise((resolve, reject) => {
            clientService
                .patchClient(data.update)
                .then(() => {
                    clientService
                        .fetchClients({})
                        .then((clients) => {
                            commit("setClients", clients);
                            resolve();
                        })
                })
                .catch((err) => reject(err));
        });
    },

    removeClient({ commit }, clientId) {
        return new Promise((resolve, reject) => {
            clientService
                .deleteClient(clientId)
                .then(() => {
                    clientService
                        .fetchClients({})
                        .then((clients) => {
                            commit("setClients", clients);
                            resolve();
                        })
                })
                .catch((err) => reject(err));
        });
    },
};

const mutations = {
    setClients(state, clients) {
        state.clients = clients;
    },

    setClientDistance(state, clientDistance) {
        state.clientDistance = clientDistance;
    },

    addClient(state, clients) {
        state.clients.push(clients);
    },

};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};

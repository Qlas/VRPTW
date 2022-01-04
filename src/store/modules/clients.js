import clientService from "@/services/clientService";
import { jsonConcat } from "@/utils/utils.js";

const state = {
    clients: [],
};

const getters = {
    clients: (state) => {
        return state.clients;
    },
};

const actions = {
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

import resultService from "@/services/resultService";
import { jsonConcat } from "@/utils/utils.js";

const state = {
    results: [],
};

const getters = {
    results: (state) => {
        return state.results;
    },
};

const actions = {
    getResults({ commit }, params) {
        return new Promise((resolve, reject) => {
            resultService
                .fetchResults(params)
                .then((results) => {
                    commit("setResults", results);
                    resolve();
                })
                .catch((err) => reject(err));
        });
    },

    addResult({ commit }, result) {
        return new Promise((resolve, reject) => {
            resultService
                .postResult(result)
                .then(() => {
                    commit("addResult", result);
                    resolve();
                })
                .catch((err) => reject(err));
        });
    },

    updateResult({ commit }, data) {
        return new Promise((resolve, reject) => {
            resultService
                .patchResult(data.update)
                .then(() => {
                    resultService
                        .fetchResults({})
                        .then((results) => {
                            commit("setResults", results);
                            resolve();
                        })
                })
                .catch((err) => reject(err));
        });
    },

    removeResult({ commit }, resultId) {
        return new Promise((resolve, reject) => {
            resultService
                .deleteResult(resultId)
                .then(() => {
                    resultService
                        .fetchResults({})
                        .then((results) => {
                            commit("setResults", results);
                            resolve();
                        })
                })
                .catch((err) => reject(err));
        });
    },
};

const mutations = {
    setResults(state, results) {
        state.results = results;
    },

    addResult(state, results) {
        state.results.push(results);
    },

};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};

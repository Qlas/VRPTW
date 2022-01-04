import { api } from "@/services/api";
import { NotificationProgrammatic as Notification } from "buefy";
import jwt_decode from "jwt-decode";
import router from "@/router";
import authService from "../../services/authService";

const state = {
    accessToken: localStorage.getItem("accessToken") || "",
    refreshToken: localStorage.getItem("refreshToken") || "",
    ciKey: null,
    refreshTokenCounterID: "",
};

const getters = {
    accessToken: (state) => state.accessToken,
    accessTokenDecoded: (state) => jwt_decode(state.accessToken),
    ciKeyDecoded: (state) => jwt_decode(state.ciKey),
    refreshTokenDecoded: (state) => jwt_decode(state.refreshToken),
    refreshToken: (state) => state.refreshToken,
    isAuthenticated: (state) => !!state.accessToken,
    isAccessTokenExpired: (state, getters) => {
        const exp = getters.accessTokenDecoded.exp;
        if (new Date(exp * 1000) < new Date()) {
            return true;
        } else {
            return false;
        }
    },
    refreshTokenCounterID: (state) => state.refreshTokenCounterID,
    authUser: (state, getters) => getters.accessTokenDecoded.user,
};

const actions = {
    getTokenPair({ dispatch }, credentials) {
        return new Promise((resolve, reject) => {
            authService
                .fetchTokens(credentials)
                .then((data) => {
                    dispatch("setTokens", data);
                    dispatch("startTokenRefreshCounter");
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    refreshAccessToken({ commit, getters, dispatch }) {
        return new Promise((resolve, reject) => {
            authService
                .fetchRefreshedAccessToken(getters.refreshToken)
                .then((data) => {
                    commit("setAccessToken", data.access);
                    dispatch("setAxiosHeaders", data.access);
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    setAxiosHeaders({ getters }) {
        api.defaults.headers.common["Authorization"] = "Bearer " + getters.accessToken;
    },
    removeAxiosHeaders() {
        delete api.defaults.headers.common["Authorization"];
    },
    setTokens({ commit, dispatch }, data) {
        commit("setAccessToken", data.access);
        commit("setRefreshToken", data.refresh);
        dispatch("setAxiosHeaders", data.access);
    },
    startTokenRefreshCounter({ dispatch, commit }) {
        const ID = setInterval(() => {
            dispatch("refreshAccessToken").catch(() => {
                dispatch("endAuthSession");
                router.push("/login");
                Notification.open({
                    duration: 8000,
                    message: `Refresh auth error. This should have never happened. Please sign in again. Please report this to administrator.`,
                    position: "is-top-right",
                    type: "is-danger",
                    hasIcon: true,
                });
            });
        }, 3600000); // 1 hour
        commit("setTokenRefreshCounterID", ID);
    },
    endAuthSession({ commit, getters, dispatch }, notification = false) {
        authService.logoutUser(getters.refreshToken).catch((err) => {
            Notification.open({
                duration: 8000,
                message: `There was ${err.response.status} error while logging you out. Please report this to administrator.`,
                position: "is-top-left",
                type: "is-warning",
                hasIcon: true,
            });
        });
        commit("removeTokens");
        dispatch("removeAxiosHeaders");

        const ID = getters.refreshTokenCounterID;
        if (ID != "") {
            clearInterval(ID);
        }
        if (notification) {
            Notification.open({
                duration: 8000,
                message: `Your session has expired, please sign in again.`,
                position: "is-top-right",
                type: "is-warning",
                hasIcon: true,
            });
        }
    },
    getCiKey({ commit }) {
        return new Promise((resolve, reject) => {
            authService
                .getCiKey()
                .then((data) => {
                    commit("setCiKey", data.token);
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
    obtainCiKey({ commit }) {
        return new Promise((resolve, reject) => {
            authService
                .obtainCiKey()
                .then((data) => {
                    commit("setCiKey", data.token);
                    resolve();
                })
                .catch((err) => {
                    reject(err);
                });
        });
    },
};

const mutations = {
    setTokenRefreshCounterID(state, ID) {
        state.refreshTokenCounterID = ID;
    },
    setRefreshToken(state, token) {
        state.refreshToken = token;
        localStorage.setItem("refreshToken", token);
    },
    setAccessToken(state, token) {
        state.accessToken = token;
        localStorage.setItem("accessToken", token);
    },
    removeTokens(state) {
        state.accessToken = "";
        state.refreshToken = "";
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
    },
    setCiKey(state, token) {
        state.ciKey = token;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};

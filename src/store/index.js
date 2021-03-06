import Vue from "vue";
import Vuex from "vuex";
import auth from "./modules/auth";
import clients from "./modules/clients";
import results from "./modules/results";

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        auth,
        clients,
        results
    },
});

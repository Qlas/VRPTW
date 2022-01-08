import Vue from "vue";
import App from "@/App.vue";

import Buefy from "buefy";
import store from "@/store";
import router from "@/router";
import errorHandler from "@/error";
import permissionUtils from "@/utils/permissionUtils";
import VueCookie from "vue-cookie";
import VueCountdown from "@chenfengyuan/vue-countdown";
import VueMarkdown from "vue-markdown";
import { NotificationProgrammatic as Notification } from "buefy";
import { ValidationProvider, ValidationObserver } from "vee-validate";
import { Network } from "vue-vis-network";
import "./validation/rules";
import ValidatedInput from "@/components/customInputs/validatedInput";
import ValidatedSelect from "@/components/customInputs/ValidatedSelect";

Vue.filter("capitalize", function (value) {
    value = value.toString();
    return value.charAt(0).toUpperCase() + value.slice(1);
});

Vue.config.productionTip = false;

// register global components
Vue.use(Buefy);
Vue.use(VueCookie);
Vue.component("vue-markdown", VueMarkdown);
Vue.component(VueCountdown.name, VueCountdown);

Vue.component("ValidationProvider", ValidationProvider);
Vue.component("ValidationObserver", ValidationObserver);
Vue.component(ValidatedInput.name, ValidatedInput);
Vue.component(ValidatedSelect.name, ValidatedSelect);
Vue.component('network', Network);

Vue.prototype.$errorHandler = errorHandler;
Vue.prototype.$permissions = permissionUtils;

// handle auth when user open / refresh the app
if (store.getters["auth/isAuthenticated"]) {
    store.dispatch("auth/setAxiosHeaders");
    if (store.getters["auth/isAccessTokenExpired"]) {
        store.dispatch("auth/endAuthSession", true);
        router.push("/login");
    } else {
        store
            .dispatch("auth/refreshAccessToken")
            .then(() => {
                store.dispatch("auth/startTokenRefreshCounter");
            })
            .catch(() => {
                Notification.open({
                    duration: 8000,
                    message: `Refresh auth error. This should have never happened. Please sign in again. Please report this to administrator.`,
                    position: "is-top-right",
                    type: "is-danger",
                    hasIcon: true,
                });
                store.dispatch("auth/endAuthSession");
                router.push("/login");
            });
    }
}

const vue = new Vue({
    router,
    store,
    render: (h) => h(App),
});

vue.$mount("#app");

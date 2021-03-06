import Vue from "vue";
import store from "@/store";
import Router from "vue-router";

import permissions from "@/utils/permissionUtils";

import Home from "@/views/Home";
import Clients from "@/views/Clients";
import Calculate from "@/views/Calculate";
import Results from "@/views/Results";
import Login from "@/views/Login";
import InsufficientPermissions from "@/views/InsufficientPermissions";

Vue.use(Router);

const router = new Router({
    routes: [
        {
            path: "/",
            name: "Home",
            component: Home,
            meta: { requiresAuth: false, requiresNoAuth: false, canBeOnFooter: false },
        },
        {
            path: "/clients",
            name: "Clients",
            component: Clients,
            beforeEnter: (to, from, next) => {
                const authUser = store.getters["auth/authUser"];
                if (
                    permissions.client.any(authUser)
                )
                    next();
                else next("/insufficient-permissions");
            },
            meta: { requiresAuth: true, requiresNoAuth: false, canBeOnFooter: false },
        },
        {
            path: "/calculate",
            name: "Calculate",
            component: Calculate,
            meta: { requiresAuth: true, requiresNoAuth: false, canBeOnFooter: false },
        },
        {
            path: "/results",
            name: "Results",
            component: Results,
            meta: { requiresAuth: true, requiresNoAuth: false, canBeOnFooter: false },
        },
        {
            path: "/login",
            name: "Login",
            component: Login,
            meta: { requiresAuth: false, requiresNoAuth: true, canBeOnFooter: false },
        },
        {
            path: "/insufficient-permissions",
            name: "Insufficient permissions",
            component: InsufficientPermissions,
            meta: { requiresAuth: true, requiresNoAuth: false, canBeOnFooter: false },
        },
    ],
    scrollBehavior() {
        return { x: 0, y: 0 };
    },
});
export default router;

router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (store.getters["auth/isAuthenticated"]) {
            next();
        } else {
            next("/login");
        }
    } else if (to.matched.some((record) => record.meta.requiresNoAuth)) {
        if (!store.getters["auth/isAuthenticated"]) {
            next();
        } else {
            next("/");
        }
    } else {
        next();
    }
});

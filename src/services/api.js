import axios from "axios";
import Cookies from "js-cookie";

// !!!!
// If you create an api instance to a view which is secured, you also need to update setAxiosHeaders and removeAxiosHeaders
// in @/store/auth.js
// !!!!

const api = axios.create({
    baseURL: "/api",
    timeout: 5000,
    headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken"),
    },
});

export { api };

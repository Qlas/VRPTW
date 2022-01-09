import { api } from "@/services/api";

export default {
    fetchClients(params) {
        return api.get(`client_distance/`, { params }).then((response) => response.data);
    },
};

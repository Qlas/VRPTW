import { api } from "@/services/api";

export default {
    fetchClients(params) {
        return api.get(`client/`, { params }).then((response) => response.data);
    },
    postClient(payload) {
        return api.post(`client/`, payload).then((response) => response.data);
    },
    patchClient(update) {
        return api
            .patch(`client/${update.clientId}/`, update.payload)
            .then((response) => response.data);
    },
    deleteClient(clientId) {
        return api.delete(`client/${clientId}/`).then((response) => response.data);
    },
};

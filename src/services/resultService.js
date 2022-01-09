import { api } from "@/services/api";

export default {
    fetchResults(params) {
        return api.get(`result/`, { params }).then((response) => response.data);
    },
    postResult(payload) {
        return api.post(`result/`, payload).then((response) => response.data);
    },
    patchResults(update) {
        return api
            .patch(`result/${update.resultId}/`, update.payload)
            .then((response) => response.data);
    },
    deleteResult(resultId) {
        return api.delete(`result/${resultId}/`).then((response) => response.data);
    },
};

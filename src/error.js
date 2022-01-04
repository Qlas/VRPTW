import { DialogProgrammatic as Dialog } from "buefy";
import { deslugify } from "@/utils/utils.js";

function create400ErrorMessage(error) {
    let errorMsgArr = [];
    for (const key in error.response.data) {
        for (const message of error.response.data[key])
            errorMsgArr.push(`<li><b>${deslugify(key)}: </b>${message}</li>`);
    }
    return `<ul style="list-style:inside">${errorMsgArr.join(" ")}</ul>`;
}

function createDefaultErrorMessage(error, activityString) {
    let msg =
        `Your request to endpoint <br> <i>${error.response.request.responseURL}</i> has failed with the code:` +
        "<br><br>" +
        `<b>${error.response.status} - ${error.response.statusText}</b>`;
    if (activityString)
        msg = `While ${activityString} this error occured:<br><br>` + msg;
    return msg;
}

const errorHandler = {
    handleResponseError: (error, activityString = null) => {
        switch (error.response.status) {
            case 400:
                Dialog.alert({
                    title: "Problem with your input data",
                    message: create400ErrorMessage(error),
                    confirmText: "Ok",
                    type: "is-danger",
                    hasIcon: true,
                    icon: "alert-circle-outline",
                });
                break;

            case 500:
                Dialog.alert({
                    title: "Connection to the server failed",
                    message:
                        "<b>Had trouble establishing connection to the server. Try refreshing the page.</b>" +
                        "<br> If the problem occurs frequently please contact our team.",
                    confirmText: "Refresh",
                    canCancel: true,
                    cancelText: "Cancel",
                    type: "is-danger",
                    hasIcon: true,
                    icon: "alert-circle-outline",
                    onConfirm: () => {
                        window.location.reload();
                    },
                });
                break;

            default:
                Dialog.alert({
                    title: "Something went wrong...",
                    message: createDefaultErrorMessage(error, activityString),
                    confirmText: "Ok",
                    type: "is-danger",
                    hasIcon: true,
                    icon: "alert-circle-outline",
                });
                break;
        }
    },
};

export default errorHandler;

import { extend } from "vee-validate";
import {
    numeric,
    alpha_num,
    alpha_dash,
    min_value,
    max_value,
    between,
    oneOf,
    required,
} from "vee-validate/dist/rules";
import { messages } from "vee-validate/dist/locale/en.json";

// List of already existing rules that you can add and edit https://vee-validate.logaretm.com/v3/guide/rules.html#rules
// --------------------------------------------------------------------------------------------------------------------
extend("required", {
    ...required,
    message: "This field is required.",
});

extend("numeric", {
    ...numeric,
    message: messages["numeric"],
});

extend("alpha_num", {
    ...alpha_num,
    message: messages["alpha_num"],
});

extend("alpha_dash", {
    ...alpha_dash,
    message: messages["alpha_dash"],
});

extend("min_value", {
    ...min_value,
    message: messages["min_value"],
});

extend("max_value", {
    ...max_value,
    message: messages["max_value"],
});

extend("between", {
    ...between,
    message: messages["between"],
});

extend("oneOf", {
    ...oneOf,
    message: "Invalid value! Select one from the list.",
});

// For creating new rules refer to https://vee-validate.logaretm.com/v3/guide/basics.html#adding-rules
// ---------------------------------------------------------------------------------------------------
extend("ip", {
    validate(value) {
        return /^((25[0-5]|(2[0-4]|1[0-9]|[1-9]|)[0-9])(\.(?!$)|$)){4}$/.test(value);
    },
    message: "Invalid IP address.",
});

extend("url", {
    validate(value) {
        return /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([-.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.[^ ]*)?$|^((http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(:[0-9]{1,5})?(\/.[^ ]*)?$/.test(
            value
        );
    },
    message: "Invalid URL.",
});

extend("segID", {
    params: ["field", "segIDs"],
    validate(value, { field, segIDs }) {
        for (const key in segIDs) {
            if ((field === key) | (key === "id")) continue;
            if (segIDs[key] === value) return false;
        }

        return true;
    },
    message: "Duplicate ID value.",
});

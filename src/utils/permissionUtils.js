import { capitalize } from "./utils";

const models = ["client"];
const actions = ["add", "change", "delete", "view"];

const permissionUtils = {};

for (const model of models) {
    permissionUtils[model] = {};

    for (const action of actions) {
        permissionUtils[model][`can${capitalize(action)}`] = (user) =>
            user.user_permissions.indexOf(`${action}_${model}`) > -1;
    }

    permissionUtils[model]["any"] = (user) => {
        for (const action of actions) {
            if (permissionUtils[model][`can${capitalize(action)}`](user)) return true;
        }
        return false;
    };

    permissionUtils[model]["all"] = (user) => {
        for (const action of actions) {
            if (!permissionUtils[model][`can${capitalize(action)}`](user)) return false;
        }
        return true;
    };
}

permissionUtils["any"] = (user) => {
    for (const model of models) {
        if (permissionUtils[model]["any"](user)) return true;
    }
    return false;
};

permissionUtils["all"] = (user) => {
    for (const model of models) {
        if (!permissionUtils[model]["all"](user)) return false;
    }
    return true;
};

export default permissionUtils;

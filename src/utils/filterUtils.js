const filterUtils = {
    collectOptionsFromField(field, reservations) {
        let data = [];
        for (let group in reservations) {
            for (let tl of reservations[group]) {
                if (!data.includes(tl[field])) {
                    data.push(tl[field]);
                }
            }
        }

        return data.sort();
    },

    filterByGroup(filterChecked, reservations) {
        let filteredReservations = {};
        if (filterChecked.group.length > 0) {
            for (const group of filterChecked.group) {
                filteredReservations[group] = reservations[group];
            }
        } else {
            for (const group in reservations) {
                filteredReservations[group] = reservations[group];
            }
        }
        return filteredReservations;
    },

    filterByField(filterChecked, reservations, filtersType) {
        let filters;
        let filteredReservations = Object.assign({}, reservations);

        switch (filtersType) {
            case "status":
                filters = filterChecked.status;
                break;
            case "hw_version":
                filters = filterChecked.hardware;
                break;
            case "platform_version":
                filters = filterChecked.platform;
                break;
        }

        if (filters.length > 0) {
            for (const group in reservations) {
                filteredReservations[group] = reservations[group].filter((tl) =>
                    filters.includes(tl[filtersType])
                );
            }
        }

        return filteredReservations;
    },

    parseParamsString(paramsString) {
        let params = {};
        let paramsStringArray = paramsString.split("&");

        for (const psa of paramsStringArray) {
            const [key, valueString] = psa.split("=");
            params[key] = valueString.split("%7C");
        } //                                "%7C" === "|"
        return params;
    },

    parseUrlParams(urlString, paramsOptions) {
        let params = {};

        for (const filterType of paramsOptions) {
            params[filterType] = [];
        }

        let paramsString = urlString.split("?")[1];

        if (paramsString) {
            const urlParams = this.parseParamsString(paramsString);
            for (const paramType of paramsOptions) {
                params[paramType] = [];
                if (Object.hasOwnProperty.call(urlParams, paramType)) {
                    urlParams[paramType].forEach((string, index, arr) => {
                        arr[index] = arr[index]
                            .replaceAll("%20", " ")
                            .replaceAll("%21", "!")
                            .replaceAll("%5E", "^")
                            .replaceAll("%24", "$");
                    }); // "%20" == " " "%21" == "!" "%5E" == "^" "%24" == "$"
                    params[paramType] = urlParams[paramType];
                }
            }
        }

        return params;
    },

    createUrlParams(params) {
        let paramsString = [];
        let paramsCopy = Object.assign({}, params);

        for (const filterType in paramsCopy) {
            if (paramsCopy[filterType].length > 0) {
                paramsString.push(`${filterType}=${paramsCopy[filterType].join("|")}`);
            }
        }

        if (paramsString.length > 0) {
            return "?" + paramsString.join("&");
        }

        return "";
    },
    addFiltersToParams(paramsObj, filters) {
        for (const filterType in filters) {
            if (filters[filterType]) paramsObj[filterType] = filters[filterType];
        }

        return paramsObj;
    },

    addOrderingToParams(paramsObj, orderingField, orderingType, array = false) {
        const toReturn = orderingType == "asc" ? orderingField : "-" + orderingField;

        paramsObj["ordering"] = array ? [toReturn] : toReturn;

        return paramsObj;
    },
};

export default filterUtils;

export function jsonConcat(o1, o2) {
    for (var key in o2) {
        o1[key] = o2[key];
    }
}

export function capitalize(str) {
    if (typeof str !== "string") return "";
    return str.charAt(0).toUpperCase() + str.slice(1);
}

export function deslugify(str) {
    return str.replaceAll("_", " ").toUpperCase();
}

export function getCurrentDates() {
    // set default value of datepicker to range from yesterday midnight to todays night (two full days)
    // e.g. for date.now() == 18th dec 18:56:12, it will return:
    // d1 = 17th dec 00:00:00
    // d2 = 18th dec 23:59:59
    var d1 = new Date(new Date().setHours(0, 0, 0, 0));
    var d2 = new Date(new Date().setHours(0, 0, 0, 0));
    d1.setDate(d1.getDate() - 1);
    d2.setDate(d2.getDate() + 1);
    d2.setSeconds(d2.getSeconds() - 1);
    return [d1, d2];
}

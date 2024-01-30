function getYear(date) {
    // https://en.wikipedia.org/wiki/Ab_urbe_condita
    return 753 + date.getUTCFullYear();
}

function getDayOfYear(date) {
    const y = date.getUTCFullYear();
    const m = date.getUTCMonth();
    const d = date.getUTCDate();
    // https://stackoverflow.com/questions/8619879/javascript-calculate-the-day-of-the-year-1-366
    return -1+m*31-(m>1?(1054267675>>m*3-6&7)-(y&3||!(y%25)&&y&15?0:1):0)+d;
}


function getDecimalSecondOfDay(date) {
    const ms = date.getUTCMilliseconds();
    const s = date.getUTCSeconds();
    const m = date.getUTCMinutes();
    const h = date.getUTCHours();
    // 864 is number of milliseconds in a decimal second, 24*60*60*1000/(10*100*100)
    return Math.trunc((ms+(s+(m+h*60)*60)*1000)/864);
}

function getTimeFromDecimalSeconds(seconds, dayOfWeek = 0) {
    return {
        hour: dayOfWeek*10 + Math.trunc(seconds/10000),
        minute: Math.trunc((seconds%10000)/100),
        second: seconds%100,
    }
}

function printTime() {
    const date = new Date();
    const dayOfYear = getDayOfYear(date);
    const secondOfDay = getDecimalSecondOfDay(date);

    const global = {
        year: getYear(date),
        week: Math.trunc(dayOfYear/10),
        ...getTimeFromDecimalSeconds(secondOfDay, dayOfYear%10)
    };

    console.log("global:",  global);

    navigator.geolocation.getCurrentPosition(function(position) {
        const longitude = position.coords.longitude;
        // const b = Math.trunc(1e8*((longitude+180)/360)/864);
        const longitudeInSeconds = Math.trunc(1e5*(longitude+180)/360);
        const shift = secondOfDay-longitudeInSeconds;
        const timeToNoonSeconds = shift >= -50000 && shift < 50000 ? Math.abs(shift) : 100000-Math.abs(shift);
        const period = (shift >= -50000 && shift < 0) || shift >= 50000 ? "am" : "pm";
        const local = {
            ...getTimeFromDecimalSeconds(timeToNoonSeconds),
            period: period
        };
        const noonSeconds = 100000-longitudeInSeconds;
        const noon = getTimeFromDecimalSeconds(noonSeconds)
        console.log("local:", local, "at longitude", longitude);
        console.log("noon: ", noon)
    }, function(error) {
        console.log(error);
    });
}

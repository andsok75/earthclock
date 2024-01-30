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
    // 864 is the number of milliseconds in a decimal second, 24*60*60*1000/(10*100*100).
    return Math.trunc((ms+(s+(m+h*60)*60)*1000)/864);
}

function getTimeFromDecimalSeconds(seconds, dayOfWeek = 0) {
    // There 100 decimal seconds in a decimal minute, 100 decimal minutes in a decimal hour, and
    // 10 decimal hours in a day or 100 decimal hours in a decimal (10 day) week.
    // Thus there are one million decimal seconds in a decimal week.
    return {
        hour: dayOfWeek*10 + Math.trunc(seconds/10000),
        minute: Math.trunc((seconds%10000)/100),
        second: seconds%100
    }
}

function getSecondsToLocalNoon(secondOfDay, secondOfDayAtLocalNoon) {
    const ds = secondOfDay-secondOfDayAtLocalNoon;
    const secondsToLocalNoon = -50000 < ds && ds < 50000 ? Math.abs(ds) : 100000-Math.abs(ds);
    const period = (-50000 <= ds && ds < 0) || 50000 <= ds ? "am" : "pm";
    return [secondsToLocalNoon, period];
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

    if (!navigator.geolocation) { return; }

    navigator.geolocation.getCurrentPosition(function(position) {
        const longitude = position.coords.longitude;
        // longitude below is measured in decimal seconds, as integer ranging from 0 up to 100000
        // Greenwich meridian is at 50000 and Sydney is at 92000 decimal seconds
        const longitudeInSeconds = Math.trunc(100000*(longitude+180)/360);
        const secondOfDayAtLocalNoon = 100000-longitudeInSeconds;
        const timeAtLocalNoon = getTimeFromDecimalSeconds(secondOfDayAtLocalNoon);
        const [secondsToLocalNoon, period] = getSecondsToLocalNoon(secondOfDay, secondOfDayAtLocalNoon);
        const local = {
            ...getTimeFromDecimalSeconds(secondsToLocalNoon),
            period: period
        };
        console.log("local:", local, "at longitude", longitude);
        console.log("noon: ", timeAtLocalNoon)
    }, function(error) {
        console.log(error);
    });
}

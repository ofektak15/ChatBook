function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();

    var full_comment = "";
    m = checkTime(m);
    s = checkTime(s);
    full_comment += h + " : " + m + " : " + s;
    document.getElementById("current_time").innerHTML = h + " : " + m + " : " + s;
    setTimeout(startTime, 500);

    if (today.getHours() < 12) {
        full_comment += "\n Good Morning :)";
    }

    else if (today.getHours() < 17) {
        full_comment += "\n Good Afternoon :)";
    }

    else {
        full_comment += "\n Good Evening :)";
        document.getElementById('current_time');
    }

    document.getElementById("current_time").innerHTML = full_comment;
}

function checkTime(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}



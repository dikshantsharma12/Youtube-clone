

function toggle(flag) {
    if (flag == "peoples") {
        document.getElementById("filtered-videos").style.display = "none";
        document.getElementById("filtered-users").style.display = "flex";
        document.getElementById("filtered-users").style.height = "44rem";
        document.getElementById("videos-button").style.backgroundColor = "#fff";
        document.getElementById("people-button").style.backgroundColor = "rgb(233, 233, 233)";
        videos = false

    }
    else {
        document.getElementById("filtered-videos").style.display = "flex";
        document.getElementById("filtered-videos").style.height = "44rem";
        document.getElementById("filtered-videos").style.overflowY = "scroll";
        document.getElementById("filtered-users").style.display = "none";
        document.getElementById("people-button").style.backgroundColor = "#fff";
        document.getElementById("videos-button").style.backgroundColor = "rgb(233, 233, 233)";
        videos = true
    }

};
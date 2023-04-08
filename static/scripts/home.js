var flag = true;
function minimizeOrMaximize() {
    if (flag == true) {
        document.querySelector(".more-area-minimize").style.display = "block";
        document.querySelector(".more-area").style.display = "none";
        flag = false;
    } else {
        document.querySelector(".more-area-minimize").style.display = "none";
        document.querySelector(".more-area").style.display = "block";
        flag = true;
    }
}



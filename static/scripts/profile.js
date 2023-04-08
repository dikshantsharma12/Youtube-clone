function openForm() {
    document.querySelector(".bg-modal").style.display = "flex";
}
function closeForm() {
    document.querySelector(".bg-modal").style.display = "none";
}

function openUploadVideoForm() {
    document.querySelector(".upload-video-form-outer").style.display = "flex";
}
function closeUploadVideoForm() {
    document.querySelector(".upload-video-form-outer").style.display = "none";
}

function toggle(className, selfClass) {
    var classList = [
        "personal-home",
        "personal-videos",
        "personal-playlists",
        "personal-channels",
        "personal-about",
    ];
    var navigationList = [
        "navigation-home",
        "navigation-videos",
        "navigation-playlists",
        "navigation-channels",
        "navigation-about",
    ];
    for (let currClass of classList) {
        if (className == currClass) {
            document.querySelector("." + currClass).style.display = "block";
        } else {
            document.querySelector("." + currClass).style.display = "none";
        }
    }
    for (let currClass of navigationList) {
        if (selfClass == currClass) {
            document.querySelector("." + currClass).style.borderBottom =
                "solid";
            document.querySelector("." + currClass).style.opacity = 1;
        } else {
            document.querySelector("." + currClass).style.borderBottom = "none";
            document.querySelector("." + currClass).style.opacity = 0.5;
        }
    }
}

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

function previewImage(event) {
    var image = URL.createObjectURL(event.target.files[0]);
    var imageArea = document.getElementById("profile-image-input");
    imageArea.style.backgroundImage = "url(" + image + ")";
}

function previewThumbnail(event) {
    var image = URL.createObjectURL(event.target.files[0]);
    document.getElementById("thumbnail-image-input-icon").style.display =
        "none";
    var imageArea = document.getElementById("thumbnail-image-input-div");
    imageArea.style.backgroundImage = "url(" + image + ")";
}

function previewVideo(event) {
    var video = URL.createObjectURL(event.target.files[0]);
    var videoDiv = document.getElementById("section-uploaded-video-inner");
    var previewVideo = document.createElement("video");
    if (videoDiv.hasChildNodes()) {
        videoDiv.removeChild(videoDiv.firstChild);
    }
    previewVideo.src = video;
    previewVideo.controls = true;
    previewVideo.setAttribute("width", "auto");

    document.getElementById("section-uploaded-video__p").innerHTML =
        "Choose Another";
    filename = event.target.files[0].name.split(".")[0];
    document.getElementById("section-uploaded-video-text").style.display =
        "block";
    document.getElementById("filename-header").innerHTML = filename;
    document.getElementById("filename").innerHTML = event.target.files[0].name;
    var imageArea = document.getElementById("section-uploaded-video-inner");
    imageArea.appendChild(previewVideo);
}

const submitButton = document.getElementById("subscribe");

submitButton.addEventListener("click", async function () {
    data = JSON.stringify({
        youtuber: document.getElementById("subscribe").getAttribute("youtuber"),
        option: document.getElementById("subscribe").getAttribute("option"),
    });
    console.log(data);
    await fetch("/subscribe_or_unsubscribe/", {
        method: "POST",
        body: data,
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector(
                "[name = csrfmiddlewaretoken]"
            ).value,
        },
    })
        .then((response) => response.json())
        .then((output) => {
            console.log(output);
            if (output.status == "subscribed") {
                document
                    .getElementById("subscribe")
                    .setAttribute("option", "unsubscribe");
                currValue = parseInt(
                    document.getElementById("subscribers-count").innerHTML
                );
                document.getElementById("subscribers-count").innerHTML =
                    currValue + 1;
                try {
                    document.querySelector(".subscribe").innerHTML =
                        "Unsubscribe";
                } catch (error) {}
                try {
                    document.querySelector(".unsubscribe").innerHTML =
                        "Unsubscribe";
                } catch (error) {
                    console.log(error);
                }
            } else {
                document
                    .getElementById("subscribe")
                    .setAttribute("option", "subscribe");
                currValue = parseInt(
                    document.getElementById("subscribers-count").innerHTML
                );
                document.getElementById("subscribers-count").innerHTML =
                    currValue - 1;
                try {
                    document.querySelector(".subscribe").innerHTML =
                        "Subscribe";
                } catch (error) {
                    console.log(error);
                }
                try {
                    document.querySelector(".unsubscribe").innerHTML =
                        "Subscribe";
                } catch (error) {
                    console.log(error);
                }
            }
            return output;
        })
        .catch((error) => console.error(error));
});

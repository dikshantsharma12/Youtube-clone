function seterror(id, error) {
    document.getElementById(id).innerHTML = error;
    document.getElementById(id).style.color = "red";
}
function validateForm() {
    var correct = true;

    var password = document.getElementById("pass").value;
    var confirm = document.getElementById("confirm").value;

    if (password.length < 8) {
        seterror("password-error", "Use 8 characters or more for your password");
        document.getElementById("pass").style.borderColor = "red";
        correct = false;
    } else if (password != confirm) {
        seterror("password-error", "Those passwords didn’t match. Try again.");
        document.getElementById("pass").style.borderColor = "rgb(196, 196, 196)";
        document.getElementById("confirm").style.borderColor = "red";
        correct = false;
    }

    return correct;
}

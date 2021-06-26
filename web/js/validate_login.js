function validate_login() {

    if (document.getElementById("username").value == "" || document.getElementById("password").value == "") {
        alert("You must Enter UserName and Password");
        return false;
    }
    return true;
}
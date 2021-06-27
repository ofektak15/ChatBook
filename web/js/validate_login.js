function validate_login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    if (username == "" || password == "") {
        alert("You must Enter UserName and Password");
        return false;
    }
    alert("Attempting to login...");
    status_registration = eel.login(username, password);
    // TODO: different errors for failed registration and failed checks
    return status_registration;
}
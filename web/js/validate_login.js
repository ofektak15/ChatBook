// https://github.com/ChrisKnott/Eel/issues/426
eel.expose(go_to)
function go_to(url){
    window.location.replace(url);
};

async function validate_login() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

        if (username == ""){
        document.getElementById("error_username").innerHTML = "You must enter username!";
    }
    else{
        document.getElementById("error_username").innerHTML = "";
    }

    if (password == ""){
        document.getElementById("error_password").innerHTML = "You must enter password!";
        }
    else{
        document.getElementById("error_password").innerHTML = "";
    }
    alert("Attempting to login...");
    status_registration = await eel.login(username, password)();
    alert(status_registration)
    if (status_registration == "False"){
        document.getElementById("general_error").innerHTML = "Username or password does not match.";
        return false;
    }
    return true;
}
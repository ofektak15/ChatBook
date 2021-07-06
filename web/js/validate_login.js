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
    status_registration = await eel.login(username, password)();
    document.getElementById("general_error").innerHTML = "";
    if (status_registration == false){
        if (username != "" && password != ""){
            document.getElementById("general_error").innerHTML = "Username or password does not match.";
            return false;
        }
    }
    return true;
}
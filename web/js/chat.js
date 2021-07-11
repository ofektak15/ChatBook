
// The function doesn't get parameters.
// The function gets all the chats that are exist in the data base and shows the chats on the screen.
async function get_chats(){
    dict_chats = await eel.get_chats()(); // get all the chats in a dictionary
    var div_section = document.getElementById("inbox_chat");
    div_section.innerHTML = '';
    var active_chat_class = '';

    // a loop that goes through all the chats
    for(var chat_name in dict_chats){
        var chat_dict = dict_chats[chat_name];
        var chat_participants = chat_dict['chat_participants']; // the participants in the current group
        var chat_type = chat_dict['chat_type']; // the type of the chat - group or private
        var sender_username = chat_dict['sender_username']; // the username of the user who sent the

        // GROUP CHAT
        if (chat_type == 'group'){
            // if the current chat is the selected chat
            if (chat_name == g_selected_active_chat_shown){
                active_chat_class = ' active_chat'; // now the name of the class is - "chat_list active_chat"
                g_selected_active_chat_type = chat_type;
            }
            // showing the names of the chats
            div_section.innerHTML += '<div class="chat_list' + active_chat_class + '"><div class="chat_people"><div class="chat_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="chat_ib"><div onclick="get_chat_messages(\'' + chat_name + '\', \'' + chat_name  + '\');"><b>' + chat_name + '</b><br><div id="participants_' + chat_name + '"</div></div></div></div></div>';

            // showing the usernames of the participants in the current group
            document.getElementById("participants_" + chat_name).innerHTML = "participants: ";
            for (var i = 0; i < chat_participants.length; i++) {
                // if it's the last participant - don't add ','
                if (i == chat_participants.length - 1){
                    document.getElementById("participants_" + chat_name).innerHTML += chat_participants[i];

                }
               // if it's not the last participant - add ','
                else{
                    document.getElementById("participants_" + chat_name).innerHTML += chat_participants[i] + ",";
                }
            }
        }

        // PRIVATE CHAT
        else if (chat_type == 'private'){
            var pair_participants = chat_name.split(','); // an array of the two participants in the chat

            // if the username of the sender is in the first place - the shown chat name is the other name in the array
            if (pair_participants.indexOf(sender_username) == 0){
                var shown_chat_name = pair_participants[1];
            }
            else {
                var shown_chat_name = pair_participants[0];
            }

            // if the current chat is the selected chat
            if (shown_chat_name == g_selected_active_chat_shown){
                active_chat_class = ' active_chat'; // now the name of the class is - "chat_list active_chat"
                g_selected_active_chat_type = chat_type;
            }

            var is_connected = await get_is_connected(shown_chat_name); // is the user connected
            if (is_connected) // if the user is connected - show the name of the user and a connected icon
            {
                div_section.innerHTML += '<div class="chat_list' + active_chat_class + '"><div class="chat_people"><div class="chat_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="chat_ib"><div onclick="get_chat_messages(\'' + chat_name + '\', \'' + shown_chat_name  + '\');"><b>' + shown_chat_name + '</b><div id="connected_icon"</div></div></div></div></div>';
            }
            else // if the user is disconnected - show the name of the user and a disconnected icon
            {
                div_section.innerHTML += '<div class="chat_list' + active_chat_class + '"><div class="chat_people"><div class="chat_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="chat_ib"><div onclick="get_chat_messages(\'' + chat_name + '\', \'' + shown_chat_name  + '\');"><b>' + shown_chat_name + '</b><div id="disconnected_icon"</div></div></div></div></div>';
            }
        }
        if (active_chat_class != ''){
            g_selected_active_chat_real = chat_name;
        }
        active_chat_class = '';
    }
}


// The function gets the real chat name and the shown chat name
// The function shows on the screen all the messages in the chosen conversation
async function get_chat_messages(chat_name, shown_chat_name){
    g_selected_active_chat_real = chat_name; // the real selected chat name is the chat name

    // if the real chat name contains ',' - it's a private chat
    if (g_selected_active_chat_real.indexOf(',') != -1){
        g_selected_active_chat_type = "private";
    }

    // if the real chat name doesn't contain ',' - it's a group chat
    else{
        g_selected_active_chat_type = "group";
    }

    // PRIVATE CHAT
    if(chat_name.indexOf(',') != -1)
    {
        var is_connected = await get_is_connected(shown_chat_name);
        if (is_connected) // if the recipient is connected
        {
            document.getElementById("is_connected").innerText = "connected";
        }
        else // if the recipient is not connected
        {
            document.getElementById("is_connected").innerText = "disconnected";
        }
    }

    // showing on the screen the name of the chat
    document.getElementById("name_of_chat").innerHTML = shown_chat_name;
    var div_section = document.getElementById("msg_history");
    div_section.innerHTML = '';
    var dict_messages = await eel.get_chat_messages(chat_name)(); // all the messages in the current chat in a dictionary
    var list_chat_messages = dict_messages['list_messages']; // a list of all the messages
    var username = dict_messages['username']; // the user who is connected
    select_active_chat(shown_chat_name); // change the current chat from not active to active

    var msg_content = ''; // the content of the message
    var msg_from = '';    // who sent the message
    // A loop that goes through all the messages in the current chat
    for (var i = 0; i < list_chat_messages.length; i++) {
        msg_content = list_chat_messages[i]['message_content']; // the content of the message
        current_time = list_chat_messages[i]['time']; // the time the message was sent
        msg_from = list_chat_messages[i]['from']; // who sent the message

        // if the user who is connected sent the message
        if (msg_from == username){
            if (chat_name.indexOf(',') != -1) // if there is not ',' - private chat
            {
                div_section.innerHTML += '<div class="outgoing_msg"><div class="sent_msg"></div><div class="sent_msg"><div class="sent_withd_msg"><p>' + msg_content + '</p><span class="time_date">' + current_time + '</span></div></div></div>';
            }
            else // if there is a ',' - group chat
            {
                document.getElementById("is_connected").innerText = ""; // if it's a group - there is no indication to is connected
                div_section.innerHTML += '<div class="outgoing_msg"><div class="sent_msg"></div><div class="sent_msg"><div class="sent_withd_msg"><p style="color: #ADFF2F">' + msg_from + '<br></p><p>' + msg_content + '</p><span class="time_date">' + current_time + '</span></div></div></div>';
            }
        }

        // if the user who is connected didn't send the message
        else{
            if (chat_name.indexOf(',') != -1) // if there is not ',' - private chat
            {
                 div_section.innerHTML += '<div class="incoming_msg"><div class="incoming_msg_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="received_msg"><div class="received_withd_msg"><p>' + msg_content + '</p><span class="time_date">' + current_time + '</span></div></div></div>';
            }
            else // if there is a ',' - group chat
            {
                document.getElementById("is_connected").innerText = ""; // if it's a group - there is no indication to is connected
                div_section.innerHTML += '<div class="incoming_msg"><div class="incoming_msg_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="received_msg"><div class="received_withd_msg"><p style="color: red"">' + msg_from + '<br><p>' + msg_content + '</p></p><span class="time_date">' + current_time + '</span></div></div></div>';
            }
        }
    }
}

// The function gets a shown chat name
// The function changes the div's class of the parameter from not active to active
function select_active_chat(shown_chat_name){
    g_selected_active_chat_shown = shown_chat_name;
    var div_section = document.getElementById("inbox_chat");
    var div_objs = div_section.getElementsByTagName('div');
    for (var index = 0; index < div_objs.length; index++){
        // if the current chat is the active chat - change it to not active chat
        if (div_objs[index].getAttribute('class') == 'chat_list active_chat'){
            div_objs[index].setAttribute('class', 'chat_list');
        }
        // if the class of the current chat is not active chat
        // AND
        // the name of the chat in the current chat is the shown chat parameter - change it to active
        if (div_objs[index].getAttribute('class') == 'chat_list'){
            if (div_objs[index].getElementsByTagName('div')[2].innerText == shown_chat_name){
                div_objs[index].setAttribute('class', 'chat_list active_chat');
            }
        }
    }
}

// The function doesn't get parameters
// The function shows on the top of the screen the name of the connected user and says hello. Example: "Hello Ofek!"
async function say_hello_to_username(){
    var username = await eel.get_username()();
    var div_section = document.getElementById("say-hello");
    div_section.innerHTML = "Hello " + username + "!"
}


// global vars
var g_selected_active_chat_shown = ''; // the shown active chat name
var g_selected_active_chat_real = '';  // the real active chat name
var g_selected_active_chat_type = '';  // the type of the active chat
var g_input_create_chat_name = '';


// The function doesn't get parameters
// The function sends a message
async function send_message(){
    // the field where the user writes his message
    var element_input_write_msg = document.getElementById("input_write_msg");

    // the content of the message
    var message_content = element_input_write_msg.value;
    var username = await eel.get_username()();
    var chat_type = g_selected_active_chat_type; // the type of the chat
    var status = await eel.send_message(username, g_selected_active_chat_real, message_content, chat_type)();
    element_input_write_msg.value = ''; // deleting the written message which has been sent to the chat
}


async function create_chat(){
    var group_name_div = document.getElementById("create_chat_group_name");
    var div_input_create_chat_name = document.getElementById("create-chats");

    if (div_input_create_chat_name.value == ""){
        document.getElementById("error_usernames").innerHTML = "You must enter username/s!";
        return;
    }
    else{
        g_input_create_chat_name = div_input_create_chat_name.value;
        document.getElementById("error_usernames").innerHTML = "";
        if (group_name_div.getElementsByTagName('input').length == 0){
            create_private_chat(g_input_create_chat_name);
        }
        else{
            var group_name = '';
            if (group_name_div.getElementsByTagName('input').length >= 1 ){
                group_name = group_name_div.getElementsByTagName('input')[0].value;
            }
            if (group_name == ""){
                document.getElementById("error_group_name").innerHTML = "You must enter group name!";
                return;
            }
            document.getElementById("error_group_name").innerHTML = "";
            create_group_chat(g_input_create_chat_name, group_name);
        }
    }
    document.getElementById("group_name").value = "";
        document.getElementById("create-chats").value = "";

}

async function create_private_chat(recipient){
    await eel.create_private_chat(recipient)();
}


async function create_group_chat(recipient, group_name){
    await eel.create_group_chat(recipient, group_name)();
}

function check_create_group(){
    var div_input_create_chat_name = document.getElementById("create-chats");
    if (div_input_create_chat_name == null){
        return;
    }
    g_input_create_chat_name = div_input_create_chat_name.value;

    var group_name_div = document.getElementById("create_chat_group_name");
    if (g_input_create_chat_name.indexOf(",") != -1){
        group_name_div.innerHTML = '<input type="text" id="group_name" placeholder="Enter group_name"/>';
    }
    else{
        group_name_div.innerHTML = "";
        document.getElementById("error_group_name").innerHTML = "";
    }
}

async function get_is_connected(username){
    is_connected = await eel.get_is_connected(username)();
    return is_connected;
}



async function log_out(){
    var username = await eel.get_username()();
    await eel.log_out(username)();
    go_to("login.html")
}


async function get_is_update(){
    var is_update = await eel.get_is_update()();
    return is_update;
}

eel.expose(go_to)
function go_to(url){
    window.location.replace(url);
}



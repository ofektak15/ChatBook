async function get_chats(){
    dict_chats = await eel.get_chats()();
    var div_section = document.getElementById("inbox_chat");
    div_section.innerHTML = '';
    var active_chat_class = '';
    for(var chat_name in dict_chats){
        var chat_dict = dict_chats[chat_name];
        var chat_participants = chat_dict['chat_participants'];
        var chat_type = chat_dict['chat_type'];
        var sender_username = chat_dict['sender_username'];
        if (chat_type == 'group'){
            if (chat_name == g_selected_active_chat_shown){
                active_chat_class = ' active_chat';
                g_selected_active_chat_type = chat_type;
            }
            div_section.innerHTML += '<div class="chat_list' + active_chat_class + '"><div class="chat_people"><div class="chat_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="chat_ib"><button onclick="get_chat_messages(\'' + chat_name + '\', \'' + chat_name  + '\');">' + chat_name + '</button></div></div></div>';
        }
        else if (chat_type == 'private'){
            var pair_participants = chat_name.split(',');
            if (pair_participants.indexOf(sender_username) == 0){
                var shown_chat_name = pair_participants[1];
            }
            else {
                var shown_chat_name = pair_participants[0];
            }
            if (shown_chat_name == g_selected_active_chat_shown){
                active_chat_class = ' active_chat';
                g_selected_active_chat_type = chat_type;
            }
            div_section.innerHTML += '<div class="chat_list' + active_chat_class + '"><div class="chat_people"><div class="chat_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="chat_ib"><button onclick="get_chat_messages(\'' + chat_name + '\', \'' + shown_chat_name  + '\');">' + shown_chat_name + '</button></div></div></div>';
        }
        if (active_chat_class != ''){
            g_selected_active_chat_real = chat_name;
//            alert("g_selected_active_chat_real: " + g_selected_active_chat_real)
        }
        active_chat_class = '';
    }
}
async function get_chat_messages(chat_name, shown_chat_name){
    var div_section = document.getElementById("msg_history");
    div_section.innerHTML = '';
    var dict_messages = await eel.get_chat_messages(chat_name)();
    var list_chat_messages = dict_messages['list_messages'];
    var username = dict_messages['username'];
    select_active_chat(shown_chat_name);

    var msg_content = '';
    var msg_from = '';
    for (var i = 0; i < list_chat_messages.length; i++) {
        msg_content = list_chat_messages[i]['message_content'];
        current_time = list_chat_messages[i]['time'];

        msg_from = list_chat_messages[i]['from'];
        if (msg_from == username){
            div_section.innerHTML += '<div class="outgoing_msg"><div class="sent_msg"></div><div class="sent_msg"><div class="sent_withd_msg"><p>' + msg_from + '<br>' + msg_content + '</p><span class="time_date">' + current_time + '</span></div></div></div>';
        }
        else{
            div_section.innerHTML += '<div class="incoming_msg"><div class="incoming_msg_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="received_msg"><div class="received_withd_msg"><p>' + msg_from + '<br>' + msg_content + '</p><span class="time_date">' + current_time + '</span></div></div></div>';
        }
        div_section.innerHTML += '<div class="sender_name">' + msg_from + '</div>';
    }
}

async function get_username(){
    var username = await eel.get_username()();
    return username;
}


async function say_hello_to_username(){
    var username = get_username();

    var div_section = document.getElementById("text-center");
    div_section.innerHTML = "Hello " + username + "!"
}

var g_selected_active_chat_shown = '';
var g_selected_active_chat_real = '';
var g_selected_active_chat_type = '';

function select_active_chat(shown_chat_name){
    g_selected_active_chat_shown = shown_chat_name;
    var div_section = document.getElementById("inbox_chat");
    var div_objs = div_section.getElementsByTagName('div');
    for (var index = 0; index < div_objs.length; index++){
        if (div_objs[index].getAttribute('class') == 'chat_list active_chat'){
            div_objs[index].setAttribute('class', 'chat_list');
        }
        if (div_objs[index].getAttribute('class') == 'chat_list'){
            if (div_objs[index].getElementsByTagName('div')[2].innerText == shown_chat_name){
                div_objs[index].setAttribute('class', 'chat_list active_chat');
            }
        }
    }
}

async function send_message(){
    var element_input_write_msg = document.getElementById("input_write_msg");
    var message_content = element_input_write_msg.value;
    var username = await eel.get_username()();
    var chat_type = g_selected_active_chat_type;
    var status = await eel.send_message(username, g_selected_active_chat_real, message_content, chat_type)();
    element_input_write_msg.value = '';
}
////show on the screen a conversation title on the right side of the screen
//eel.expose(add_conversation_to_list);
//function add_conversation_to_list(conv)
//{
//    var div_section = document.getElementById("conversations");
//    div_section.innerHTML += '<p class="friend_item" onclick="ask_to_get_conversation(this)" id="' + conv + '">' + conv + "</p>";
//}
//
////show on the screen a conversation title on the right side of the screen
//eel.expose(add_all_conversations_to_list);
//function add_all_conversations_to_list(conv, only_names)
//{
//    var only_names = only_names.split("//");
//    var chats = conv.split("//");
//    var div_section = document.getElementById("conversations");
//    for(var i = 0; i < chats.length; i++)
//    {
//        var names = chats[i].split(",");
//        div_section.innerHTML += '<p class="friend_item" onclick="ask_to_get_conversation(this)" id="' + only_names[i] + '">' + names + "</p>";
//    }
//}
//
////send to the server a request to get specific conversation
//function ask_to_get_conversation(elem)
//{
//    document.title = elem.id;
//    eel.receive_specific_conversation(elem.id);
//}


async function get_chats(){
    alert("get_chats...");
    dict_chats = await eel.get_chats()();
    alert(dict_chats);
    var div_section = document.getElementById("inbox_chat");
    for(var chat_name in dict_chats){
        var chat_dict = dict_chats[chat_name];
        var chat_participants = chat_dict['chat_participants'];
        var chat_type = chat_dict['chat_type'];
        var sender_username = chat_dict['sender_username'];
        if (chat_type == 'group'){
            div_section.innerHTML += '<div class="chat_list"><div class="chat_people"><div class="chat_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="chat_ib"><button onclick="get_chat_messages(\'' + chat_name + '\', \'' + chat_name  + '\');">' + chat_name + '</button></div></div></div>';
        }
        else if (chat_type == 'private'){
            var pair_participants = chat_name.split(',');
            if (pair_participants.indexOf(sender_username) == 0){
                var shown_chat_name = pair_participants[1];
            }
            else {
                var shown_chat_name = pair_participants[0];
            };
            div_section.innerHTML += '<div class="chat_list"><div class="chat_people"><div class="chat_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="chat_ib"><button onclick="get_chat_messages(\'' + chat_name + '\', \'' + shown_chat_name  + '\');">' + shown_chat_name + '</button></div></div></div>';
        }
    }
}
async function get_chat_messages(chat_name, shown_chat_name){
    alert("get_chat_messages...");
    var div_section = document.getElementById("msg_history");

    var dict_messages = await eel.get_chat_messages(chat_name)();
    var list_chat_messages = dict_messages['list_messages'];
    var username = dict_messages['username'];
    select_active_chat(shown_chat_name);
//    alert(list_chat_messages);
//    alert(list_chat_messages);
//    var div_section = document.getElementById("inbox_chat");
    var msg_content = '';
    var msg_from = '';
    for (var i = 0; i < list_chat_messages.length; i++) {
        msg_content = list_chat_messages[i]['message_content'];

        msg_from = list_chat_messages[i]['from'];
        if (msg_from == username){
            div_section.innerHTML += '<div class="outgoing_msg"><div class="sent_msg"></div><div class="sent_msg"><div class="sent_withd_msg"><p>' + msg_content + '</p><span class="time_date"> 11:01 AM    |    June 9</span></div></div></div>'
        }
        else{
            div_section.innerHTML += '<div class="incoming_msg"><div class="incoming_msg_img"><img src="img/default_profile_icon.png" alt="profile"></div><div class="received_msg"><div class="received_withd_msg"><p>' + msg_content + '</p><span class="time_date"> 11:01 AM    |    June 9</span></div></div></div>'
        }
//        alert("From: " + msg_from + "\nContent: " + msg_content);
    }
}

function say_hello_to_username(username){
    var div_section = document.getElementById("text-center");
    div_section.innerHTML = "Hello " + username + "!"
}


function select_active_chat(shown_chat_name){
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
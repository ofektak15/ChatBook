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
    list_chat_names = await eel.get_chats()();
    alert(list_chat_names);
    var div_section = document.getElementById("inbox_chat");
    for (var i; i < list_chat_names.length; i++) {
        div_section.innerHTML += '<div class="chat_list"><div class="chat_people"><div class="chat_ib"><h5>' + list_chat_names[i] + '</h5></div></div></div>';
    }
}

// eel.get_chats() -> promise()

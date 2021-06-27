//send a connect request to the server
function connect()
{
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var ip = document.getElementById("ip").value;
    document.title = username;
    eel.send_connect_request(username, password, ip);
}

//show an error message when log in fail
eel.expose(show_message_for_log_in);
function show_message_for_log_in(message)
{
    var error = document.getElementById("error");
    error.innerHTML = message;//"Username or password not matches";
}

//show message after trying to add a new friend
eel.expose(show_message_when_adding_friend);
function show_message_when_adding_friend(msg)
{
    var message = document.getElementById("message_new_friend");
    message.innerHTML = msg;
}

//send to the server a request to add a friend
function add_friend()
{
    var friend_name = document.getElementById("text_edit_new_friend").value;
    eel.add_conversation(friend_name);
}

//show on the screen a conversation title on the right side of the screen
eel.expose(add_conversation_to_list);
function add_conversation_to_list(conv)
{
    var div_section = document.getElementById("conversations");
    div_section.innerHTML += '<p class="friend_item" onclick="ask_to_get_conversation(this)" id="' + conv + '">' + conv + "</p>";
}

//show on the screen a conversation title on the right side of the screen
eel.expose(add_all_conversations_to_list);
function add_all_conversations_to_list(conv, only_names)
{
    var only_names = only_names.split("//");
    var chats = conv.split("//");
    var div_section = document.getElementById("conversations");
    for(var i = 0; i < chats.length; i++)
    {
        var names = chats[i].split(",");
        div_section.innerHTML += '<p class="friend_item" onclick="ask_to_get_conversation(this)" id="' + only_names[i] + '">' + names + "</p>";
    }
}

//send to the server a request to get specific conversation
function ask_to_get_conversation(elem)
{
    document.title = elem.id;
    eel.receive_specific_conversation(elem.id);
}

//show chat
eel.expose(show_conversation);
function show_conversation(title, conversation, username)
{
    var t = document.getElementById("title");
    t.innerHTML = title;

    var div_section = document.getElementById("chat-area");
    div_section.innerHTML = "";

    var messages = conversation.split("~");
    for(var i = 0; i < messages.length; i++)
    {
        update_conversation(messages[i], username);
    }
}

//update the chat
eel.expose(update_conversation);
function update_conversation(message, username)
{
    var div_section = document.getElementById("chat-area");
    var sender = message.split("^")[1];
    var message_content = message.split("^")[2];

    if(sender == username)
    {
        div_section.innerHTML += "<div class='message-left'> <div class='message-title'>" +
                                 sender +
                                 "</div> <div class='message-text'>" +
                                 replaceURLs(message_content) +
                                 "</div> </div>";
    }

    else
    {
        div_section.innerHTML += "<div class='message-right'> <div class='message-title'>" +
                                  sender +
                                  "</div> <div class='message-text'>" +
                                  replaceURLs(message_content) +
                                  "</div> </div>";
    }

    //scroll down
    div_section.scrollTop = div_section.scrollHeight;
}

function replaceURLs(message) {
  if(!message) return;

  var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;
  return message.replace(urlRegex, function (url) {
    var hyperlink = url;
    if (!hyperlink.match('^https?:\/\/')) {
      hyperlink = 'http://' + hyperlink;
    }
    return '<a href="' + hyperlink + '" target="_blank" rel="noopener noreferrer">' + url + '</a>'
  });
}

/*function detectURLs(text)
{
    var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;
    //return text.replace(urlRegex, function(url)
    //{
    //    return '<a target="_blank" href="' + url + '">' + url + '</a>';
    //})
    // or alternatively
    return text.replace(urlRegex, '<a target="_blank" href="$1">$1</a>')
}*/


//send to the server message for specific chat
function send_message()
{
    var message = document.getElementById("text_edit_messages");
    var content = message.value.trim();

    if(content.length > 0)
    {
        eel.send_message(content.replace(";", "☐").replace("{~$^}", "☐"));
    }
    message.value = "";
}

//show the register page
function show_register_page()
{
    var myWindow = window.open("register_page.html", "newWindow", "width=500,height=700");
}

//send to the server a request to create new account
function create_new_account()
{
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var ip = document.getElementById("ip").value;
    eel.create_new_account(username, password, ip);
}

//show the response from the server fer the create new account request
eel.expose(show_message_for_register);
function show_message_for_register(msg)
{
    var message = document.getElementById("message_register");
    if(msg == "Created")
    {
        message.innerHTML = msg + "<br>Close this window and log in";
    }

    else
    {
        message.innerHTML = msg;
    }
}

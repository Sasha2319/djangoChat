    location.href = "#lastMessage";

    $("#ddChatsButton").click(function(){
        location.href = '/chats/'
    })

    $("#ddPasswordButton").click(function(){
        location.href = '/changePassword/'
    })

    $("#ddLogOutButton").click(function(){
        location.href = '/logout/'
    })

    function send(){
    let mtV = $("#messageInput").val();
        if(mtV === ""){
        console.log("Empty")
        }
        if($("#messageInput").val() !== ""){
            const csrf = document.getElementsByName("csrfmiddlewaretoken");
            const token = csrf[0].value
            const messageText = document.getElementById("messageInput");
            let id = "new-" + String(sendTimeCount)
            console.log(id)

            const fd = new FormData()
            fd.append('csrfmiddlewaretoken', token)
            fd.append('author_name', username)
            fd.append('messageText', messageText.value)
            $.ajax({
                type: 'POST',
                url: url,
                enctype: 'multipart/form-data',
                data: fd,
                processData: false,
                success: function(response){
                    console.log(response)
                    $(`<div id=${id} class="media media-chat media-chat-reverse">
                            <div class="media-body">
                                <p><small>${response.author_name}</small></br>${response.messageText}</p>
                                <p class="meta" ><time datetime="2018"><span class="timeSpan"><small>${response.pub_date}</small></span></time></p>
                            </div>
                        </div>`).insertAfter("#lastMessage")
                    $("#lastMessage").detach();
                    $("<div id=\"lastMessage\"></div>").insertAfter(`#${id}`)

                    document.getElementById("lastMessage").scrollIntoView();
                    $("#messageInput").val("")

                },
                cache: false,
                contentType: false,
            })
        }
        sendTimeCount++;
    }

    $("#sendMessage").click(send)


             $("#login").html(`<div class="btn-group" style="float:right">
  <button type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" aria="true" aria-expanded="false">
    Hello, ${username}!
  </button>
  <div class="dropdown-menu dropdown-menu-right">
    <button id="ddChatsButton" class="dropdown-item" type="button">your chats</button>
    <button id="ddPasswordButton" class="dropdown-item" type="button">change password</button>
    <button id="ddLogOutButton" class="dropdown-item" type="button">Log out</button>
  </div>
</div>`)

$(document).on('keypress',function(e) {
    if(e.which == 13) {
        send()
    }
});
const next_chat = $("#next_chat")
const send_message = $("#send_message")
const message_input = $("input#message")
const texts = $(".chat .texts")
const info = $('#info')
const loading = $('.loading')
const disconnected = $('.disconnected')

let is_disconected = false

window.onbeforeunload = () => {
    $.ajax({url:'/disconnect/'})
}

$(document).on("keydown", (e)=>{
    if(e.code == "Escape"){
        next_chat.click()
    }
})


function addMessage(from, text){
    const p = document.createElement('p')
    const span_from = document.createElement('span')
    const span_message = document.createElement('span')
    span_from.classList.add('from') 
    span_from.classList.add(`c${from + 1}`)
    span_from.innerHTML = "- "
    
    span_message.classList.add('message')
    span_message.innerHTML = text

    p.appendChild(span_from)
    p.appendChild(span_message)

    texts.append(p)
    texts.animate({scrollTop: texts[0].scrollHeight}, 1)
    $('body, html').animate({screenTop: $(document).scrollHeight}, 1)

}

function chatInfo(){
    $.ajax({url:'/chat_info/'}).then(res=>{
        console.log(res)
        is_disconected = !res.two_users === true

        if(is_disconected){
            disconnected.css("display", "inline-block")
            message_input.prop( "disabled", true )
        }
        else{
            loading.css("display", "none")
            message_input.prop( "disabled", false )
            disconnected.css("display","none")
        }

    })
}

message_input.on("keydown", (e)=>{
    if(e.code === "Enter"){
        e.preventDefault(e)
        send_message.click()
    }
})

next_chat.click((e)=>{
    e.preventDefault()
    disconnected.css({"diplay":"inline-block"})
    if(is_disconected){
        $.ajax({url: '/next_chat/'})
        disconnected.css({"diplay":"none"})
        loading.css("display", "inline-block")
        texts.html("")
        messages_length = 0
        messages = []
    }
    else{
        $.ajax({url: '/disconnect/'})
        disconnected.css({"diplay":"inline-block"})
    }
    
})

send_message.click((e)=>{
    e.preventDefault()
    $.ajax({
        url: '/message/',
        method: 'POST',
        data: JSON.stringify({
            text: message_input.val()
        })

    })
    message_input.val("")
    message_input.focus()
})

let messages_length = 0
let messages = []
function load_messages(){
    chatInfo()

    if(!is_disconected)
    $.ajax({
        url: '/messages/',
    }).then(res=>{
        if(Object.keys(res).length !== messages_length){
            messages_length = Object.keys(res).length
            for(let i = 0; i < messages_length; i++){
                if(messages.includes(i)){
                    continue
                }
                addMessage(res[i].from, res[i].text)
                messages.push(i)
            }
        }
    })
}

setInterval(load_messages, 1000)

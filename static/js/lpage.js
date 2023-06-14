var messageArray = ["Charity Insights Canada Project", "Inform", "Build", "Strengthen"];
var textPosition = 0;
var speed = 100;


typewriter = () => {
    document.querySelector('#message').innerHTML = messageArray[0].substring(0, textPosition)
    document.querySelector("#message-dynamic").innerHTML = messageArray[1].substring(0, textPosition) + messageArray[2].substring(0, textPosition) + messageArray[3].substring(0, textPosition) + "<span>\u25ae</span>";


    if (textPosition++ != messageArray.length)
        setTimeout(typewriter, speed);
}



window.addEventListener("load", typewriter);

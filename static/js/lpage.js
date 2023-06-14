var messageArray = ["Charity Insights Canada Project", "Inform", "Build", "Strengthen"];
var textPosition = 0;
var speed = 200;


typewriter = () => {
    document.querySelector('#message').innerHTML = messageArray[0].substring(0, textPosition);
    document.querySelector("#message-dynamic").innerHTML = messageArray[1].substring(0, textPosition) + "<span>\uFF0E</span>" + messageArray[2].substring(0, textPosition) + "<span>\uFF0E</span>" + messageArray[3].substring(0, textPosition) + "<span>\u25ae</span>";


    if (textPosition++ != messageArray.length[0])
        setTimeout(typewriter, speed);
    if (textPosition++ != messageArray.length[1])
        setTimeout(typewriter, speed);
    if (textPosition++ != messageArray.length[2])
        setTimeout(typewriter, speed);
    if (textPosition++ != messageArray.length[3])
        setTimeout(typewriter, speed);
}



window.addEventListener("load", typewriter);

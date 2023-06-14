var messageArray = ["Charity Insights Canada Project", "Inform", "Build", "Strengthen"];
var textPosition = 0;
var speed = 100;
var speedNew = 200;
var cursorVisible = true;

typewriter = () => {
    if (textPosition < messageArray[0].length) {
        document.querySelector('#message').innerHTML += messageArray[0][textPosition];
        textPosition++;
    } else {
        if (cursorVisible) {
            document.querySelector('.cursor').style.opacity = 0;
            cursorVisible = false;
        } else {
            document.querySelector('.cursor').style.opacity = 1;
            cursorVisible = true;
        }
    }

    if (textPosition < messageArray[0].length) {
        setTimeout(typewriter, speed);
    } else if (textPosition === messageArray[0].length) {
        setTimeout(displayRemainingText, speedNew);
    }
}

displayRemainingText = () => {
    var remainingText = messageArray.slice(1).join("<span>\uFF0E</span>");
    document.querySelector('#message-dynamic').innerHTML = remainingText + "<span>\uFF0E</span>" + "<span class='cursor'></span>";
}

window.addEventListener("load", typewriter);

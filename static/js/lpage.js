var messageArray = ["FILTER REPORTS USING A DATE OR THEME "];
var textPosition = 0;
var speed = 100;
var speedNew = 200;
var cursorVisible = true;

typewriter = () => {
    if (textPosition < messageArray[0].length) {
        document.querySelector('#message').innerHTML += messageArray[0][textPosition];
        textPosition++;
    }

    if (textPosition < messageArray[0].length) {
        setTimeout(typewriter, speed);
    }
}


window.addEventListener("load", typewriter);

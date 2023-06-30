const messageArray = [gettext("FILTER REPORTS USING A DATE OR THEME ")];
let textPosition = 0;
const speed = 100;
const speedNew = 200;
const cursorVisible = true;

const typewriter = () => {
    if (textPosition < messageArray[0].length) {
        document.querySelector('#message').innerHTML += messageArray[0][textPosition];
        textPosition++;
    }

    if (textPosition < messageArray[0].length) {
        setTimeout(typewriter, speed);
    }
}

const screenloader = () => {
    const loader = document.querySelector('.loader');

    loader.classList.add("loader-hidden");

    loader.addEventListener('transitionend', () => {
        document.removeChild("loader")

    })
};

window.addEventListener("load", function () {
    typewriter();

    // screenloader();


});

// var messageArray = ["Charity Insights Canada Project"];
// var textPosition = 0;
// var speed = 100;


// typewriter = () => {
//     document.querySelector('#message').innerHTML = messageArray[0].substring(0, textPosition) + "<span>\u25ae</span>";

//     if (textPosition++ != messageArray[0].length)
//         setTimeout(typewriter, speed);
// }

const carouselText = [
    { text: "Inform", color: "red" },
    { text: "Build", color: "red" },
    { text: "Strengthen", color: "red" }
]

$(document).ready(async function () {
    carousel(carouselText, "#feature-text")
});

async function typeSentence(sentence, eleRef, delay = 100) {
    const letters = sentence.split("");
    let i = 0;
    while (i < letters.length) {
        await waitForMs(delay);
        $(eleRef).append(letters[i]);
        i++
    }
    return;
}

async function deleteSentence(eleRef) {
    const sentence = $(eleRef).html();
    const letters = sentence.split("");
    let i = 0;
    while (letters.length > 0) {
        await waitForMs(100);
        letters.pop();
        $(eleRef).html(letters.join(""));
    }
}

async function carousel(carouselList, eleRef) {
    var i = 0;
    while (true) {
        updateFontColor(eleRef, carouselList[i].color)
        await typeSentence(carouselList[i].text, eleRef);
        await waitForMs(1500);
        await deleteSentence(eleRef);
        await waitForMs(500);
        i++
        if (i >= carouselList.length) { i = 0; }
    }
}

function updateFontColor(eleRef, color) {
    $(eleRef).css('color', color);
}

function waitForMs(ms) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

window.addEventListener("load", typewriter);

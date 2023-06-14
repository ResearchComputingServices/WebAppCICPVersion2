// const carouselText = [
//     { text: "Inform", color: "red" },
//     { text: "Build", color: "red" },
//     { text: "Strengthen", color: "red" }
// ]

// async function carousel(carouselList, eleRef) {
//     var i = 0;
//     while (true) {
//         updateFontColor(eleRef, carouselList[i].color)
//         await typeSentence(carouselList[i].text, eleRef);
//         await waitForMs(1500);
//         await deleteSentence(eleRef);
//         await waitForMs(500);
//         i++
//         if (i >= carouselList.length) { i = 0; }
//     }
// }

// function updateFontColor(eleRef, color) {
//     $(eleRef).css('color', color);
// }

var messageArray = ["Charity Insights Canada Project"];
var textPosition = 0;
var speed = 100;


typewriter = () => {
    document.querySelector('#message').innerHTML = messageArray[0].substring(0, textPosition) + "<span>\u25ae</span>";

    if (textPosition++ != messageArray[0].length)
        setTimeout(typewriter, speed);
}

window.addEventListener("load", typewriter);

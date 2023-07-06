const messageArray = ["FILTER REPORTS USING A DATE OR THEME "];
let textPosition = 0;
const speed = 100;
const speedNew = 200;
const cursorVisible = true;

const typewriter = () => {
    if (textPosition < messageArray[0].length) {
        document.querySelector('#message').innerHTML += messageArray[0][textPosition];
        textPosition++;
        if (textPosition < messageArray[0].length) {
            setTimeout(typewriter, speed);
        }
    }
};

const screenloader = () => {
    const loader = document.querySelector('.loader');

    loader.classList.add("loader-hidden");

    loader.addEventListener('transitionend', () => {
        loader.parentNode.removeChild(loader);
    });
};

window.addEventListener("load", function () {
    typewriter();
    // screenloader();
});

document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById("myForm");
    form.onsubmit = validateDate;

    function validateDate(event) {
        var dateInput = document.forms["myForm"]["date"].value;
        var themeInputs = document.querySelectorAll('input[name="theme"]:checked');

        if (dateInput === "" && themeInputs.length === 0) {
            alert("Please select a date and a theme to search.");
            event.preventDefault();  // Prevent the form submission
        } else if (dateInput === "") {
            alert("Please select a date from the calendar to search.");
            event.preventDefault();  // Prevent the form submission
        } else if (themeInputs.length === 0) {
            alert("Please select a theme to search.");
            event.preventDefault();  // Prevent the form submission
        }
    }
});


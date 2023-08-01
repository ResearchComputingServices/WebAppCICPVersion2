const messageArray = [gettext("FILTER REPORTS USING A DATE OR THEME")];
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

document.onreadystatechange = function () {
    if (document.readyState !== "complete") {
        document.querySelector("body").style.visibility = "hidden";
        document.querySelector("#loader").style.visibility = "visible";
    } else {
        typewriter();
        document.querySelector("#loader").style.display = "none";
        document.querySelector("body").style.visibility = "visible";
    }
};



window.addEventListener("load", function () {
    // All page content (including images) has been loaded, do any additional setup here
    // You can also call your screenloader() function here if needed
});

document.addEventListener('DOMContentLoaded', function () {
    var dateForm = document.getElementById("dateForm");
    var themeForm = document.getElementById("themeForm");

    dateForm.addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent the form submission

        var dateInput = dateForm.querySelector('input[name="report_date"]').value;

        if (dateInput === "") {
            alert("Please select a date from the calendar to search.");
        } else {
            // If validation passes, submit the date form
            dateForm.submit();
        }
    });

    themeForm.addEventListener("submit", function (event) {
        event.preventDefault();  // Prevent the form submission

        var themeInputs = themeForm.querySelectorAll('input[name="theme"]:checked');

        if (themeInputs.length === 0) {
            alert("Please select a theme to search.");
        } else {
            // If validation passes, submit the theme form
            themeForm.submit();
        }
    });
});

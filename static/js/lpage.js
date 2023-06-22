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

window.addEventListener("load", function () {
    typewriter();

    // Get the selected date input element
    const selectedDateInput = document.getElementById('selected-date');

    // Add an event listener to the input field to capture changes
    selectedDateInput.addEventListener('change', function () {
        // Get the selected date value
        const selectedDate = selectedDateInput.value;
        // Update the cookie with the selected date
        document.cookie = `selected_date=${selectedDate}; path=/`;
    });
});




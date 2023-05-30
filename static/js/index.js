$(document).ready(function () {


    function toggleblackbox() {
        // get the clock
        var myBox = document.getElementById('blackbox');

        // get the current value of the clock's display property
        var displaySetting = myBox.style.display;

        // also get the clock button, so we can change what it says
        var boxButton = document.getElementById('boxButton');

        // now toggle the clock and the button text, depending on current state
        if (displaySetting == 'block') {
            // clock is visible. hide it
            myBox.style.display = 'none';
            // change button text
            boxButton.innerHTML = 'Show Box';
        }
        else {
            // clock is hidden. show it
            myBox.style.display = 'block';
            // change button text
            boxButton.innerHTML = 'Hide Box';
        }
    }

});


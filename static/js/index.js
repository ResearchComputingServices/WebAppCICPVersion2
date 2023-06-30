window.addEventListener("load", () => {
    const loader = document.querySelector('.loader');

    loader.classList.add("loader-hidden");

    loader.addEventListener('transitionend', () => {
        document.removeChild("loader")

    })
}

)
function toggleblackbox(e) {

    e.preventDefault();
    // get the clock
    var myBox = document.getElementById('blackbox');

    // get the current value of the clock's display property
    var displaySetting = myBox.style.display;


    // now toggle the clock and the button text, depending on current state
    if (displaySetting == 'block') {
        // clock is visible. hide it
        myBox.style.display = 'none';
    }
    else {
        // clock is hidden. show it
        myBox.style.display = 'block';
    }
};

function showDiv() {
    document.getElementById('main').style.display = 'none';
    document.getElementById('loader').style.display = 'block';

    setTimeout(function () {
        document.getElementById('loader').style.display = 'none';
        document.getElementById('main').style.display = 'block';
    }, 60);

};
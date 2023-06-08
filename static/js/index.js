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
}

const carousel = document.querySelector('.carousel');
const carouselItems = document.querySelectorAll('.carousel-item');
let currentIndex = 0;

console.log("carouselItems.length ", carouselItems.length)
function showGraph(index) {
    carousel.style.transform = `translateX(-${index * 100}%)`;
}

// Handle next button click
document.getElementById('next-button').addEventListener('click', function () {
    if (currentIndex < carouselItems.length - 1) {
        currentIndex++;
        showGraph(currentIndex);
    }
});

// Handle previous button click
document.getElementById('prev-button').addEventListener('click', function () {
    if (currentIndex > 0) {
        currentIndex--;
        showGraph(currentIndex);
    }
});



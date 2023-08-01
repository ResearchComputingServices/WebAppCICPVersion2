document.onreadystatechange = function () {
    if (document.readyState !== "complete") {
        document.querySelector("body").style.visibility = "hidden";
        document.querySelector("#loader").style.visibility = "visible";
    } else {
        document.querySelector("#loader").style.display = "none";
        document.querySelector("body").style.visibility = "visible";
    }
};

document.addEventListener('DOMContentLoaded', function () {
    new Splide('#image-slider').mount();
});

function openNav() {
    document.getElementById("sidebar").style.width = "100%";
}

function closeNav() {
    document.getElementById("sidebar").style.width = "0";

}


// Function to handle the click event
function checkFilters(event) {
    const url = window.location.href;
    const containsProvince = url.includes("province");
    const containsSize = url.includes("size");
    const containsAge = url.includes("age");

    if (!(containsProvince || containsSize || containsAge)) {
        // Display an alert
        alert("Please select a filter");
        // Prevent default behavior of the link (don't follow the link)
        event.preventDefault();

    } else {
        // Follow the URL defined in urls.py
        window.location.href = url;
    }
}

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


function checkFilters(event) {
    const form = document.querySelector('form'); // Get the form element
    const inputs = form.querySelectorAll('input[type="text"], input[type="date"], input[type="checkbox"],input[type="radio"],select');

    // Check if any input field is filled
    const isFormFilled = [...inputs].some(input => {
        if (input.type === 'checkbox') {
            return input.checked;
        } else {
            return input.value.trim() !== '';
        }
    });

    if (!isFormFilled) {
        // Display an alert
        alert("Please select a filter to search.");
        // Prevent the form submission
        event.preventDefault();
    } else {
        // The form is filled, proceed with the search (form submission)
        // If the form submission is allowed, the default behavior will be followed.
        form.submit();
    }
}



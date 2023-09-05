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
        if (input.type === 'checkbox' || input.type === 'radio') {
            return input.checked;
        } else {
            return input.value.trim() !== '';
        }
    });

    if (!isFormFilled) {
        // Display an alert
        alert(gettext("Please select a filter to search."));
        // Prevent the form submission
        event.preventDefault();
    } else {
        // The form is filled, proceed with the search (form submission)
        // If the form submission is allowed, the default behavior will be followed.
        form.submit();
    }
}

// Assuming you have the total number of subfolders available as 'totalSubfolders'
// and an array 'subfolderData' containing subfolder information

const itemsPerPage = 1; // Number of images to display per page

// Calculate the total number of pages based on subfolders
const totalPages = Math.ceil(totalSubfolders / itemsPerPage);

// Function to generate the HTML for the pagination buttons
function generatePaginationButtons() {
    const paginationButtons = document.getElementById('pagination-buttons');
    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.innerText = i;
        button.addEventListener('click', () => showPage(i));
        paginationButtons.appendChild(button);
    }
}

// Function to display images for a specific page
function showPage(pageNumber) {
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;

    const list = document.querySelector('.splide__list');
    list.innerHTML = ''; // Clear the list

    for (let i = startIndex; i < endIndex && i < totalSubfolders; i++) {
        const subfolder = subfolderData[i];
        const listItem = document.createElement('li');
        listItem.className = 'splide__slide';
        listItem.innerHTML = `
      <h4 id="heading">${subfolder.name}</h4>
      <ul>
        ${subfolder.images.map(imageUrl => `<li><img src="${imageUrl}" alt="Image"></li>`).join('')}
      </ul>
    `;
        list.appendChild(listItem);
    }
}

// Initialize the pagination
generatePaginationButtons();
showPage(1); // Show the first page by default




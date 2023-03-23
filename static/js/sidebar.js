// // Get the sidebar toggle button and sidebar section
// const sidebarToggle = document.getElementById('sidebar-toggle');
// const sidebar = document.querySelector('.sidebar');
// const sidebarLinks = document.querySelectorAll('.sidebar a');

// // Add an event listener to the sidebar toggle button
// sidebarToggle.addEventListener('click', () => {
//     // Toggle the "active" class on the sidebar
//     sidebar.classList.toggle('active');
//     document.getElementsByClassName('sidebar active')




//     // Change the button text depending on the sidebar state
//     if (sidebar.classList.contains('active')) {
//         sidebarToggle.textContent = '✕ Close';
//         document.getElementById("sidebar").style.width = "100%";

//     } else {
//         sidebarToggle.textContent = '☰ Filters';
//         document.getElementById("sidebar").style.width = "0%";

//     }
// });


function openNav() {
    document.getElementById("sidebar").style.width = "100%";
}

function closeNav() {
    document.getElementById("sidebar").style.width = "0";
}
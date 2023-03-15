// Get the sidebar toggle button and sidebar section
const sidebarToggle = document.getElementById('sidebar-toggle');
const sidebar = document.querySelector('.sidebar');
const sidebarLinks = document.querySelectorAll('.sidebar a');

// Add an event listener to the sidebar toggle button
sidebarToggle.addEventListener('click', () => {
    // Toggle the "active" class on the sidebar
    sidebar.classList.toggle('active');

    // Change the button text depending on the sidebar state
    if (sidebar.classList.contains('active')) {
        sidebarToggle.textContent = '✕ Close';
    } else {
        sidebarToggle.textContent = '☰ Filters';
    }
});

// // Add a resize event listener to show/hide the sidebar and button
// window.addEventListener('resize', () => {
//     if (window.innerWidth <= 768) {
//         sidebar.style.display = 'none';
//         sidebarToggle.style.display = 'block';
//     } else {
//         sidebar.style.display = 'block';
//         sidebarToggle.style.display = 'none';
//     }
// });

// // Trigger the resize event on page load
// window.dispatchEvent(new Event('resize'));

// // Add an event listener to the sidebar links
// sidebarLinks.forEach(link => {
//     link.addEventListener('click', () => {
//         // Hide the sidebar for small screens when a link is clicked
//         if (window.innerWidth <= 768) {
//             sidebar.classList.remove('active');
//             sidebarToggle.textContent = '☰ Filters';
//         }
//     });
// });

// // Show the sidebar when the toggle button is clicked on large screens
// sidebarToggle.addEventListener('click', () => {
//     if (window.innerWidth > 768) {
//         sidebar.classList.add('active');
//     }
// });
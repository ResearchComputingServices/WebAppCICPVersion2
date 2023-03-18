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
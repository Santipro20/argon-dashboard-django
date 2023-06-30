// Obtiene una referencia a la barra lateral
const sidebar = document.getElementById('sidenav-main');

// Obtiene una referencia al botón de toggle
const sidebarToggleButton = document.querySelector('.navbar-toggler');

// Agrega un evento click al botón de toggle
sidebarToggleButton.addEventListener('click', toggleSidebar);

// Función para contraer o expandir la barra lateral
function toggleSidebar() {
  sidebar.classList.toggle('collapsed');
}
function showButton() {
    const button = document.getElementById("navbar-dropdown-calendar");
    button.style.display = "block";
}

function hideButton() {
    const button = document.getElementById("navbar-dropdown-calendar");
    button.style.display = "none";
}

function init() {
    // Obtener la URL actual
    const currentURL = window.location.pathname;

    if (currentURL === '/app/index2/' ) {
        // Mostrar el botón para ciertas páginas
        showButton();
    } else {
        // Ocultar el botón para otras páginas
        hideButton();
    }
}

// Llamar a la función init al cargar la página
init();

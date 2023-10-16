function showButton() {
    const button = document.getElementById("navbar-dropdown-calendar");
    button.style.display = "block";
  }
  
  function hideButton() {
    const button = document.getElementById("navbar-dropdown-calendar");
    button.style.display = "none";
  }
  
  function init() {
    function updateButtonVisibility() {
      // Obtener la URL actual
      const currentURL = window.location.pathname;
  
      if (currentURL.startsWith('/app/index2/')) {
        // Mostrar el botón para ciertas páginas
        showButton();
      } else {
        // Ocultar el botón para otras páginas
        hideButton();
      }
    }
  
    // Llamar a la función updateButtonVisibility al cargar la página
    updateButtonVisibility();
  
    // Escuchar cambios en la URL y actualizar el botón en consecuencia
    window.addEventListener('popstate', updateButtonVisibility);
  }
  
  init();
  
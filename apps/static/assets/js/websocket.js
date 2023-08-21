// Configuración del WebSocket
var socket = new WebSocket("ws://127.0.0.1:8000/ws/co2_updates/");

// Escuchar eventos del WebSocket
socket.addEventListener("open", function (event) {
  console.log("Connexion WebSocket établie");
});

socket.addEventListener("message", function (event) {
  var data = JSON.parse(event.data);
  updateValues(data.updated_data); // Actualizar los valores en las tarjetas usando los datos recibidos
});

// Función para enviar la fecha seleccionada al servidor a través de WebSockets
function envoyerDateSelectionnee(selectedDate) {
  socket.send(JSON.stringify({ type: "date", value: selectedDate }));
}

// Exportar el objeto socket y la función envoyerDateSelectionnee
window.socket = socket
window.envoyerDateSelectionnee = envoyerDateSelectionnee;

// Función para inicializar y actualizar valores antes del WebSocket
function updateValues(updatedData) {
  document.getElementById("number_of_deliveries").innerHTML = updatedData.number_of_deliveries;
  document.getElementById("porcentage_km").innerHTML = updatedData.porcentage_km + "%";
  document.getElementById("value_km").innerHTML = "Km économisé soit " + updatedData.value_km + "h";
  document.getElementById("value_h").innerHTML = "Temps économisé soit " + updatedData.value_h + "h";
  document.getElementById("porcentage_h").innerHTML = updatedData.porcentage_h + "%";
  document.getElementById("value_e").innerHTML = "CO2 économisé soit " + updatedData.value_e + " kg";
  document.getElementById("porcentage_e").innerHTML = updatedData.porcentage_e + "%";
}

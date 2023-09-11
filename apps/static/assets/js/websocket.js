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
  document.getElementById("recharge_portable").innerHTML = updatedData.recharge_portable;
  document.getElementById("recharge_ordina").innerHTML = updatedData.recharge_ordina;
  document.getElementById("arbes_hec").innerHTML = updatedData.arbes_hec;
  document.getElementById("train_voya").innerHTML = updatedData.train_voya;
  document.getElementById("diesel_E10").innerHTML = updatedData.diesel_E10;
  document.getElementById("uber_livra").innerHTML = updatedData.uber_livra;
  document.getElementById("feuilles_print").innerHTML = updatedData.feuilles_print;
  document.getElementById("emails").innerHTML = updatedData.emails;
  document.getElementById("travailleur_moyen").innerHTML = updatedData.travailleur_moyen;
  document.getElementById("water_bo").innerHTML = updatedData.water_bo;
  document.getElementById("pain_tranches").innerHTML = updatedData.pain_tranches;
  document.getElementById("portion_fromage").innerHTML = updatedData.portion_fromage;
}

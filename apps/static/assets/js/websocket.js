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

function sendFiltersDataToServer(selectedDate, selectedCity, selectedPeriod) {
  // Get the 'nuevonombre' from the URL
  var newuser = window.newuserf;
  var new_user = window.newuserh;

  // Create an object with the selected date, cities, and 'nuevonombre'
  const messageData = {
    type: "filters",
    selected_date: selectedDate,
    selected_city: selectedCity,
    newuser: newuser || null,
    new_user: new_user || null,
    selected_period: selectedPeriod, 
  };

  console.log("Mensaje enviado al servidor:", messageData);

  // Convert the object to JSON and send it to the WebSocket server
  const messageJSON = JSON.stringify(messageData);
  socket.send(messageJSON);
}
// Exportar el objeto socket y la función envoyerDateSelectionnee
window.socket = socket
window.sendFiltersDataToServer = sendFiltersDataToServer;

// Función para inicializar y actualizar valores antes del WebSocket
function updateValues(updatedData) {
  // Function to get an element by its ID and check its existence
  function getElementByIdSafe(id) {
    var element = document.getElementById(id);
    if (element) {
      return element;
    } else {
      console.error("The element with ID '" + id + "' was not found on the page.");
      return null;
    }
  }

  var numberOfDeliveriesElement = getElementByIdSafe("number_of_deliveries");
  if (numberOfDeliveriesElement) {
    numberOfDeliveriesElement.innerHTML = updatedData.number_of_deliveries;
  }
  var porcentageKmElement = getElementByIdSafe("porcentage_km");
  if (porcentageKmElement) {
    porcentageKmElement.innerHTML = updatedData.porcentage_km + "%";
  }
  var distanceKmElement = getElementByIdSafe("value_km");
  if (distanceKmElement) {
    distanceKmElement.innerHTML = "Distance économisé soit " + updatedData.value_km + "km";
  }
  var tempsecoElement = getElementByIdSafe("value_h");
  if (tempsecoElement) {
    tempsecoElement.innerHTML = "Temps économisé soit " + updatedData.value_h + "h";
  }
  var tempsporElement = getElementByIdSafe("porcentage_h");
  if (tempsporElement) {
    tempsporElement.innerHTML = updatedData.porcentage_h + "%";
  }
  var co2Element = getElementByIdSafe("value_e");
  if (co2Element) {
    co2Element.innerHTML = "CO2 économisé soit " + updatedData.value_e + " kg";
  }
  var co2porElement = getElementByIdSafe("porcentage_e");
  if (co2porElement) {
    co2porElement.innerHTML = updatedData.porcentage_e + "%";
  }
  var reportElement = getElementByIdSafe("recharge_portable");
  if (reportElement) {
    reportElement.innerHTML = updatedData.recharge_portable;
  }
  var reordElement = getElementByIdSafe("recharge_ordina");
  if (reordElement) {
    reordElement.innerHTML = updatedData.recharge_ordina;
  }
  var arbesElement = getElementByIdSafe("arbes_hec");
  if (arbesElement) {
    arbesElement.innerHTML = updatedData.arbes_hec;
  }
  var trainElement = getElementByIdSafe("train_voya");
  if (trainElement) {
    trainElement.innerHTML = updatedData.train_voya;
  }
  var dieselElement = getElementByIdSafe("diesel_E10");
  if (dieselElement) {
    dieselElement.innerHTML = updatedData.diesel_E10;
  }
  var uberElement = getElementByIdSafe("uber_livra");
  if (uberElement) {
    uberElement.innerHTML = updatedData.uber_livra;
  }
  var feuillesElement = getElementByIdSafe("feuilles_print");
  if (feuillesElement) {
    feuillesElement.innerHTML = updatedData.feuilles_print;
  }
  var emailsElement = getElementByIdSafe("emails");
  if (emailsElement) {
    emailsElement.innerHTML = updatedData.emails;
  }
  var travailleurElement = getElementByIdSafe("travailleur_moyen");
  if (travailleurElement) {
    travailleurElement.innerHTML = updatedData.travailleur_moyen;
  }
  var waterElement = getElementByIdSafe("water_bo");
  if (waterElement) {
    waterElement.innerHTML = updatedData.water_bo;
  }
  var painElement = getElementByIdSafe("pain_tranches");
  if (painElement) {
    painElement.innerHTML = updatedData.pain_tranches;
  }
  var fromageElement = getElementByIdSafe("portion_fromage");
  if (fromageElement) {
    fromageElement.innerHTML = updatedData.portion_fromage;
  }
  var sc_vulElement = getElementByIdSafe("sc_vul");
  if (sc_vulElement) {
    sc_vulElement.innerHTML = "VUL : " + updatedData.sc_vul + " m&sup2";
  }
  var sc_dekiElement = getElementByIdSafe("sc_deki");
  if (sc_dekiElement) {
    sc_dekiElement.innerHTML = "Deki : " + updatedData.sc_deki + " m&sup2";
  }
  var sc_ecoElement = getElementByIdSafe("sc_eco");
  if (sc_ecoElement) {
    sc_ecoElement.innerHTML = "Économie : " + updatedData.sc_eco + " m&sup2";
  }
  var livra_KPIElement = getElementByIdSafe("livra_KPI");
  if (livra_KPIElement) {
    livra_KPIElement.innerHTML = updatedData.livra_KPI + " Kg";
  }
  var km_KPIElement = getElementByIdSafe("km_KPI");
  if (km_KPIElement) {
    km_KPIElement.innerHTML = updatedData.km_KPI + " Kg";
  }
  var coli_KPIElement = getElementByIdSafe("coli_KPI");
  if (coli_KPIElement) {
    coli_KPIElement.innerHTML = updatedData.coli_KPI + " Kg";
  }
  var poids_KPIElement = getElementByIdSafe("poids_KPI");
  if (poids_KPIElement) {
    poids_KPIElement.innerHTML = updatedData.poids_KPI + " G";
  }
  var m2_KPIElement = getElementByIdSafe("m2_KPI");
  if (m2_KPIElement) {
    m2_KPIElement.innerHTML = updatedData.m2_KPI + " G";
  }
  var tempsElement = getElementByIdSafe("temps");
  if (tempsElement) {
    tempsElement.innerHTML = updatedData.temps + " Kg";
  }
  var number_of_deliveries_1Element = getElementByIdSafe("number_of_deliveries_1");
  if (number_of_deliveries_1Element) {
    number_of_deliveries_1Element.innerHTML = updatedData.number_of_deliveries;
  }
  var colisElement = getElementByIdSafe("colis");
  if (colisElement) {
    colisElement.innerHTML = updatedData.colis;
  }
  var kilosElement = getElementByIdSafe("kilos");
  if (kilosElement) {
    kilosElement.innerHTML = updatedData.kilos + " Kg";
  }
  var distance_parElement = getElementByIdSafe("distance_par");
  if (distance_parElement) {
    distance_parElement.innerHTML = updatedData.distance_par + " km";
  }
  var numElement = getElementByIdSafe("num");
  if (numElement) {
    numElement.innerHTML = updatedData.num;
  }
  var num1Element = getElementByIdSafe("num1");
  if (num1Element) {
    num1Element.innerHTML = updatedData.num1;
  }
  var num2Element = getElementByIdSafe("num2");
  if (num2Element) {
    num2Element.innerHTML = updatedData.num2;
  }
  var num3Element = getElementByIdSafe("num3");
  if (num3Element) {
    num3Element.innerHTML = updatedData.num3;
  }
  var num4Element = getElementByIdSafe("num4");
  if (num4Element) {
    num4Element.innerHTML = updatedData.num4;
  }

  var value1Element = getElementByIdSafe("value1");
  if (value1Element) {
    value1Element.innerHTML = updatedData.value1 + " km";
  }

  var value2Element = getElementByIdSafe("value2");
  if (value2Element) {
    value2Element.innerHTML = updatedData.value2 + " min";
  }

  var value3Element = getElementByIdSafe("value3");
  if (value3Element) {
    value3Element.innerHTML = updatedData.value3 + " kg";
  }

  var value4Element = getElementByIdSafe("value4");
  if (value4Element) {
    value4Element.innerHTML = updatedData.value4 + " #";
  }
}


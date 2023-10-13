'use strict';
//
// Donut graphic
//
$(document).ready(function() {
	var $chart = $('#chart-donut');
	var donutChart = initDonutChart($chart);
	var isActivePage = true;
	let sc_eco = window.sc_eco
	let sc_vul = window.sc_vul 
	let sc_deki = window.sc_deki

	function updateDonutChart() {
		if (isActivePage) {
		  updateDonutChartWithData(donutChart, [sc_vul, sc_deki, sc_eco]);
		}
	  }

	socket.addEventListener("message", function (event) {
		var data = JSON.parse(event.data);
		var updatedData = data.updated_data;
		
		if (isActivePage) {
			sc_eco = updatedData.sc_eco
			sc_vul = updatedData.sc_vul
			sc_deki = updatedData.sc_deki
		

			updateDonutChart();
		}

	  });

	document.addEventListener('visibilitychange', function () {
		isActivePage = document.visibilityState === 'visible';
	});

});

var chartData = {
	labels: ['VUL', 'Deki', 'Économie'],
	datasets: [
	  {
		data: [sc_vul, null, null],
		backgroundColor: ['#E85127', null, null]
	  },
	  {
		data: [null, sc_deki, sc_eco],
		backgroundColor: [null, '#005347', '#C9D200']
	  }
	]
  };
  

function initDonutChart($chart) {
	var chart = new Chart($chart, {
	  type: 'doughnut',
	  data: chartData,
	  options: {
		cutoutPercentage: 40,
		responsive: true,
		tooltips: {
		  callbacks: {
			label: function(tooltipItem, data) {
			  var label = data.labels[tooltipItem.index];
			  var value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];

			  // Only show the tooltip if the value is not null
			  if (value !== null) {
				return label + ': ' + value;
			  } else {
				return '';
			  }
			}
		  }
		}
	  }
	});
	return chart;
  }
  
  

function updateDonutChartWithData(chart, newData) {
	chart.data.datasets[0].data = [newData[0], null, null];
  	chart.data.datasets[1].data = [null, newData[1], newData[2]];
	chart.update()
}
  


'use strict';

$(document).ready(function() {
	// Inicializa el gráfico cuando el documento esté listo
	var $chart = $('#chart-sales-dark');
	var salesChart = initSalesChart($chart);
	var isActivePage = true; 
	let driving = window.driving
	let cycling = window.cycling 
	let deki_vul = window.deki_vul
	let VUL_met = window.VUL_met 
	let VUL_no2 = window.VUL_no2
	let VUL_NOx = window.VUL_NOx
	let VUL_CO = window.VUL_CO 
	let VUL_PM = window.VUL_PM
	let deki_met = window.deki_met 
	let deki_no2 = window.deki_no2
	let deki_NOx = window.deki_NOx
	let deki_CO = window.deki_CO
	let deki_PM = window.deki_PM
	let deki_vul_met = window.deki_vul_met 
	let deki_vul_no2 = window.deki_vul_no2
	let deki_vul_NOx = window.deki_vul_NOx
	let deki_vul_CO = window.deki_vul_CO
	let deki_vul_PM = window.deki_vul_PM
	let socket = window.socket

	function updateChart() {
		if (isActivePage) {
		  salesChart.data.datasets[0].label = 'Émissions de CO2 en kg';
		  salesChart.options.scales.xAxes[0].scaleLabel.labelString = 'Kg de CO2';
		  updateChartWithData(salesChart, [driving, deki_vul, cycling]);
		}
	  }

	socket.addEventListener("message", function (event) {
		var data = JSON.parse(event.data);
		var updatedData = data.updated_data;

		if (isActivePage) {
			driving = updatedData.driving;
			cycling = updatedData.cycling;
			deki_vul = updatedData.deki_vul;
			VUL_met = updatedData.VUL_met;
			VUL_no2 = updatedData.VUL_no2;
			VUL_NOx = updatedData.VUL_NOx;
			VUL_CO = updatedData.VUL_CO;
			VUL_PM = updatedData.VUL_PM;
			deki_met = updatedData.deki_met;
			deki_no2 = updatedData.deki_no2;
			deki_NOx = updatedData.deki_NOx;
			deki_CO = updatedData.deki_CO;
			deki_PM = updatedData.deki_PM;
			deki_vul_met = updatedData.deki_vul_met;
			deki_vul_no2 = updatedData.deki_vul_no2;
			deki_vul_NOx = updatedData.deki_vul_NOx;
			deki_vul_CO = updatedData.deki_vul_CO;
			deki_vul_PM = updatedData.deki_vul_PM;
	  
			updateChart();
		  }

	  });
	
	document.addEventListener('visibilitychange', function () {
		isActivePage = document.visibilityState === 'visible';
	  });

	// Event listeners for button clicks
	$('#co2-button').click(updateChart);
  
	$('#metano-button').click(function() {
	  salesChart.data.datasets[0].label = 'Émissions de CH4 en g';
	  salesChart.options.scales.xAxes[0].scaleLabel.labelString = 'G de CH4';
	  updateChartWithData(salesChart, [VUL_met,deki_vul_met,deki_met]);
	});
  
	$('#contaminante1-button').click(function() {
	  salesChart.data.datasets[0].label = 'Émissions de N20 en g';
	  salesChart.options.scales.xAxes[0].scaleLabel.labelString = 'G de N20';
	  updateChartWithData(salesChart, [VUL_no2,deki_vul_no2, deki_no2]);
	});
  
	$('#contaminante2-button').click(function() {
	  salesChart.data.datasets[0].label = 'Émissions de NOx en Kg';
	  salesChart.options.scales.xAxes[0].scaleLabel.labelString = 'Kg de NOx';
	  updateChartWithData(salesChart, [VUL_NOx,deki_vul_NOx, deki_NOx]);
	});

	$('#contaminante3-button').click(function() {
		salesChart.data.datasets[0].label = 'Émissions de CO en g';
		salesChart.options.scales.xAxes[0].scaleLabel.labelString = 'G de CO';
		updateChartWithData(salesChart, [VUL_CO,deki_vul_CO,deki_CO]);
	  });

	$('#contaminante4-button').click(function() {
		salesChart.data.datasets[0].label = 'Émissions de PM en ppm';
		salesChart.options.scales.xAxes[0].scaleLabel.labelString = 'Ppm de PM';
		updateChartWithData(salesChart, [VUL_PM,deki_vul_PM, deki_PM]);
	});
});
  
  
  // Función para inicializar el gráfico
  function initSalesChart($chart) {
    return new Chart($chart, {
        type: 'horizontalBar',
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: function(value) {
                            return  value ;
                        }
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Kg de CO2' // Nombre del eje X
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Type de véhicule' // Nombre del eje Y
                    }
                }]
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        },
        data: {
            labels: ['VUL thermique', 'VUL électrique', 'Deki'],
            datasets: [{
                label: 'Émissions de CO2 en kg',
                data: [driving, deki_vul, cycling],
                backgroundColor: ['#E85127', '#C9D200', '#005347']
            }]
        }
    });
}

  
  // Función para actualizar los datos del gráfico
  function updateChartWithData(chart, newData) {
	chart.data.datasets[0].data = newData;
	chart.update();
};
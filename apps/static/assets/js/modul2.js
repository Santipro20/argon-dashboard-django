'use strict';

//
// Sales chart
//

let value0 = window.value 
let value1 = window.value1
let value2 = window.value2

    //let socket = window.socket

$(document).ready(function() {
	var $chart = $('#chart-ff');
	var mylineChart = lineChart($chart);
	var isActivePage = true;
  let socket = window.socket

	function updateLineChart() {
		if (isActivePage) {
            mylineChart.options.scales.yAxes[0].scaleLabel.labelString = 'Nombre de livraisons';
		  updateLineChartWithData(mylineChart, value0.map(d => d.y), value0.map(d => d.x));
		}
	  }

	socket.addEventListener("message", function (event) {
		var data = JSON.parse(event.data);
		var updatedData = data.updated_data;
		
        if (isActivePage) {
           
            value0 = JSON.parse(updatedData.value5);
            value1 = JSON.parse(updatedData.value6);
            value2 = JSON.parse(updatedData.value7);
            
            updateLineChart();
        }

	  });

	document.addEventListener('visibilitychange', function () {
		isActivePage = document.visibilityState === 'visible';
	});

    // Event listeners for button clicks
	$('#Livraisons').click(updateLineChart);
  
	$('#Colis').click(function() {
        mylineChart.options.scales.yAxes[0].scaleLabel.labelString = 'Nombre de colis';
	  updateLineChartWithData(mylineChart, value1.map(d => d.y),value1.map(d => d.x));
	});
  
	$('#Poids').click(function() {
        mylineChart.options.scales.yAxes[0].scaleLabel.labelString = 'Kg';
	  updateLineChartWithData(mylineChart, value2.map(d => d.y),value2.map(d => d.x));
	});

});


function lineChart($chart) {
    return new Chart($chart, {
        type: 'line',
        options: {
          scales: {
            yAxes: [{
              gridLines: {
                lineWidth: 1, // Cambiar el ancho de las líneas de la cuadrícula
                color: 'rgba(0, 0, 0, 0.1)', // Cambiar el color de las líneas de la cuadrícula
                zeroLineColor: 'rgba(0, 0, 0, 0.5)' // Cambiar el color de las líneas de la cuadrícula de valor cero
              },scaleLabel: {
                display: true,
                labelString: 'Nombre de livraisons' // Cambia 'Eje Y' al título que desees para el eje y
            },
              ticks: {
                callback: function(value) {
                  if (!(value % 10)) {
                    return value ;
                  }
                }
              }
            }],
            xAxes: [{
                scaleLabel: {
                  display: true,
                  labelString: 'Date' // Cambia 'Eje X' al título que desees para el eje x
                },
              ticks: {
                  maxTicksLimit: 11 
                }
                
              }],
          },
          legend: {
            display: false, // Desactiva la leyenda
          },
          tooltips: {
            callbacks: {
              label: function(item, data) {
                var label = data.datasets[item.datasetIndex].label || '';
                var yLabel = item.yLabel;
                var content = '';
  
                if (data.datasets.length > 1) {
                  content += label;
                }
  
                content +=  yLabel ;
                return content;
              }
            }
          }
        },
        data: {
          labels: value0.map(d => d.x),
          datasets: [{
            label: 'Ligne',
            data:  value0.map(d => d.y),
            borderColor: '#51AB27',
            fill: false, 
          }]
        }
    });
}

function updateLineChartWithData(chart, newData,newLabels) {
    chart.data.datasets[0].data = newData;
    chart.data.labels = newLabels; 
    chart.update();
  }




//
// Bars chart
//

let temps_driving = window.temps_d
let temps_cycling = window.temps_c
let distance_driving = window.distance_d 
let distance_cycling = window.distance_c 

'use strict';

$(document).ready(function() {
	// Inicializa el gráfico cuando el documento esté listo
	var $chart = $('#chart-vertical');
	var salesChart = initSalesChart($chart);
	var isActivePage = true; 
	let socket = window.socket

	function updateChart() {
		if (isActivePage) {
		  salesChart.data.datasets[0].label = 'Temps en heures';
		  salesChart.options.scales.xAxes[0].scaleLabel.labelString = 'Hours';
		  updateChartWithData(salesChart, [temps_driving,temps_cycling]);
		}
	  }

	socket.addEventListener("message", function (event) {
		var data = JSON.parse(event.data);
		var updatedData = data.updated_data;

		if (isActivePage) {
			temps_driving = updatedData.time_d;
            temps_cycling = updatedData.time_c;
            distance_driving = updatedData.distance_d;
            distance_cycling = updatedData.distance_c;
			updateChart();
		  }

	  });
	
	document.addEventListener('visibilitychange', function () {
		isActivePage = document.visibilityState === 'visible';
	  });

	// Event listeners for button clicks
	$('#Temps').click(updateChart);
  
	$('#Distance').click(function() {
	  salesChart.data.datasets[0].label = 'Distance en km';
	  salesChart.options.scales.xAxes[0].scaleLabel.labelString = 'Km';
	  updateChartWithData(salesChart, [distance_driving,distance_cycling]);
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
                        labelString: 'Hours' // Nombre del eje X
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
            labels: ['VUL thermique', 'Deki'],
            datasets: [{
                label: 'Temps en heures',
                data: [temps_driving, temps_cycling],
                backgroundColor: ['#E85127', '#005347']
            }]
        }
    });
}

  
  // Función para actualizar los datos del gráfico
  function updateChartWithData(chart, newData) {
	chart.data.datasets[0].data = newData;
	chart.update();
};


'use strict';

//
// pie graphic
//
let days_week = window.week 
$(document).ready(function() {
	var $chart = $('#chart-donut');
	var pieChart = initPieChart($chart);
	var isActivePage = true;
    let socket = window.socket
    


	function updatePieChart() {
		if (isActivePage) {
		  updatePieChartWithData(pieChart ,days_week.map(d => d.y), days_week.map(d => d.x) );
		}
	  }

	socket.addEventListener("message", function (event) {
		var data = JSON.parse(event.data);
		var updatedData = data.updated_data;
		
		if (isActivePage) {
			days_week = JSON.parse(updatedData.days_week)
            console.log(days_week)
		

			updatePieChart();
		}

	  });

	document.addEventListener('visibilitychange', function () {
		isActivePage = document.visibilityState === 'visible';
	});

});


  

function initPieChart($chart) {
	var chart = new Chart($chart, {
	  type: 'pie',
	  data:  {
        labels: days_week.map(d => d.x),
        datasets: [
          {
            data: days_week.map(d => d.y),
            backgroundColor: ['#1D1D1B','#E85127','#005347', '#C9D200','#32D21B','#57AB27' ]
          }
        ]
      },
	  options: {
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
		}, legend: {
            display: true,
            position: 'right',
            labels: {
              generateLabels: function(chart) {
                var data = chart.data;
                if (data.labels.length && data.datasets.length) {
                  return data.labels.map(function(label, i) {
                    var value = data.datasets[0].data[i];
                    return {
                      text: label + ': ' + value,
                      fillStyle: data.datasets[0].backgroundColor[i],
                      hidden: isNaN(value),
                      index: i,
                      lineWidth: 0
                    };
                  });
                }
                return [];
              }
            }
          }, elements: {
            arc: {
              borderWidth: 0 
            }
          }
	  }
	});
	return chart;
  }
  
const fixedColors = ['#1D1D1B', '#E85127', '#005347', '#C9D200', '#32D21B', '#57AB27'];


function updatePieChartWithData(chart, newData,newLabels) {
    chart.data.datasets[0].data = newData;
    chart.data.labels = newLabels; 
    chart.data.datasets[0].backgroundColor = fixedColors.slice(0, newData.length);
    chart.update();
}

//
// Bars chart
//

let j_0 = window.j_0
let j_1 = window.j_1
let j_2 = window.j_2
let k_1 = window.k_1
let k_2 = window.k_2
let k_3 = window.k_3
let k_4 = window.k_4
let k_5 = window.k_5

'use strict';

$(document).ready(function() {
	// Inicializa el gráfico cuando el documento esté listo
	var $chart = $('#chart-u');
	var barChart = initbarChart($chart);
	var isActivePage = true; 
	let socket = window.socket

	function updatebarChart() {
		if (isActivePage) {
		  barChart.options.scales.xAxes[0].scaleLabel.labelString = 'Immédiateté';
		  updatebarChartWithData(barChart, [j_0,j_1,j_2],['J+0', 'J+1','J+2']);
		}
	  }

	socket.addEventListener("message", function (event) {
		var data = JSON.parse(event.data);
		var updatedData = data.updated_data;

      if (isActivePage) {
        j_0 = updatedData.j_0;
        j_1 = updatedData.j_1;
        j_2 = updatedData.j_2;
        k_1 = updatedData.k_1;
        k_2 = updatedData.k_2;
        k_3 = updatedData.k_3;
        k_4 = updatedData.k_4;
        k_5 = updatedData.k_5;
        
        updatebarChart();
        }

	  });
	
	document.addEventListener('visibilitychange', function () {
		isActivePage = document.visibilityState === 'visible';
	  });

	// Event listeners for button clicks
	$('#Immédiateté').click(updatebarChart);
  
	$('#Poids2').click(function() {
	  barChart.options.scales.xAxes[0].scaleLabel.labelString = 'Poids en kg';
	  updatebarChartWithData(barChart, [k_1,k_2,k_3,k_4,k_5],['0-5','5-40','40-150','150-300','300+']);
	});
  

});
  
  
  // Función para inicializar el gráfico
  function initbarChart($chart) {
    return new Chart($chart, {
        type: 'bar',
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
                        labelString: 'Immédiateté'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Nombre de livraisons' 
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
            labels: ['J+0', 'J+1','J+2'],
            datasets: [{
                label: 'Nombre de livraisons',
                data: [j_0, j_1,j_2],
                backgroundColor: ['#E85127', '#005347', '#C9D200']
            }]
        }
    });
}

const fixedColors2 = ['#E85127', '#005347', '#C9D200', '#32D21B', '#1D1D1B']
  
// Función para actualizar los datos del gráfico
function updatebarChartWithData(chart, newData, newLabels) {
	chart.data.datasets[0].data = newData;
  chart.data.labels = newLabels; 
  chart.data.datasets[0].backgroundColor = fixedColors2.slice(0, newData.length);
	chart.update();
};

//usar "timeout" apenas no success, em vez de "interval" para os 
//requests nao acumularem caso um deles demore a executar

var timeout_timer = 2000;
var source_url = 'http://84.23.208.186:25000';

/*
function getNumberOfCars() {
  $.ajax({
    type: "get",
    url: source_url + "/number_of_cars_parked",
    success: function (data) {
      //console.log the response
      console.log(data);
      $('#number_of_cars_parked').text(data);
      getNumberOfFreeSpaces();
    },
    error: function () {
      console.log('error');
      getNumberOfFreeSpaces();
    }
  });
}

function getNumberOfFreeSpaces() {
  $.ajax({
    type: "get",
    url: source_url + "/number_of_free_spaces",
    success: function (data) {
      //console.log the response
      console.log(data);
      $('#number_of_free_spaces').text(data);
      getNumberOfEntriesInTheLastHour();
    },
    error: function () {
      console.log('error');
      getNumberOfEntriesInTheLastHour();
    }
  });
}

function getNumberOfEntriesInTheLastHour() {
  $.ajax({
    type: "get",
    url: source_url + "/number_of_entries_in_the_last_hour",
    success: function (data) {
      //console.log the response
      console.log(data);
      $('#number_of_entries_last_hour').text(data);
      getNumberOfExitsInTheLastHour();
    },
    error: function () {
      console.log('error');
      getNumberOfExitsInTheLastHour();
    }
  });
}

function getNumberOfExitsInTheLastHour() {
  $.ajax({
    type: "get",
    url: source_url + "/number_of_exits_in_the_last_hour",
    success: function (data) {
      //console.log the response
      console.log(data);
      $('#number_of_exits_last_hour').text(data);
      //Send another request in 2 seconds.
      getNumberOfSpaces();
    },
    error: function () {
      console.log('error');
      getNumberOfSpaces();
    }
  });
}

function getNumberOfSpaces() {
  $.ajax({
    type: "get",
    url: source_url + "/number_of_spaces",
    success: function (data) {
      //console.log the response
      console.log(data);
      $('#number_of_spaces').text(data);
      getStatistics();
    },
    error: function () {
      console.log('error');
      getStatistics();
    }
  });
}

function getStatistics() {
  $.ajax({
    type: "get",
    url: source_url + "/statistics",
    success: function (data) {
      //console.log the response
      console.log(data);
      $('#statistics').text(data);
      get24hLog();
    },
    error: function () {
      console.log('error');
      get24hLog();
    }
  });
}

function get24hLog() {
  $.ajax({
    type: "get",
    url: source_url + "/last_24_hours_history",
    success: function (data) {
      //console.log the response
      console.log(data);
      $('#24h_log').text(data);
      getFullLog();
    },
    error: function () {
      console.log('error');
      getFullLog();
    }
  });
}

function getFullLog() {
  $.ajax({
    type: "get",
    url: source_url + "/all_time_history",
    success: function (data) {
      //console.log the response
      console.log(data);
      $('#all_time_log').text(data);
      setTimeout(function () {
        getNumberOfCars();
      }, 1000);
    },
    error: function () {
      setTimeout(function () {
        console.log('error');
        getNumberOfCars();
      }, timeout_timer);
    }
  });
}

function logout() {
  window.alert("logout!")
}
*/

function getMainPackage() {
  $.ajax({
    type: "get",
    url: source_url + "/main_data_package",
    success: function (data) {
      //console.log the response
      console.log(data);
      updateFields(data)
      setTimeout(function () {
        getMainPackage();
      }, timeout_timer);
    },
    error: function () {
      setTimeout(function () {
        console.log('error');
        getMainPackage();
      }, timeout_timer);
    }
  });
}

function updateFields(data) {
  var text = "";
  data['Busiest hours today'].forEach(element => {
    text += element + "h" + " ";
  });

  $('#busiest_hours_today').text(text);
  $('#number_of_cars_parked').text(data['Number of cars parked']);
  $('#number_of_free_spaces').text(data['Number of free spaces']);
  $('#number_of_entries_last_hour').text(data['Number of entries in the last hour']);
  $('#number_of_exits_last_hour').text(data['Number of exits in the last hour']);
  $('#number_of_spaces').text(data['Number of spaces']);
  $('#total_entries_today').text(data['Number of entries today']);
  $('#total_exits_today').text(data['Number of exits today']);
  $('#average_free_spaces_today').text(data['Average number of free spaces today']);
  $('#average_parked_cars_today').text(data['Average number of cars parked today']);

  updateActivityLog(data);
  updateGraph(data['Number of cars parked today hourly']);
}

function updateActivityLog(data) {
  $('#activity_1').text(data['Activity log'][0]['event']);
  $('#time_1').text(data['Activity log'][0]['time']);
  $('#activity_2').text(data['Activity log'][1]['event']);
  $('#time_2').text(data['Activity log'][1]['time']);
  $('#activity_3').text(data['Activity log'][2]['event']);
  $('#time_3').text(data['Activity log'][2]['time']);
  $('#activity_4').text(data['Activity log'][3]['event']);
  $('#time_4').text(data['Activity log'][3]['time']);
  $('#activity_5').text(data['Activity log'][4]['event']);
  $('#time_5').text(data['Activity log'][4]['time']);
  $('#activity_6').text(data['Activity log'][5]['event']);
  $('#time_6').text(data['Activity log'][5]['time']);
  $('#activity_7').text(data['Activity log'][6]['event']);
  $('#time_7').text(data['Activity log'][6]['time']);
  $('#activity_8').text(data['Activity log'][7]['event']);
  $('#time_8').text(data['Activity log'][7]['time']);
}

function drawGraph() {

  //get the bar chart canvas
  var ctx = $("#bar-chartcanvas");
  var n_carros = new Array(24);
  var colors = new Array(24);
  var borders = new Array(24);
  var labels = new Array(24);
  for (var i = 0; i < 24; i++) {
    n_carros[i] = 130;
    colors[i] = "rgba(255,170,86,0.8)";
    borders[i] = "rgba(10,20,30,1)";
    labels[i] = i + "h";
  }

  //bar chart data
  var data = {
    labels: labels,
    datasets: [
      {
        label: "Number of parked cars",
        data: n_carros,
        backgroundColor: colors,
        borderColor: borders,
        borderWidth: 1
      }
    ]
  };

  //options
  var options = {
    responsive: true,
    legend: {
      display: true,
      position: "bottom",
      labels: {
        fontColor: "#333",
        fontSize: 16
      }
    },
    scales: {
      yAxes: [{
        ticks: {
          min: 0
        }
      }]
    }
  };

  //create Chart class object
  chart = new Chart(ctx, {
    type: "bar",
    data: data,
    options: options
  });
};

function updateGraph(data_array) {
  //console.log(data_array);

  //remove old data
  for (var i = 0; i < 24; i++) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
      dataset.data.pop();
    });
  }

  //add new data
  for (var i = 0; i < 24; i++) {
    chart.data.labels.push(i + "h");
    chart.data.datasets.forEach((dataset) => {
      dataset.data.push(data_array[i]);
    });
  }
  chart.update(0);
  //console.log(chart);
}

//Call functions

//getNumberOfCars();
drawGraph();
getMainPackage();
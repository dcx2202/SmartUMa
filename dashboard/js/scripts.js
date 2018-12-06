//usar "timeout" apenas no success, em vez de "interval" para os 
//requests nao acumularem caso um deles demore a executar

var timeout_timer = 1000;
var source_url = 'http://84.23.208.186:25000';


function getMainPackage() {
  $.ajax({
    type: "get",
    url: source_url + "/main_data_package",
    success: function (data) {
      //console.log the response
      console.log(data);
      updateFields(data);
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
  $('#number_of_entries_last_hour_2').text(data['Number of entries in the last hour']);
  $('#number_of_exits_last_hour').text(data['Number of exits in the last hour']);
  $('#number_of_exits_last_hour_2').text(data['Number of exits in the last hour']);
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

function checkLogin() {
  var isLoggedOn = localStorage.getItem('isLoggedOn');
  var mail_split = localStorage.getItem('mail').split('@');

  if (isLoggedOn == 'false') {
    window.location.replace('index.html');
  }

  if (mail_split[1] != 'admin.uma.pt'){
    $('#admin_tab').hide();
  }

  $('#username').text(localStorage.getItem('user'));
}

function checkRemember() {
  var checked_remember = localStorage.getItem('checked');
  var mail = localStorage.getItem('mail');

  //console.log(checked_lembrar);
  if (checked_remember === 'true') {
    $('#mail').val(mail);
    $('#check_remember').prop('checked', true);
  }
}

function loginFunction() {

  var mail = $('#mail').val().trim();
  var mail_split = mail.split('@');
  var pwd = $('#pwd').val();
  var erro = false;

  if (mail == '' || pwd == '')
    erro = true;
  else if (mail_split.length != 2)
    erro = true;
  else if (mail_split[0] == '' || mail_split[1] == '')
    erro = true;
  else if (mail_split[1] != 'student.uma.pt' && mail_split[1] != 'admin.uma.pt')
    erro = true;

  if (erro) {
    window.alert('Insert valid data!');
    return;
  }

  if ($('#check_remember').is(":checked")) {
    localStorage.setItem('checked', true);
    localStorage.setItem('mail', mail);
  }
  else {
    localStorage.setItem('checked', false);
  }

  localStorage.setItem('isLoggedOn', true);
  localStorage.setItem('user', mail_split[0]);
  window.location.replace('dashboard.html');
}

function logout() {
  window.alert("You have logged out!");
  localStorage.setItem('isLoggedOn', false);
  window.location.replace('index.html');
}

function dashboard() {
  checkLogin();
  drawGraph(); //draws a graph with placeholder values
  getMainPackage();
}

function index() {
  checkRemember();
}
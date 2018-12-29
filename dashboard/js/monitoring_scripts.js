function getMonitoringPackage() {
  $.ajax({
    type: "get",
    url: 'http://84.23.208.186:25000/system_monitoring_package',
    timeout: 7000,
    success: function (data) {
      console.log(data);
      setOnline('database', 'Online');
      setOnline('api', 'Online');
      $('#database_entries').text(data['Number of database entries']);
      $('#average_database_access_time').text(Number(data['Average database access time']).toFixed(3) + "s");
      $('#number_of_tables').text(data['Number of database tables']);
      $('#paths_available').text(data['Number of api endpoints available']);
      $('#api_requests').text(data['Number of api requests received']);
      $('#api_uptime').text(data['API Uptime']);
      $('#paths_available').text(data['Number of api endpoints available']);
    },
    error: function (data) {
      console.log(data);
      setOffline('database', 'Offline');
      setOffline('api', 'Offline');
      $('#database_entries').text('---');
      $('#number_of_tables').text('---');
      $('#average_database_access_time').text('---');
      $('#paths_available').text('---');
      $('#api_requests').text('---');
      $('#api_uptime').text('---');
      $('#paths_available').text('---');
    },
  });
}

function setOnline(name_of_square, text) {
  $('#' + name_of_square + '_color').removeClass('card-red');
  $('#' + name_of_square + '_color').addClass('card-green');
  $('#' + name_of_square + '_state').text(text);
}

function setOffline(name_of_square, text) {
  $('#' + name_of_square + '_color').addClass('card-red');
  $('#' + name_of_square + '_color').removeClass('card-green');
  $('#' + name_of_square + '_state').text(text);
}

function setGray(name_of_square) {
  $('#' + name_of_square + '_color').removeClass('card-red');
  $('#' + name_of_square + '_color').removeClass('card-green');
  $('#' + name_of_square + '_state').text('State');
}

function setSquaresOnClick() {
  var api_paths = [
    'number_of_cars_parked',
    'number_of_cars_parked_today_hourly',
    'number_of_entries_in_the_last_hour',
    'number_of_exits_in_the_last_hour',
    'number_of_entries_today',
    'number_of_exits_today',
    'number_of_spaces',
    'number_of_free_spaces',
    'average_number_of_cars_parked_today',
    'average_number_of_free_spaces_today',
    'busiest_hours_today',
    'activity_log',
    'main_data_package',
    'last_24_hours_history',
    'all_time_history'
  ];

  api_paths.forEach(element => {
    $('#' + element + '_color').click(function () {
      sendAjaxRequest(element)
    });
  });
}

function sendAjaxRequest(path) {
  setGray(path);
  var startDate = new Date();
  $.ajax({
    type: "get",
    url: 'http://84.23.208.186:25000/' + path,
    timeout: 5000,
    success: function (data) {
      console.log(data);
      var endDate = new Date();
      var interval = endDate - startDate;
      setOnline(path, 'Success: ' + interval + 'ms');
    },
    error: function (data) {
      console.log(data);
      setOffline(path, 'Request Failed');
    },
  });
}

function checkLogin() {
  var isLoggedOn = localStorage.getItem('isLoggedOn');
  var mail_split = localStorage.getItem('mail').split('@');

  if (isLoggedOn == 'false' || mail_split[1] != 'admin.uma.pt') {
    window.location.replace('index.html');
  }

  $('#username').text(localStorage.getItem('user'));
}

function logout() {
  window.alert("You have logged out!");
  localStorage.setItem('isLoggedOn', false);
  window.location.replace('index.html');
}

function monitoring() {
  checkLogin();
  setGray('database');
  setGray('api');
  getMonitoringPackage();
}

//update periodically
setInterval(getMonitoringPackage, 10000);
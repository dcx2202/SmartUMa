//usar "timeout" apenas no success, em vez de "interval" para os 
//requests nao acumularem caso um deles demore a executar

var timeout_timer = 2000;
var source_url = 'http://84.23.208.186:25000'

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

//Call functions
getNumberOfCars();
//getNumberOfFreeSpaces();
//getNumberOfEntriesInTheLastHour();
//getNumberOfExitsInTheLastHour();

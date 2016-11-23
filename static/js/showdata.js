$(document).ready(function() {
  $("body").backstretch("/static/img/bg.jpg");

  let his_data = [],
    his_day = [];
  for (let i = 0; i < 60; i++) {
    // his_data.push(Math.floor(Math.random() * 22));
    his_data.push(0);
    his_day.push('');
  }
  //alert("aa");
  let linectx = $("#line");
  let barctx = $("#bar")
  //let myNewChart = new Chart(ctx);

  let options = {
    legend: {
      display: false,
    },
    scales: {
      xAxes: [{
        stacked: true
      }],
      yAxes: [{
        stacked: true
      }]
    },
    maintainAspectRatio: false
  };
  let bardata = {
    labels: his_day,
    datasets: [{
      //display:false,
      //label: "My First dataset",
      backgroundColor: 'rgba(54, 162, 235, 0.2)',

      borderColor: 'rgba(54, 162, 235, 0.2)',

      borderWidth: 1,
      data: his_data,
    }]
  };
  let linedata = {
    labels: his_day,
    datasets: [{
      fill: false,
      lineTension: 0.1,
      backgroundColor: "rgba(75,192,192,0.5)",
      borderColor: "rgba(75,192,192,0.5)",
      borderCapStyle: 'butt',
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: 'miter',
      pointBorderColor: "rgba(75,192,192,0.5)",
      pointBackgroundColor: "#fff",
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(75,192,192,0.5)",
      pointHoverBorderColor: "rgba(220,220,220,1)",
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: his_data,
      spanGaps: false,
      cubicInterpolationMode: 'monotone',
    }]
  };
  //let month=["January","February","March","April","MAy","June","July","August","September","October","November","December"];

  let get_dt_data = function() {
    $.ajax({
      url: "/get_dt_data",
      type: "GET",
      dataType: "json",
      contentType: 'application/x-www-form-urlencoded; charset=utf-8',
      cache: false,
      data: {
        timeLimits: + new Date(),
        timeInterval: 5 * 1000
      },
      success: function(data) {
        // console.log(data);
        his_data.push(data);
        his_data.shift();

        // myBarChart.data.datasets[0].data = his_data;
        // myBarChart.data.datasets[1].data = his_data;
        // myBarChart.data.labels = his_day;
        // myBarChart = new Chart(ctx, par);
        myBarChart.update(true);
        myLineChart.update(true);

        now_num += data;
        my_clock.face.factory.setValue(now_num);
      }
    });
  }

  let barpar = {
    type: 'bar',
    data: bardata,
    options: options
  };
  let linepar = {
    type: 'line',
    data: linedata,
    options: options
  };
  $("#bar").fadeOut();
  $("#line").show();
  let myLineChart = new Chart(linectx, linepar);
  let myBarChart = new Chart(barctx, barpar);
  // random data
  // 当前抖腿数量
  // let now_num = parseInt(Math.random() * 100);
  let now_num = 0;
  $('.reload').click(function() {
    get_dt_data();
  });
  $('.convertLB').click(function() {
    $("#bar").toggle('slow');
    $("#line").fadeToggle('slow');

  });
  // Clock counter
  // window.my_clock = new FlipClock($('.clock'), {
  //   clockFace: 'Counter',
  //   autoStart: false
  // });

  window.my_clock = $('.clock').FlipClock(9999, {
    clockFace: 'Counter'
  });
  my_clock.face.factory.setValue(now_num);

  setInterval(function(){
    $(".reload").click();
  }, 5000);

});
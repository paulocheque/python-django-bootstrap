'use strict';


angular.module('dashboard', ['ui'])

.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})

.run(function($http) {
  $http.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
})

.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
}])

.controller('DashboardCtrl', function($scope, $http) {
    $scope.dashboards = []
    $scope.dashboard = null
    $scope.timers = {}
    $scope.widgetFunction = {}

    $http.get("/api/v1/dashboard/?format=json").success(function (data) {
        // console.log(data)
        data.objects.forEach(function(dashboard) {
            $scope.dashboards.push(dashboard)
            if ($scope.dashboard == null) {
                $scope.selectDashboard(dashboard)
            }
        })
    });

    $scope.clearTimers = function() {
        for (var key in $scope.timers) {
            clearInterval($scope.timers[key])
        }
        $scope.timers = {}
    };

    $scope.selectDashboard = function(dashboard) {
        $scope.clearTimers()
        $scope.dashboard = dashboard
        $scope.widgets = dashboard.widgets
        $scope.widgets.forEach(function(widget) {
            widget.img_url = "?"
            // var timer = setInterval(function(){}, widget.api_config.refresh_interval);
            var timer = setInterval(function(){ $scope.updateWidget(widget) }, 50*1000);
            $scope.timers[widget.id] = timer

            $scope.updateWidget(widget)
        })
    };

    $scope.updateWidget = function(widget) {
        $scope.drawWidgetChart(widget)
        // $scope.drawWidgetToolbar(widget)
    };

    $scope.getWidgetHtmlElement = function(widget) {
      return document.getElementById("widget-" + widget.id)
    };

    $scope.getToolbarHtmlElement = function(widget) {
      return document.getElementById("toolbar-" + widget.id)
    };

    $scope.drawWidgetChart = function(widget) {
      $.ajax({
          url: widget.refresh_url,
          dataType:"json",
          accepts: 'application/json',
          contentType: 'application/json',
          success: function(response) {
              console.log(response)
              // var data = response.data.data;
              var data = response.data;
              var f = $scope.widgetFunction["_" + widget.widget_type]
              f(widget, data)
          }
      });
    };

    $scope.drawWidgetToolbar = function(widget) {
      var components = [
          // {type: 'html', datasource: widget.refresh_url},
          // {type: 'csv', datasource: widget.refresh_url},
          {type: 'htmlcode', datasource: widget.refresh_url,
           gadget: 'https://www.google.com/ig/modules/pie-chart.xml',
           userprefs: {'3d': 1},
           style: 'width: 800px; height: 700px; border: 3px solid purple;'}
      ];

      var container = document.getElementById($scope.getToolbarHtmlElement(widget));
      google.visualization.drawToolbar(container, components);
    };

    $scope.drawNumber = function(widget, data) {
        $scope.getWidgetHtmlElement(widget).innerHTML = "<span class='widget-word'>1234567.89</span>"
    };

    $scope.drawWord = function(widget, data) {
        $scope.getWidgetHtmlElement(widget).innerHTML = "<span class='widget-number'>Word</span>"
    };

    $scope.drawGoogleChart = function(chart, options, widget, data) {
        options.title = widget.title
        options.chartArea = {left:10, top:20, width:"500px", height:"500px"}
        options.legend = {position:'right'}

        // options.series = {
        //     0: { color: '#e2431e' },
        //     1: { color: '#e7711b' },
        //     2: { color: '#f1ca3a' },
        //     3: { color: '#6f9654' },
        //     4: { color: '#1c91c0' },
        //     5: { color: '#43459d' },
        // }

        var dataTable = google.visualization.arrayToDataTable(data);
        // var csv = google.visualization.dataTableToCsv(dataTable);
        // console.log(csv);
        google.visualization.events.addListener(chart, 'ready', function () {
          widget.img_url = chart.getImageURI()
          $scope.$apply();
          // htmlElement.innerHTML = '<img src="' + chart.getImageURI() + '" style="display:none;">'
          // console.log(htmlElement.innerHTML)
        });
        chart.draw(dataTable, options);
    };

    $scope.drawTableChart = function(widget, data) {
        var chart = new google.visualization.Table($scope.getWidgetHtmlElement(widget));
        var options = {
          showRowNumber: true
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawLineChart = function(widget, data) {
        var chart = new google.visualization.LineChart($scope.getWidgetHtmlElement(widget));
        var options = {
          pointShape: 'circle',
          pointSize: 3,
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawCurveLineChart = function(widget, data) {
        var chart = new google.visualization.LineChart($scope.getWidgetHtmlElement(widget));
        var options = {
            curveType: 'function',
          pointShape: 'circle',
          pointSize: 3,
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawPieChart = function(widget, data) {
        var chart = new google.visualization.PieChart($scope.getWidgetHtmlElement(widget));
        var options = {
            is3D:true
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawDonutChart = function(widget, data) {
        var chart = new google.visualization.PieChart($scope.getWidgetHtmlElement(widget));
        var options = {
            pieHole: 0.4
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawAreaChart = function(widget, data) {
        var chart = new google.visualization.AreaChart($scope.getWidgetHtmlElement(widget));
        var options = {
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawStackedAreaChart = function(widget, data) {
        var chart = new google.visualization.AreaChart($scope.getWidgetHtmlElement(widget));
        var options = {
          isStacked:true
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawBarChart = function(widget, data) {
        var chart = new google.visualization.BarChart($scope.getWidgetHtmlElement(widget));
        var options = {
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawStackedBarChart = function(widget, data) {
        var chart = new google.visualization.BarChart($scope.getWidgetHtmlElement(widget));
        var options = {
          isStacked:true
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawColumnChart = function(widget, data) {
        var chart = new google.visualization.ColumnChart($scope.getWidgetHtmlElement(widget));
        var options = {
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawStackedColumnChart = function(widget, data) {
        var chart = new google.visualization.ColumnChart($scope.getWidgetHtmlElement(widget));
        var options = {
          isStacked:true
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawHistogramChart = function(widget, data) {
        var chart = new google.visualization.Histogram($scope.getWidgetHtmlElement(widget));
        var options = {
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawScatterChart = function(widget, data) {
        var chart = new google.visualization.ScatterChart($scope.getWidgetHtmlElement(widget));
        var options = {
          // trendlines: { 0: {} }    // Draw a trendline for data series 0.
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawBubbleChart = function(widget, data) {
        var chart = new google.visualization.BubbleChart($scope.getWidgetHtmlElement(widget));
        var options = {
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawGeoChart = function(widget, data) {
        var chart = new google.visualization.GeoChart($scope.getWidgetHtmlElement(widget));
        var options = {
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawGaugeChart = function(widget, data) {
        var chart = new google.visualization.Gauge($scope.getWidgetHtmlElement(widget));
        var options = {
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };

    $scope.drawCalendarChart = function(widget, data) {
        var chart = new google.visualization.CalendarChart($scope.getWidgetHtmlElement(widget));
        var options = {
        };
        $scope.drawGoogleChart(chart, options, widget, data)
    };


    $scope.widgetFunction._1 = $scope.drawTableChart
    $scope.widgetFunction._2 = $scope.drawLineChart
    $scope.widgetFunction._3 = $scope.drawCurveLineChart
    $scope.widgetFunction._4 = $scope.drawPieChart
    $scope.widgetFunction._5 = $scope.drawDonutChart
    $scope.widgetFunction._6 = $scope.drawAreaChart
    $scope.widgetFunction._7 = $scope.drawStackedAreaChart
    $scope.widgetFunction._8 = $scope.drawBarChart
    $scope.widgetFunction._9 = $scope.drawStackedBarChart
    $scope.widgetFunction._10 = $scope.drawColumnChart
    $scope.widgetFunction._11 = $scope.drawStackedColumnChart
    $scope.widgetFunction._12 = $scope.drawHistogramChart
    $scope.widgetFunction._13 = $scope.drawNumber
    $scope.widgetFunction._14 = $scope.drawWord
    $scope.widgetFunction._15 = $scope.drawScatterChart
    $scope.widgetFunction._16 = $scope.drawBubbleChart
    $scope.widgetFunction._17 = $scope.drawCalendarChart
    $scope.widgetFunction._18 = $scope.drawGeoChart
    $scope.widgetFunction._19 = $scope.drawGaugeChart
})

/**
 * Created by Hina on 4/2/2017.
 */
$(document).ready(function () {

var drawSpiderChart = function(container){
Highcharts.chart(container, {

    chart: {
        polar: true,
        type: 'line'
    },

    title: {
        text: 'Overall Quality',
        x: -80
    },

    pane: {
        size: '80%'
    },

    xAxis: {
        categories: ['Completeness', 'Timeliness', 'Correctness', 'Validity',
                'Uniqueness', 'Usability'],
        tickmarkPlacement: 'on',
        lineWidth: 0
    },

    yAxis: {
        gridLineInterpolation: 'polygon',
        lineWidth: 0,
        min: 0
    },

    tooltip: {
        shared: true,
        pointFormat: '<span style="color:{series.color}">{series.name}: <b>%{point.y:,.0f}</b><br/>'
    },

    legend: {
        align: 'right',
        verticalAlign: 'top',
        y: 70,
        layout: 'vertical'
    },

    series: [{
        name: 'Quality Parameters',
        data: [78, 34, 12, 65, 59, 67],
        pointPlacement: 'on'
    }]

});
};
var drawLineChart= function(container){
Highcharts.chart(container, {

    title: {
        text: 'Monthly Quality Metric'
    },

    subtitle: {
        text: ''
    },

    yAxis: {
        title: {
            text: 'Number of Employees'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            pointStart: 2007
        }
    },

    series: [{
        name: 'Completeness',
        data: [34, 43, 89, 98, 56, 35, 99, 76]
    }, {
        name: 'Timeliness',
        data: [87, 37, 3, 67, 78, 32, 89, 100]
    }, {
        name: 'Correctness',
        data: [97, 32, 56, 78, 89, 89, 100, 89]
    }, {
        name: 'Validity',
        data: [null, null, 45, 23, 78, 45, 76, 78]
    }, {
        name: 'Uniqueness',
        data: [65, 90, 78, 89, 56, 56, 56, 89]
    }, {
        name: 'Usability',
        data: [45, 90, 78, 89, 36, 78, 56, 87]
    }
    ]

});
};


drawSpiderChart('spidermap');
drawLineChart('monthlylinegraph');
drawLineChart('yearlylinegraph');
});
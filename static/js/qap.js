/**
 * Created by Hina on 4/2/2017.
 */
$(document).ready(function () {
var format = function (str, col) {
    col = typeof col === 'object' ? col : Array.prototype.slice.call(arguments, 1);

    return str.replace(/\{\{|\}\}|\{(\w+)\}/g, function (m, n) {
        if (m == "{{") { return "{"; }
        if (m == "}}") { return "}"; }
        return col[n];
    });
};
var drawSpiderChart = function(container,seriesdata,titletext){
Highcharts.chart(container, {

    chart: {
        polar: true,
        type: 'line'
    },

    title: {
        text: titletext,
        x: -50
    },

    pane: {
        size: '75%'

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
        min: 1
    },

    tooltip: {
        shared: true,
        pointFormat: '<span style="color:{series.color}">{series.name}: <b>%{point.y:,.0f}</b><br/>'
    },


    series: [{
        name: 'Quality Parameters',
        data: [parseFloat(seriesdata.Completeness), parseFloat(seriesdata.Timeliness), parseFloat(seriesdata.Correctness), parseFloat(seriesdata.Validity), parseFloat(seriesdata.Uniqueness), parseFloat(seriesdata.Usability)],
        pointPlacement: 'on'
    }]

});
};
var drawMontlyChart = function(dom,categorydata,seriesdata){
console.log(seriesdata);
Highcharts.chart(dom, {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Monthly'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: categorydata
    },
    yAxis: {
        title: {
            text: 'Quality (%)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: false
            },
            enableMouseTracking: true
        }
    },
    series: [{
        name: 'Completeness',
        data: seriesdata.Completeness
    }, {
        name: 'Timeliness',
        data: seriesdata.Timeliness
    }, {
        name: 'Correctness',
        data: seriesdata.Correctness
    }, {
        name: 'Validity',
        data: seriesdata.Validity
    }, {
        name: 'Uniqueness',
        data: seriesdata.Uniqueness
    }, {
        name: 'Usability',
        data: seriesdata.Usability
    }
    ]

});

};
var drawYearlyChart = function(dom,categorydata,seriesdata){
console.log(seriesdata);
Highcharts.chart(dom, {
    chart: {
        type: 'line'
    },
    title: {
        text: 'Yearly'
    },
    subtitle: {
        text: ''
    },
    xAxis: {
        categories: categorydata
    },
    yAxis: {
        title: {
            text: 'Quality (%)'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: false
            },
            enableMouseTracking: true
        }
    },
    series: [{
        name: 'Completeness',
        data: seriesdata.Completeness
    }, {
        name: 'Timeliness',
        data: seriesdata.Timeliness
    }, {
        name: 'Correctness',
        data: seriesdata.Correctness
    }, {
        name: 'Validity',
        data: seriesdata.Validity
    }, {
        name: 'Uniqueness',
        data: seriesdata.Uniqueness
    }, {
        name: 'Usability',
        data: seriesdata.Usability
    }
    ]

});

};

var showanalysis = function(data,issearch){
 $('#chartcontainer').empty();
   if(issearch)
    {
        populateanalysis(data);
    }
    else
    {
        var i;
        for(i=0;i<data.length;i++)
        {
            populateanalysis(data[i]);
        }
    }
    showcontent(4);
};

var populateanalysis = function(data){
    var stationcontainer='stationcontainer_' + data.uid;
        var spidercontainer='spiderchart_' + data.uid;
        var monthchartcontainer='monthchart_' + data.uid;
        var yearchartcontainer='yearchart_' + data.uid;

        var templatedom =' <span class="w3-text-grey w3-hover-text-grey:hover">{4}</span><div id="{0}" class="w3-container"><div  id="{1}"  class="w3-third" ></div><div id="{2}" class="w3-third"></div><div id="{3}"  class="w3-third" ></div></div><hr/>';
        var stationcontainerdom = format(templatedom,stationcontainer,spidercontainer,monthchartcontainer,yearchartcontainer,data.Station);
        $('#chartcontainer').append(stationcontainerdom);

        var defaultseriesdata =data.DefaultQualityParameters;
        var spidercharttitletext='Overall Quality ('+ String(data.DefaultQualityParameters.Overall_Data_Quality)+' %)'
        drawSpiderChart(spidercontainer,defaultseriesdata,spidercharttitletext);

        if(data.MonthlyQPFlag === true)
        {
            var categorydata= data.MonthlyLabel; // ['Jan, Feb,Mar]
            var seriesdata =data.MonthlyQualityParameters;
            drawMontlyChart(monthchartcontainer,categorydata,seriesdata);
        }

        if(data.YearlyQPFlag === true)
        {
            var categorydata= data.YearlyLabel; // ['2015', '2016', '2017'];
            var seriesdata =data.YearlyQualityParameters;
            drawYearlyChart(yearchartcontainer,categorydata,seriesdata);

        }
};


 //$('#modal').modal();
        // Smart Wizard
        $('#wizard').smartWizard({onFinish: onFinishCallback});

        function onFinishCallback(objs, context) {

            if (validateAllSteps()) {

                var data =viewModel.DataInputModel;
                data.Source = viewModel.DiSourceValue();
                //data.CsvFileName= "98723420348.csv",
                //name of file input taken from the server side
                data.CsvFileName=$('#hdnFileName').val()
                data.Region = $("#dropdowndatainputregion").val();
                data.Station = $("#dropdowndatainputstation").val();
                if(data.Station == 'Other')
                {
                    data.Station = $('#txtInputOtherStation').val();
                }

                data.FromDate = $("#datepickerdatainputfrom").val();
                data.ToDate = $("#datepickerdatainputto").val();
                data.IsRequiredClean =viewModel.IsRequiredClean();
                data.Parameters.Completeness = viewModel.Completeness();
                data.Parameters.Correctness = viewModel.Correctness();
                data.Parameters.Timeliness = viewModel.Timeliness();
                data.Parameters.Uniqueness = viewModel.Uniqueness();
                data.Parameters.Validity = viewModel.Validity();
                data.Parameters.Consistency = viewModel.Consistency();
                data.Parameters.Reliability = viewModel.Reliability();
                data.Parameters.Usability = viewModel.Usability();
                data.ValidationType = viewModel.ValidationType();
                data.ModelBasedSubType =viewModel.ModelBasedSubType();
                data.MonthlyValidation=viewModel.MonthlyValidation();
                data.MonthStartDate=viewModel.MonthStartDate();
                data.MonthEndDate=viewModel.MonthEndDate();
                data.YearlyValidation=viewModel.YearlyValidation();
                data.StartYear=viewModel.StartYear();
                data.EndYear=viewModel.EndYear();

                data.Model = viewModel.Model();
                console.log(data);
                qap.submitdatainput(data,showanalysis);
               // getsetSearchResult();
                //showanalysis(4);
                //showMessage();
            }
        }

        // Your Step validation logic
        function validateSteps(stepnumber) {
            var isStepValid = true;
            // validate step 1
            if (stepnumber == 1) {
                // Your step validation logic
                // set isStepValid = false if has errors
            }
            // ...
        }

        function validateAllSteps() {
            var isStepValid = true;
            // all step validation logic
            return isStepValid;
        }

        function showMessage() {
            alert('Hello');
        }

        $("#collectionaccordion").accordion();


        // create a template using the above definition
        var validatedData = qap.getResult();

        var dataSource = new kendo.data.DataSource({
            data: validatedData,
            change: function () { // subscribe to the CHANGE event of the data source
                //$("#validatedResultSet tbody").html(kendo.render(template, this.view())); // populate the table
            }
        });

        // read data from the "movies" array
        dataSource.read();

        var bindResultGrid = function (resultData) {
            var tempDataSource =new kendo.data.DataSource({ data: resultData });

            $("#grid").kendoGrid({
                dataSource: tempDataSource,
                selectable: "row",
                change: function (e) {
                    var selectedRows = this.select();
                    showanalysis(this.dataItem(selectedRows[0]));

                },
                // navigatable: true,
                // navigate: function(e) {
                //   console.log(e.element); // displays the newly highlighted cell
                //  },
                //height: 450,
                groupable: false,
                sortable: true,
                pageable: {
                    refresh: true,
                    pageSizes: true,
                    buttonCount: 5
                },
                columns: [{
                    field: "Region",
                    title: "Region",
                    width: 200
                }, {
                    field: "Station",
                    title: "Station",
                    width: 200
                }, {
                    field: "From",
                    title: "From"
                }, {
                    field: "To",
                    title: "To"
                }, {
                    field: "IsCleaned",
                    title: "Is Cleaned",
                    width: 100
                },
                {
                    command: [{
                        name: "Analysis",
                        width: 100,
                        click: function(e) {
                            // prevent page scroll position change
                            e.preventDefault();
                            // e.target is the DOM element representing the button
                            var tr = $(e.target).closest("tr"); // get the current table row (tr)
                            // get the data bound to the current table row
                            var data = this.dataItem(tr);
                             var selectedRows = this.select();
                            showanalysis(data,true);
                            console.log("Details for: " + data.Region);
                        }
                      }]
                }
                ]
            });
        };

        /*Get Region Start*/
        var getregion = function(){
            var regions;
            $.ajax({
                type: "GET",
                url: "/getallregioninfo",
                dataType:"json",
                contentType:"application/json",
                success: function (result) {
                        regions = result.regions;
                        binddatainputregion(regions); //Data input page
                        bindregion(regions); //Search Page
                },
                error: function(){
                    console.log("Error occured while fetching region information")
                }
            });
        };
        /*Get Region End*/

        var bindregion = function (regions) {
              $("#dropdownregion").kendoDropDownList({
                    dataTextField: "RegionName",
                    dataValueField: "RegionName",
                    dataSource: regions,
                    index: 0,
                    change: function(){
                        bindstation(this.dataItem().Stations);
                    },
                    dataBound:function(e){
                        bindstation(this.dataItems()[0].Stations);
                    }
                });
            };


        var binddatainputregion = function (regions) {


            $("#dropdowndatainputregion").kendoDropDownList({
                dataTextField: "RegionName",
                dataValueField: "RegionName",
                dataSource: regions,
                index: 0,
                change: function(){
                        binddatainputstation(this.dataItem().Stations);
                    },
                dataBound:function(e){
                        binddatainputstation(this.dataItems()[0].Stations);
                    }
            });
        };
        var bindstation = function (stations) {
            var regionId = 1;
            //var stations = qap.getStationsByRegionId(regionId);
            $("#dropdownstation").kendoDropDownList({
                dataTextField: "StationName",
                dataValueField: "StationName",
                dataSource: stations,
                index: 0,
                change: function(){
                        showhideOtherStation('dropdownstation','txtOtherStation');
                    },
            });

        };

        var showhideOtherStation=function(drpstation,txtotherstation)
        {
            if( $("#"+drpstation).val() == 'Other')
            {
                $("#"+txtotherstation).show();
            }
            else
            {
                $("#"+txtotherstation).hide();
            }
        }

        var binddatainputstation = function (stations) {
            var regionId = 1;
            //var stations = qap.getStationsByRegionId(regionId);
            $("#dropdowndatainputstation").kendoDropDownList({
                dataTextField: "StationName",
                dataValueField: "StationName",
                dataSource: stations,
                index: 0,
                 change: function(){
                        showhideOtherStation('dropdowndatainputstation','txtInputOtherStation');
                    },

            });
        };


        getregion();
        $("#fromdatepicker").kendoDatePicker();
        $("#todatepicker").kendoDatePicker();
        $("#datepickerdatainputfrom").kendoDatePicker();
        $("#datepickerdatainputto").kendoDatePicker();


        //Knocout Bindings

        ko.applyBindings(viewModel);

        var getsetSearchResult = function(){

        var tempregion = $("#dropdownregion").val();
            var tempstation = $("#dropdownstation").val();
            if(tempstation == 'Other')
            {
                tempstation = $("#txtOtherStation").val();
            }
            viewModel.SearchModel.Region=tempregion;
            viewModel.SearchModel.Station=tempstation;
            viewModel.SearchModel.FromDate=$('#fromdatepicker').val();
            viewModel.SearchModel.ToDate=$('#todatepicker').val();
            var selfQap = qap;
           // var resultdata = selfQap.search(viewModel.SearchModel);
           $.ajax({
                    type:"GET",
                    url:"/search",
                    dataType:"json",
                    //contentType:"application/json",
                    data:viewModel.SearchModel,
                     beforeSend: function(){
                         // Handle the beforeSend event
                         selfQap.showmodal();
                       },
                    success:function(response){
                        if(response.data.found ==='no')
                        {
                            console.log('No Record found');
                            return;
                        }

                    },
                    error:function(response){console.log('There is error while fetching search data')},
                    complete:function(response){
                     selfQap.resultModel = response.responseJSON.data.records;
                     bindResultGrid(selfQap.resultModel);
                    selfQap.hidemodal();

                    }
                });

        };
        $("#btnSearch").on("click", function () {
            getsetSearchResult();

           // qap.hidemodal();
        });

         $('#btncsvfile').change(function () {
        sendFile(this.files[0]);
        //$('#frmcsvfile').submit(function (e) {
            // e.preventDefault();
       // });
    });

    function sendFile(file) {
        var fd = new FormData(document.getElementById("frmcsvfile"));
        $.ajax({
            type: 'post',
            url: '/upload',
            data: fd,
            success: function (data) {
                // do something
                var fname = data.result.filename;
                console.log(fname);
                $('#hdnFileName').val(fname);
            },
             error: function (data) {
                // do something

                $('#hdnFileName').val('error');
            },
            xhrFields: {
                // add listener to XMLHTTPRequest object directly for progress (jquery doesn't have this yet)
                onprogress: function (progress) {
                    // calculate upload progress
                    var percentage = Math.floor((progress.total / progress.totalSize) * 100);
                    // log upload progress to console
                    console.log('progress', percentage);
                    if (percentage === 100) {
                        console.log('DONE!');
                    }
                }
            },
            processData: false,
            contentType: false
        });
        return false;
    }


    showcontent(2); //show default data input. For debug
    });


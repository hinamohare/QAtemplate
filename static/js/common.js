/**
 * Created by Hina on 3/26/2017.
 * qap -> Quality Assurance Platform
 */
$(document).ready(function(){
qap = {};
qap.models = {};
qap.models.databoardmodel = {};
qap.regions = {};
    viewModel =
    {
        SectionName: ko.observable('Dashboard'),
        SectionId: ko.observable(),
        DiSourceValue: ko.observable("WebService"),
        ShowCsvSource: ko.observable('false'),
        ShowWsSource: ko.observable('true'),
        IsRequiredClean: ko.observable('true'),
        CsvFileName:ko.observable('Somecsv.csv'),
        Completeness:ko.observable('true'),
        Accuracy:ko.observable('true'),
        Timeliness:ko.observable('true'),
        Uniqueness:ko.observable('true'),
        Validity:ko.observable('true'),
        Consistency:ko.observable('true'),
        Reliability:ko.observable('true'),
        Usability:ko.observable('true'),
        Availability:ko.observable('true'),
        Model: ko.observable('Model1'),
        ValidationType : ko.observable('ModelBased'),
        ModelBasedSubType : ko.observable('StationBased'),
        IsModelBased:ko.observable('true'),
        validationTypeClick:function () {
            var self = this;
            self.IsModelBased('false');
        }

    };


viewModel.DataInputModel = {
    Source: "CSV",
    CsvFileName: "98723420348.csv",
    Region: "SomeREgion",
    Station: "SomeStation",
    FromDate: "12/11/2009",
    ToDate: "12/11/2009",
    IsRequiredClean: true,
    Parameters: {Completeness:true,Accuracy:true,Timeliness:true,Uniqueness:true,Validity:true,Consistency:true,Reliability:true,Usability:true,Availability:true},
    Model: "TestModel",
    ValidationType: "ToolBased",
    ModelBasedSubType: "RegionBased"
};


viewModel.SearchModel = {
    Region: "TestRegion",
    Station: "TestStation",
    FromDate: '',
    ToDate: ''

};

qap = {
        showmodal :function () {
            $('#mainmodal').show();
        },
        hidemodal : function () {
            $('#mainmodal').hide();
        },
        setTimeout : function () {
            window.setTimeout(function () {
            }, 5000);
        },
        resultModel:[],
        search :function(searchParam){
            var self=this;

            $.ajax({
                    type:"GET",
                    url:"/search",
                    dataType:"json",
                    //contentType:"application/json",
                    data:searchParam,
                     beforeSend: function(){
                         // Handle the beforeSend event
                         self.showmodal();
                       },
                    success:function(response){
                        if(response.data.found ==='no')
                        {
                            console.log('No Record found');
                            return;
                        }
                        var validatedData = response.data.records;
                        self.resultModel = validatedData;
                        console.log(response.data);

                       // bindResultGrid(validatedData);
                    //bind data to result grid
                    },
                    error:function(response){console.log('There is error while fetching search data')},
                    complete:function(response){
                     self.resultModel = response.responseJSON.data.records;
                    self.hidemodal();

                    }
                });
            }
        ,submitdatainput: function (inputdata) {
            var jsonString = JSON.stringify(inputdata);
            $.ajax({
                type: "POST",
                url: "/getWaterQuality",
                contentType: "application/json",
                dataType: "json",
                success: function (msg) {
                    if (msg) {
                        //alert("Submitted");

                    } else {
                        alert("Cannot add to list !");
                    }
                },

                data: jsonString
            });
        },
        getRegions: function () {

            $.ajax({
                type: "GET",
                url: "/getallregioninfo",
                dataType:"json",
                contentType:"application/json",
                success: function (result) {
                   // return result.regions;
                    console.log(result);
                    console.log(result["regions"])

                    return result;
                },
                error: function(){
                    console.log("Error occured while fetching region information")
                    },
                /*complete:function(result){
                   // var result = JSON.parse(response);
                    console.log(result);
                    console.log(result["regions"])
                    console.log(JSON.parse(result));
                    return result;
                    }*/
            });

    },
    getStationsByRegionId: function (regionId) {
        var stations = [
            {StationName: "South March", StationCode: "elksmwq", Lat: 38.0012, Lon: 122.4604}
            , {StationName: "Azevedo Pond", StationCode: "elkapwq", Lat: 36.8457, Lon: 121.7538}
        ];
        return stations;
    },
    getResult: function () {
        var validatedData = [{
            'Region': "Padilla Bay, WA", Dimension: 'Region', 'Station': "Bayview Channel", 'From': "2017-01-01",
            'To': "2017-01-01", 'IsCleaned': "true", 'OverallQuality': 80, 'Parameters': {
                'Completeness': 45,
                'Accuracy': 98,
                'Timeliness': 89,
                'Uniqueness': 23,
                'Validity': 75,
                'Consistency': 12,
                Reliability: 75,
                Usability: 75
            }
        },
            {
                'Region': "Padilla Bay, WA", Dimension: 'Station', 'Station': "Ploeg Channel", 'From': "2017-01-01",
                'To': "2017-01-01", 'IsCleaned': "true", 'OverallQuality': 80, 'Parameters': {
                'Completeness': 34,
                'Accuracy': 56,
                'Timeliness': 76,
                'Uniqueness': 7,
                'Validity': 75,
                'Consistency': 98,
                Reliability: 75,
                Usability: 75
            }
            },
            {
                'Region': "Padilla Bay, WA", Dimension: 'Region', 'Station': "Joe Leary Estuary", 'From': "2017-01-01",
                'To': "2017-01-01", 'IsCleaned': "true", 'OverallQuality': 80, 'Parameters': {
                'Completeness': 54,
                'Accuracy': 34,
                'Timeliness': 23,
                'Uniqueness': 75,
                'Validity': 75,
                'Consistency': 76,
                Reliability: 75,
                Usability: 75
            }
            },
            {
                'Region': "Padilla Bay, WA", Dimension: 'Station', 'Station': "Bayview Channel", 'From': "2017-01-01",
                'To': "2017-01-01", 'IsCleaned': "true", 'OverallQuality': 80, 'Parameters': {
                'Completeness': 76,
                'Accuracy': 12,
                'Timeliness': 12,
                'Uniqueness': 58,
                'Validity': 75,
                'Consistency': 56,
                Reliability: 75,
                Usability: 75
            }
            },
            {
                'Region': "Padilla Bay, WA", Dimension: 'Region', 'Station': "Bayview Channel", 'From': "2017-01-01",
                'To': "2017-01-01", 'IsCleaned': "true", 'OverallQuality': 80, 'Parameters': {
                'Completeness': 34,
                'Accuracy': 65,
                'Timeliness': 32,
                'Uniqueness': 54,
                'Validity': 23,
                'Consistency': 75,
                Reliability: 98,
                Usability: 12
            }
            }
        ];
        return validatedData;

    },
    getResultByStation: function () {
        var DashBoard = new Object();
        DashBoard.Completeness = 20;
        DashBoard.Accuracy = 30;
        DashBoard.Timeliness = 50;
        DashBoard.Uniqueness = 70;
        DashBoard.Validity = 50;
        DashBoard.Consistency = 30;
        DashBoard.Reliability = 38;
        DashBoard.Usability = 49;
        return DashBoard;
    },
    getResultByRegion: function () {
        var result = [];

        var DashBoard = new Object()
        DashBoard.StationCode = "elksmwq";
        DashBoard.Completeness = 20;
        DashBoard.Accuracy = 30;
        DashBoard.Timeliness = 50;
        DashBoard.Uniqueness = 70;
        DashBoard.Validity = 50;
        DashBoard.Consistency = 30;
        DashBoard.Reliability = 38;
        DashBoard.Usability = 49;
        result.push(DashBoard)

        var DashBoard = new Object()
        DashBoard.StationCode = "elksmwq";
        DashBoard.Completeness = 56;
        DashBoard.Accuracy = 76;
        DashBoard.Timeliness = 43;
        DashBoard.Uniqueness = 24;
        DashBoard.Validity = 50;
        DashBoard.Consistency = 6;
        DashBoard.Reliability = 45;
        DashBoard.Usability = 13;

        result.push(DashBoard)
        return result;

    }


};

});
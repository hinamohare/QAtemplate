from model import RegionData


stations = [

    {
        "RegionId": 1,
        "RegionName": "San Francisco Bay, CA",
        "Stations": [
            {"StationCode": "sfbccwq",
             "Lat": 38.0012,
             "Lon": 122.4604,
             "StationName": "China Camp"
             }
        ]
    },
    {
        "RegionId": 2,
        "RegionName": "Elkhorn Slogh, CA",
        "Stations": [
            {"Lat": 36.8179,
             "StationCode": "elksmwq",
             "Lon": 121.7394,
             "StationName": "Soth March"
             },
            {"Lat": 36.8457,
             "StationCode": "elkapwq",
             "Lon": "121.7538",
             "StationName": "Azevedo Pond"
             },
            {"Lat": 36.8111,
             "StationCode": "elkvmwq",
             "Lon": 121.7792,
             "StationName": "Vierra Moth"
             },
            {"Lat": 36.8346,
             "StationCode": "elknmwq",
             "Lon": 121.7384,
             "StationName": "North Marsh"
             }
        ]
    },
    {
        "RegionId": 3,
        "RegionName": "Tijana River, CA",
        "Stations": [
            {"Lat": 32.5595,
             "StationCode": "tjrbrwq",
             "Lon": 117.1288,
             "StationName": "Boca Rio"
             },
            {"Lat": 32.59612,
             "StationCode": "tjrprwq",
             "Lon": 117.11822,
             "StationName": "Pond Eleven Restored"
             },
            {"Lat": 32.600136,
             "StationCode": "tjrsbwq",
             "Lon": 117.115692,
             "StationName": "Soth Bay"
             },
            {"Lat": 32.56829,
             "StationCode": "tjroswq",
             "Lon": 117.13127,
             "StationName": "Oneonta Slogh"
             }
        ]
    },
    {
        "RegionId": 4,
        "RegionName": "Soth Slogh, OR",
        "Stations": [
            {"Lat": 43.296501,
             "StationCode": "sosecwq",
             "Lon": 124.310729,
             "StationName": "Elliot Creek"
             },
            {"Lat": 43.3377,
             "StationCode": "soschwq",
             "Lon": 124.320533,
             "StationName": "Charleston Bridge"
             },
            {"Lat": 43.27615,
             "StationCode": "soswiwq",
             "Lon": 124.3197528,
             "StationName": "Winchester Arm"},
            {"Lat": 43.317217,
             "StationCode": "sosvawq",
             "Lon": 124.321633,
             "StationName": "Valino Island"
             }
        ]
    },
    {
        "RegionId": 5,
        "RegionName": "Padilla Bay, WA",
        "Stations": [
            {"Lat": 48.496139,
             "StationCode": "pdbbywq",
             "Lon": 122.502114,
             "StationName": "Bayview Channel"
             },
            {"Lat": 48.556322,
             "StationCode": "pdbbpwq",
             "Lon": 122.530894,
             "StationName": "Ploeg Channel"
             },
            {"Lat": 48.518264,
             "StationCode": "pdbjewq",
             "Lon": 122.474189,
             "StationName": "Joe Leary Estary"
             }
        ]
    },

    {
        "RegionName": "Kachemak Bay, Alaska",
        "RegionId": 6,
        "Stations": [
            {
                "StationName": "Seldovia Deep",
                "StationCode": "kacsdwq",
                "Lat": "59.44099",
                "Lon": "151.72096"
            },
            {
                "StationName": "Homer Dolphin Deep",
                "StationCode": "kachdwq",
                "Lat": "59.60201",
                "Lon": "151.40878"
            },
            {
                "StationName": "Seldovia Surface",
                "StationCode": "kacsswq",
                "Lat": "59.44099",
                "Lon": "151.72096"
            },
            {
                "StationName": "Homer Surface 3",
                "StationCode": "kach3wq",
                "Lat": "59.60205",
                "Lon": "151.40942"
            }
        ]
    },
    {
        "RegionName": "Mission Aransas, TX",
        "RegionId": 7,
        "Stations": [
            {
                "StationName": "Aransas Bay",
                "StationCode": "marabwq",
                "Lat": "27.9798",
                "Lon": "97.0287"
            },
            {
                "StationName": "Copano bay East",
                "StationCode": "marcewq",
                "Lat": "28.1323",
                "Lon": "97.0344"
            },
            {
                "StationName": "Ship Channel",
                "StationCode": "marscwq",
                "Lat": "27.83811",
                "Lon": "97.05022"
            },
            {
                "StationName": "Mesquite Bay",
                "StationCode": "marmbwq",
                "Lat": "28.1384",
                "Lon": "96.8285"
            },
            {
                "StationName": "Copano Bay West",
                "StationCode": "marcwwq",
                "Lat": "28.0841",
                "Lon": "97.2009"
            }
        ]
    },
    {
        "RegionName": "Lake Superior, WI",
        "RegionId": 8,
        "Stations": [
            {
                "StationName": "Barker's Island",
                "StationCode": "lksbawq",
                "Lat": "46.721772",
                "Lon": "92.06352"
            },
            {
                "StationName": "Oliver Bridge",
                "StationCode": "lksolwq",
                "Lat": "46.65685",
                "Lon": "92.20166"
            }
        ]
    },
    {
        "RegionName": "Old Woman Creek, OH",
        "RegionId": 9,
        "Stations": [
            {
                "StationName": "State Route 6",
                "StationCode": "owcwmwq",
                "Lat": "41.3825",
                "Lon": "82.515"
            },
            {
                "StationName": "Lower Estuary",
                "StationCode": "owcolwq",
                "Lat": "41.3819",
                "Lon": "82.5142"
            },
            {
                "StationName": "Berlin Road",
                "StationCode": "owcbrwq",
                "Lat": "41.3483",
                "Lon": "82.5083"
            },
            {
                "StationName": "Darrow Road",
                "StationCode": "owcdrwq",
                "Lat": "41.364978",
                "Lon": "82.504739"
            }
        ]
    },
    {
        "RegionName": "Jobos Bay, Puerto Rico",
        "RegionId": 10,
        "Stations": [
            {
                "StationName": "Station 20",
                "StationCode": "job20wq",
                "Lat": "17.930317",
                "Lon": "66.211472"
            },
            {
                "StationName": "Station 19",
                "StationCode": "job19wq",
                "Lat": "17.942914",
                "Lon": "66.228825"
            },
            {
                "StationName": "Station 10",
                "StationCode": "job10wq",
                "Lat": "17.938611",
                "Lon": "66.257736"
            },
            {
                "StationName": "Station 9",
                "StationCode": "job09wq",
                "Lat": "17.943022",
                "Lon": "66.238511"
            }
        ]
    },
    {
        "RegionName": "Grand Bay, MS",
        "RegionId": 11,
        "Stations": [
            {
                "StationName": "Bangs Lake",
                "StationCode": "gndblwq",
                "Lat": "30.3571",
                "Lon": "88.4629"
            },
            {
                "StationName": "Bayou Heron",
                "StationCode": "gndbhwq",
                "Lat": "30.4178",
                "Lon": "88.4054"
            },
            {
                "StationName": "Bayou Cumbest",
                "StationCode": "gndbcwq",
                "Lat": "30.3836",
                "Lon": "88.4364"
            },
            {
                "StationName": "Point Aux Chenes Bay",
                "StationCode": "gndpcwq",
                "Lat": "30.3486",
                "Lon": "88.4185"
            }
        ]
    },
    {
        "RegionName": "Weeks Bay, AL",
        "RegionId": 12,
        "Stations": [
            {
                "StationName": "Fish River",
                "StationCode": "wkbfrwq",
                "Lat": "30.4162",
                "Lon": "87.8228"
            },
            {
                "StationName": "Middle Bay",
                "StationCode": "wkbmbwq",
                "Lat": "30.3961",
                "Lon": "87.8335"
            },
            {
                "StationName": "Magnolia River",
                "StationCode": "wkbmrwq",
                "Lat": "30.39",
                "Lon": "87.8177"
            },
            {
                "StationName": "Weeks Bay",
                "StationCode": "wkbwbwq",
                "Lat": "30.3808",
                "Lon": "87.832"
            }
        ]
    },
    {
        "RegionName": "Apalachicola, FL",
        "RegionId": 13,
        "Stations": [
            {
                "StationName": "East Bay Bottom",
                "StationCode": "apaebwq",
                "Lat": "29.7858",
                "Lon": "84.8752"
            },
            {
                "StationName": "Dry Bar",
                "StationCode": "apadbwq",
                "Lat": "29.6747",
                "Lon": "85.0583"
            },
            {
                "StationName": "Cat Point",
                "StationCode": "apacpwq",
                "Lat": "29.7021",
                "Lon": "84.8802"
            },
            {
                "StationName": "East Bay Surface",
                "StationCode": "apaeswq",
                "Lat": "29.7858",
                "Lon": "84.8752"
            }
        ]
    },
    {
        "RegionName": "Rookery Bay, FL",
        "RegionId": 14,
        "Stations": [
            {
                "StationName": "Lower Henderson Creek",
                "StationCode": "rkblhwq",
                "Lat": "26.0257",
                "Lon": "81.7332"
            },
            {
                "StationName": "Middle Blackwater River",
                "StationCode": "rkbmbwq",
                "Lat": "25.9343",
                "Lon": "81.5946"
            },
            {
                "StationName": "Faka Union Bay",
                "StationCode": "rkbfuwq",
                "Lat": "25.9005",
                "Lon": "81.5159"
            },
            {
                "StationName": "Faka Hatchee Bay",
                "StationCode": "rkbfbwq",
                "Lat": "25.8922",
                "Lon": "81.477"
            }
        ]
    },
    {
        "RegionName": "Guana Tolomato Matanzas, FL",
        "RegionId": 15,
        "Stations": [
            {
                "StationName": "Pellicer Creek",
                "StationCode": "gtmpcwq",
                "Lat": "29.667071",
                "Lon": "81.257403"
            },
            {
                "StationName": "Pine Island",
                "StationCode": "gtmpiwq",
                "Lat": "30.050857",
                "Lon": "81.367465"
            },
            {
                "StationName": "Fort Matanzas",
                "StationCode": "gtmfmwq",
                "Lat": "29.737041",
                "Lon": "81.245953"
            },
            {
                "StationName": "San Sebastian",
                "StationCode": "gtmsswq",
                "Lat": "29.868851",
                "Lon": "81.307428"
            }
        ]
    },
    {
        "RegionName": "Sapelo Island, GA",
        "RegionId": 16,
        "Stations": [
            {
                "StationName": "Hunt Dock",
                "StationCode": "saphdwq",
                "Lat": "31.4786",
                "Lon": "81.2731"
            },
            {
                "StationName": "Lower Duplin",
                "StationCode": "sapldwq",
                "Lat": "31.417942",
                "Lon": "81.296047"
            },
            {
                "StationName": "Cabretta Creek",
                "StationCode": "sapcawq",
                "Lat": "31.4437",
                "Lon": "81.2399"
            },
            {
                "StationName": "Dean Creek",
                "StationCode": "sapdcwq",
                "Lat": "31.3896",
                "Lon": "81.2789"
            }
        ]
    },
    {
        "RegionName": "ACE Basin, SC",
        "RegionId": 17,
        "Stations": [
            {
                "StationName": "St. Pierre",
                "StationCode": "acespwq",
                "Lat": "32.5279",
                "Lon": "80.3615"
            },
            {
                "StationName": "Mosquito Creek",
                "StationCode": "acemcwq",
                "Lat": "32.5558",
                "Lon": "80.438"
            },
            {
                "StationName": "Fishing Creek",
                "StationCode": "acefcwq",
                "Lat": "32.6358",
                "Lon": "80.3655"
            }
        ]
    },
    {
        "RegionName": "North Inlet Winyah Bay, SC",
        "RegionId": 18,
        "Stations": [
            {
                "StationName": "Oyster Landing",
                "StationCode": "niwolwq",
                "Lat": "33.3493511",
                "Lon": "79.1888819"
            },
            {
                "StationName": "Debidue Creek",
                "StationCode": "niwdcwq",
                "Lat": "33.3601486",
                "Lon": "79.1674572"
            },
            {
                "StationName": "Clambank",
                "StationCode": "niwcbwq",
                "Lat": "33.3338636",
                "Lon": "79.1930411"
            },
            {
                "StationName": "Thousand Acre",
                "StationCode": "niwtawq",
                "Lat": "33.2991461",
                "Lon": "79.2560564"
            }
        ]
    },
    {
        "RegionName": "North Carolina, NC",
        "RegionId": 19,
        "Stations": [
            {
                "StationName": "Research Creek",
                "StationCode": "nocrcwq",
                "Lat": "34.156",
                "Lon": "77.8499"
            },
            {
                "StationName": "Zeke's Basin",
                "StationCode": "noczbwq",
                "Lat": "33.9547",
                "Lon": "77.935"
            },
            {
                "StationName": "Loosin Creek",
                "StationCode": "noclcwq",
                "Lat": "34.1722",
                "Lon": "77.8328"
            },
            {
                "StationName": "East Cribbing",
                "StationCode": "nocecwq",
                "Lat": "33.9399",
                "Lon": "77.9411"
            }
        ]
    },
    {
        "RegionName": "Chesapeake Bay, VA",
        "RegionId": 20,
        "Stations": [
            {
                "StationName": "Sweethall",
                "StationCode": "cbvshwq",
                "Lat": "37.57138",
                "Lon": "76.88424"
            },
            {
                "StationName": "Goodwin Island",
                "StationCode": "cbvgiwq",
                "Lat": "37.215796",
                "Lon": "76.392675"
            },
            {
                "StationName": "Claybank",
                "StationCode": "cbvcbwq",
                "Lat": "37.346665",
                "Lon": "76.611263"
            },
            {
                "StationName": "Taskinas Creek",
                "StationCode": "cbvtcwq",
                "Lat": "37.414986",
                "Lon": "76.71442"
            }
        ]
    },
    {
        "RegionName": "Chesapeake Bay, MD",
        "RegionId": 21,
        "Stations": [
            {
                "StationName": "Otter Point Creek",
                "StationCode": "cbmocwq",
                "Lat": "39.4507",
                "Lon": "76.2746"
            },
            {
                "StationName": "Railroad",
                "StationCode": "cbmrrwq",
                "Lat": "38.7813",
                "Lon": "76.7137"
            },
            {
                "StationName": "Mataponi Creek",
                "StationCode": "cbmmcwq",
                "Lat": "38.7433",
                "Lon": "76.7074"
            },
            {
                "StationName": "Iron Pot Landing",
                "StationCode": "cbmipwq",
                "Lat": "38.796",
                "Lon": "76.7208"
            }
        ]
    },
    {
        "RegionName": "Delaware, DE",
        "RegionId": 22,
        "Stations": [
            {
                "StationName": "Scotton Landing",
                "StationCode": "delslwq",
                "Lat": "39.08498",
                "Lon": "75.46058"
            },
            {
                "StationName": "Division Street",
                "StationCode": "deldswq",
                "Lat": "39.1637",
                "Lon": "75.5191"
            },
            {
                "StationName": "Blackbird Landing",
                "StationCode": "delblwq",
                "Lat": "39.38876",
                "Lon": "75.636"
            },
            {
                "StationName": "Lebanon Landing",
                "StationCode": "delllwq",
                "Lat": "39.1144",
                "Lon": "75.4992"
            }
        ]
    },
    {
        "RegionName": "Jacques Cousteau, NJ",
        "RegionId": 23,
        "Stations": [
            {
                "StationName": "Chestnut Neck",
                "StationCode": "jacnewq",
                "Lat": "39.5479",
                "Lon": "74.4608"
            },
            {
                "StationName": "Buoy 126",
                "StationCode": "jacb6wq",
                "Lat": "39.5079",
                "Lon": "74.3385"
            },
            {
                "StationName": "Lower Bank",
                "StationCode": "jacbawq",
                "Lat": "39.5937",
                "Lon": "74.5515"
            }
        ]
    },
    {
        "RegionName": "Hudson River, NY",
        "RegionId": 24,
        "Stations": [
            {
                "StationName": "Tivoli North Bay",
                "StationCode": "hudtnwq",
                "Lat": "42.0365457",
                "Lon": "73.925324"
            },
            {
                "StationName": "Saw Kill",
                "StationCode": "hudskwq",
                "Lat": "42.0171722",
                "Lon": "73.9149611"
            },
            {
                "StationName": "Stony Creek",
                "StationCode": "hudscwq",
                "Lat": "42.0463",
                "Lon": "73.9108"
            },
            {
                "StationName": "Tivoli South Bay",
                "StationCode": "hudtswq",
                "Lat": "42.0270378",
                "Lon": "73.9259569"
            }
        ]
    },
    {
        "RegionName": "Narragansett Bay, RI",
        "RegionId": 25,
        "Stations": [
            {
                "StationName": "T-Wharf Bottom",
                "StationCode": "nartbwq",
                "Lat": "41.578361",
                "Lon": "71.321125"
            },
            {
                "StationName": "T-Wharf Surface",
                "StationCode": "nartswq",
                "Lat": "41.578361",
                "Lon": "71.321125"
            },
            {
                "StationName": "Nag Creek",
                "StationCode": "narncwq",
                "Lat": "41.62485",
                "Lon": "71.324283"
            },
            {
                "StationName": "Potters Cove",
                "StationCode": "narpcwq",
                "Lat": "41.64055",
                "Lon": "71.340881"
            }
        ]
    },
    {
        "RegionName": "Wquoit Bay, MA",
        "RegionId": 26,
        "Stations": [
            {
                "StationName": "Menauhant",
                "StationCode": "wqbmhwq",
                "Lat": "41.5526",
                "Lon": "70.5485"
            },
            {
                "StationName": "Childs River",
                "StationCode": "wqbcrwq",
                "Lat": "41.5798",
                "Lon": "70.5309"
            },
            {
                "StationName": "Metoxit Point",
                "StationCode": "wqbmpwq",
                "Lat": "41.5689",
                "Lon": "70.5216"
            },
            {
                "StationName": "Sage Lot",
                "StationCode": "wqbslwq",
                "Lat": "41.5542",
                "Lon": "70.5102"
            }
        ]
    },
    {
        "RegionName": "Great Bay, NH",
        "RegionId": 27,
        "Stations": [
            {
                "StationName": "Oyster River",
                "StationCode": "grborwq",
                "Lat": "43.134",
                "Lon": "70.911"
            },
            {
                "StationName": "Lamprey River",
                "StationCode": "grblrwq",
                "Lat": "43.08",
                "Lon": "70.9344"
            },
            {
                "StationName": "Great Bay",
                "StationCode": "grbgbwq",
                "Lat": "43.0921",
                "Lon": "70.8642"
            },
            {
                "StationName": "Squamscott River",
                "StationCode": "grbsqwq",
                "Lat": "43.052403",
                "Lon": "70.911811"
            }
        ]
    },
    {
        "RegionName": "Wells, ME",
        "RegionId": 28,
        "Stations": [
            {
                "StationName": "Inlet",
                "StationCode": "welinwq",
                "Lat": "43.320089",
                "Lon": "70.563442"
            },
            {
                "StationName": "Skinner Mill",
                "StationCode": "welsmwq",
                "Lat": "43.344711",
                "Lon": "70.549217"
            },
            {
                "StationName": "Head of Tide",
                "StationCode": "welhtwq",
                "Lat": "43.298347",
                "Lon": "70.587094"
            },
            {
                "StationName": "Little River Mout",
                "StationCode": "wellmwq",
                "Lat": "43.340153",
                "Lon": "70.540603"
            }
        ]
    }
]

obj = RegionData()
obj.insertRegionInfoIntoDB(stations)


import os, shutil, json


utils = [{
    "name": "totalEnergy",
    "type": "int",
    "input_data": {
        "power" : "var9"
    },
    "used_func": "integratePower"
},
{
    "name": "hourclock",
    "type": "boolean",
    "input_data": {},
    "used_func": "hourClock"
}]

cloud_config = {
    "active" : True,
    "platform" : "azure",
    "name" : "line"
}

config_bsw = {
    "LINE": {
        "mainCounter": {
            "id": "count",
            "scale": 1
        },
        "badCounter": {
            "id": "scraps",
            "scale": 1
        },
        "scrapReasons": [
            {
                "id": "scrap_broken",
                "scale": 1
            },
            {
                "id": "scrap_generic",
                "scale": 1
            },
            {
                "id": "scrap_label",
                "scale": 1
            },
            {
                "id": "scrap_manual",
                "scale": 1
            },
            {
                "id": "scrap_shape",
                "scale": 1
            },
            {
                "id": "scrap_vision",
                "scale": 1
            }
        ],
        "idealSpeed" : {
            "id" : "idealSpeed",
            "scale" : 1
        },
        "warnings": [
            "warn1",
            "warn2",
            "warn3",
            "warn4",
            "warn5",
            "warn6",
            "warn7",
            "warn8",
            "warn9",
            "warn10",
            "warn11",
            "warn12",
            "warn13",
            "warn14",
            "warn15"
        ],
        "raws": [
            {
                "sampling": 500,
                "vars": [
                    "var1",
                    "var2",
                    "var3",
                    "var4",
                    "var5",
                    "var6",
                    "var7",
                    "var8",
                    "var9",
                    "var10"
                ],
                "sendToMqtt": False
            }
        ],
        "alarms": [
            "al1",
            "al2",
            "al3",
            "al4",
            "al5",
            "al6",
            "al7",
            "al8",
            "al9",
            "al10",
            "al11",
            "al12",
            "al13",
            "al14",
            "al15"
        ],
        "snapshot": True,
        "recipe": [
            "par1",
            "par2",
            "par3",
            "par4",
            "par5",
            "par6",
            "par7",
            "par8"
        ],
        "buttons" : [
            "buttons1",
            "buttons2",
            "buttons3",
            "buttons4",
            "buttons5",
            "buttons6",
            "buttons7",
            "buttons8",
            "buttons9",
            "buttons10",
            "buttons11",
            "buttons12",
            "buttons13",
            "buttons14",
            "buttons15"
        ],
        "aggr": [
            "bottleSize",
            "operator",
            "prodId"
        ],
        "state": {
            "var": "state",
            "faulty": [
                2
            ],
            "productive": [
                0
            ],
            "possible_vals": [
                0,
                1,
                2,
                3
            ],
            "external": []
        },
        "breakdowns": {
            "mode": "prepost",
            "params": []
        },
        "consSum" : [{
            "id" : "utils.totalEnergy",
            "scale" : 1
        }]
    }
}

profile = {
    "manufacturer": "demo",
    "model": "model",
    "description": "",
    "driverModule": "og-driver-opcua-sub.js",
    "paramProfile": [
        {
            "paramId": "al1",
            "paramDesc": "al1",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=37",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al10",
            "paramDesc": "al10",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=46",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al11",
            "paramDesc": "al11",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=47",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al12",
            "paramDesc": "al12",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=48",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al13",
            "paramDesc": "al13",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=49",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al14",
            "paramDesc": "al14",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=50",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al15",
            "paramDesc": "al15",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=51",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al2",
            "paramDesc": "al2",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=38",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al3",
            "paramDesc": "al3",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=39",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al4",
            "paramDesc": "al4",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=40",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al5",
            "paramDesc": "al5",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=41",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al6",
            "paramDesc": "al6",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=42",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al7",
            "paramDesc": "al7",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=43",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al8",
            "paramDesc": "al8",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=44",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "al9",
            "paramDesc": "al9",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=45",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "bottleSize",
            "paramDesc": "bottleSize",
            "dataType": "String",
            "nodeId": "ns=2;i=16",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "bottleSizecounter",
            "paramDesc": "bottleSizecounter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=15",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons1",
            "paramDesc": "buttons1",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=67",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons10",
            "paramDesc": "buttons10",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=76",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons11",
            "paramDesc": "buttons11",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=77",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons12",
            "paramDesc": "buttons12",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=78",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons13",
            "paramDesc": "buttons13",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=79",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons14",
            "paramDesc": "buttons14",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=80",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons15",
            "paramDesc": "buttons15",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=81",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons2",
            "paramDesc": "buttons2",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=68",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons3",
            "paramDesc": "buttons3",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=69",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons4",
            "paramDesc": "buttons4",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=70",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons5",
            "paramDesc": "buttons5",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=71",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons6",
            "paramDesc": "buttons6",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=72",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons7",
            "paramDesc": "buttons7",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=73",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons8",
            "paramDesc": "buttons8",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=74",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "buttons9",
            "paramDesc": "buttons9",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=75",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "count",
            "paramDesc": "count",
            "dataType": "Int64",
            "nodeId": "ns=2;i=3",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "cycleTime",
            "paramDesc": "cycleTime",
            "dataType": "Int64",
            "nodeId": "ns=2;i=5",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "idealSpeed",
            "paramDesc": "idealSpeed",
            "dataType": "Double",
            "nodeId": "ns=2;i=36",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "operator",
            "paramDesc": "operator",
            "dataType": "String",
            "nodeId": "ns=2;i=18",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "operatorcounter",
            "paramDesc": "operatorcounter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=17",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par1",
            "paramDesc": "par1",
            "dataType": "Double",
            "nodeId": "ns=2;i=20",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par1counter",
            "paramDesc": "par1counter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=19",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par2",
            "paramDesc": "par2",
            "dataType": "String",
            "nodeId": "ns=2;i=22",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par2counter",
            "paramDesc": "par2counter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=21",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par3",
            "paramDesc": "par3",
            "dataType": "Double",
            "nodeId": "ns=2;i=24",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par3counter",
            "paramDesc": "par3counter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=23",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par4",
            "paramDesc": "par4",
            "dataType": "Double",
            "nodeId": "ns=2;i=26",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par4counter",
            "paramDesc": "par4counter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=25",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par5",
            "paramDesc": "par5",
            "dataType": "String",
            "nodeId": "ns=2;i=28",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par5counter",
            "paramDesc": "par5counter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=27",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par6",
            "paramDesc": "par6",
            "dataType": "Double",
            "nodeId": "ns=2;i=30",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par6counter",
            "paramDesc": "par6counter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=29",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par7",
            "paramDesc": "par7",
            "dataType": "Double",
            "nodeId": "ns=2;i=32",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par7counter",
            "paramDesc": "par7counter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=31",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par8",
            "paramDesc": "par8",
            "dataType": "Double",
            "nodeId": "ns=2;i=34",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "par8counter",
            "paramDesc": "par8counter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=33",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "prodId",
            "paramDesc": "prodId",
            "dataType": "String",
            "nodeId": "ns=2;i=14",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "prodIdcounter",
            "paramDesc": "prodIdcounter",
            "dataType": "Int64",
            "nodeId": "ns=2;i=13",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "realCycleTime",
            "paramDesc": "realCycleTime",
            "dataType": "Int64",
            "nodeId": "ns=2;i=35",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "scrap_broken",
            "paramDesc": "scrap_broken",
            "dataType": "Int64",
            "nodeId": "ns=2;i=11",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "scrap_generic",
            "paramDesc": "scrap_generic",
            "dataType": "Int64",
            "nodeId": "ns=2;i=9",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "scrap_label",
            "paramDesc": "scrap_label",
            "dataType": "Int64",
            "nodeId": "ns=2;i=8",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "scrap_manual",
            "paramDesc": "scrap_manual",
            "dataType": "Int64",
            "nodeId": "ns=2;i=12",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "scrap_shape",
            "paramDesc": "scrap_shape",
            "dataType": "Int64",
            "nodeId": "ns=2;i=7",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "scrap_vision",
            "paramDesc": "scrap_vision",
            "dataType": "Int64",
            "nodeId": "ns=2;i=10",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "scraps",
            "paramDesc": "scraps",
            "dataType": "Int64",
            "nodeId": "ns=2;i=4",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "state",
            "paramDesc": "state",
            "dataType": "Int64",
            "nodeId": "ns=2;i=6",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var1",
            "paramDesc": "var1",
            "dataType": "Double",
            "nodeId": "ns=2;i=82",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var10",
            "paramDesc": "var10",
            "dataType": "Double",
            "nodeId": "ns=2;i=91",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var2",
            "paramDesc": "var2",
            "dataType": "Double",
            "nodeId": "ns=2;i=83",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var3",
            "paramDesc": "var3",
            "dataType": "Double",
            "nodeId": "ns=2;i=84",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var4",
            "paramDesc": "var4",
            "dataType": "Double",
            "nodeId": "ns=2;i=85",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var5",
            "paramDesc": "var5",
            "dataType": "Double",
            "nodeId": "ns=2;i=86",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var6",
            "paramDesc": "var6",
            "dataType": "Double",
            "nodeId": "ns=2;i=87",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var7",
            "paramDesc": "var7",
            "dataType": "Double",
            "nodeId": "ns=2;i=88",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var8",
            "paramDesc": "var8",
            "dataType": "Double",
            "nodeId": "ns=2;i=89",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "var9",
            "paramDesc": "var9",
            "dataType": "Double",
            "nodeId": "ns=2;i=90",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn1",
            "paramDesc": "warn1",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=52",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn10",
            "paramDesc": "warn10",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=61",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn11",
            "paramDesc": "warn11",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=62",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn12",
            "paramDesc": "warn12",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=63",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn13",
            "paramDesc": "warn13",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=64",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn14",
            "paramDesc": "warn14",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=65",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn15",
            "paramDesc": "warn15",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=66",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn2",
            "paramDesc": "warn2",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=53",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn3",
            "paramDesc": "warn3",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=54",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn4",
            "paramDesc": "warn4",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=55",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn5",
            "paramDesc": "warn5",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=56",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn6",
            "paramDesc": "warn6",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=57",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn7",
            "paramDesc": "warn7",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=58",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn8",
            "paramDesc": "warn8",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=59",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        },
        {
            "paramId": "warn9",
            "paramDesc": "warn9",
            "dataType": "Boolean",
            "nodeId": "ns=2;i=60",
            "attributeId": "Value",
            "canChanged": False,
            "unit": "-"
        }
    ]
}

def getExampleConfig(output_path='config_example_matedge'):
    '''generate an example configuration, can be user as a starting point to create a project'''

    if os.path.isdir(output_path):
        shutil.rmtree(output_path)

    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    
    if not os.path.isdir(os.path.join(output_path, 'profiles')):
        os.mkdir(os.path.join(output_path, 'profiles'))

    pth_cld = os.path.join(output_path, 'cloudConfig.json')
    pth_bsw = os.path.join(output_path, 'configBsw.json')
    pth_ut = os.path.join(output_path, 'utils.json')
    prf_ut = os.path.join(os.path.join(output_path, 'profiles'), 'profile.json')

    with open(pth_cld, 'w') as wf:
        json.dump(cloud_config, wf, indent=4)

    with open(pth_bsw, 'w') as wf:
        json.dump(config_bsw, wf, indent=4)
    
    with open(pth_ut, 'w') as wf:
        json.dump(utils, wf, indent=4)
    
    with open(prf_ut, 'w') as wf:
        json.dump(profile, wf, indent=4)
    
    print('generated example input configuration')


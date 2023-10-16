import json
from datetime import datetime
import re, sys, os

import yaml



USE_NUM = False

class bswParser:

    def __init__(self, config_machine, station_name, profiles, config_path, password):

        self.config_machine = config_machine
        self.station_name = station_name
        self.config_path = config_path
        self.snapshot = config_machine['snapshot']
        self.utils_dp = []
        self.possible_inputs = self.getFeInputs(profiles)
        
        self.influx_pass = password

    def getFeInputs(self, profiles):
        inputs_ = []
        for k, v in profiles.items():
            for dp in v['paramProfile']:
                if dp['paramId'] not in inputs_:
                    inputs_.append(dp['paramId'])
                else:
                    print('ERROR: duplicated inputs in factoryedge "', dp['paramId'], '" IMPOSSIBLE to configure')
                    sys.exit()

        return inputs_
    
    def genSnapshot(self, asp_name):

        s = { "json": {
                "use_asp_name": True,
                "snapshot": True,
                "file_path": "mind",
                "snapshot_name": asp_name,
                "aspects_to_write": [
                    asp_name
                ]
            }
        }
        return s 
    
    def genInput(self, profiles):
        '''genera un generico input redis'''
        out = []
        for k,v in profiles.items():

            a = {
            "redis": {
                "hostname": "redis",
                "port": 6379,
                "channelData": "data-plc" + str(k),
                "username": None,
                "password": None,
                "db": 0,
                "keyStatus": "status-plc"+str(k),
                "sleeping_time": 0.1,
                "output_status": {
                    "kind": "print",
                    "topic": None,
                    "hostname": None,
                    "port": None,
                    "username": None,
                    "password": None
                }
            }
            }
            out.append(a)

        return out

    def addDp(self, dp):
        '''aggiungi datapoint nelle utils (datapoint da completare manualmente, globali per installazione)'''

        if dp.startswith('utils.'):
            p = {"name": dp.split('utils.')[1],
                 "type": "TODO",
                 "input_data": {},
                 "used_func": "TODO"}
            if p not in self.utils_dp:

                self.utils_dp.append(p)
        else:
            if dp not in self.possible_inputs:
                print('ERROR, you are trying to use datapoint "', dp, '" that is not in any factoryedge profile. IMPOSSIBLE to configure')
                sys.exit()
        return dp

    def addAggrTgs(self, list_, asp_name):
        '''aggiunge aggregati ai tag'''
        aggrs = self.config_machine['aggr']
        for n, a in enumerate(aggrs):
            list_.append(asp_name + '.aggr' + str(n))
        return list_

    def addAggr(self, list_, mode='actual'):
        '''aggiunge aggregati alla lista'''

        if mode == 'actual':
            aggrs = self.config_machine['aggr']
            for n, a in enumerate(aggrs):
                list_.append({
                    "name": "aggr"+str(n),
                    "type": "string",
                    "input_data": {
                            "var": self.addDp(a)
                    },
                    "used_func": "doNothing"
                })
        elif mode == 'pre':
            aggrs = self.config_machine['aggr']
            for n, a in enumerate(aggrs):
                list_.append({
                    "name": "aggr"+str(n),
                    "type": "string",
                    "input_data": {
                            "var": self.addDp(a)
                    },
                    "used_func": "doNothingPre"
                })

        return list_

    def genUtils(self, utils_dp):
        '''crea gli utils da riempire a mano'''

        utils_dp.append(
            {
                    "name": "hourclock",
                    "type": "boolean",
                    "input_data": {
                    },
                    "used_func": "hourclock"
                }
        )

        if len(utils_dp) == 0:
            return []
        if os.path.isfile(f'{self.config_path}/utils.json'):
            with open(f'{self.config_path}/utils.json') as rf:
                utils_from_file = json.load(rf)
        else:
            utils_from_file = []
        
        final_dp = []
        
        for n in utils_dp:
            if n['name'] in [u['name'] for u in utils_from_file]:
                util_target = [u for u in utils_from_file if u['name'] == n['name']][0]

                for k,v in util_target['input_data'].items():
                    if type(v) == dict:
                        continue
                    if k.endswith('_keyarg'):
                        continue
                    if not v.startswith('utils.'):
                        if v not in self.possible_inputs:
                            print('ERROR, you are trying to use datapoint "', v, '" in utils ', util_target['name'] , ' that is not in any factoryedge profile. IMPOSSIBLE to configure')
                            sys.exit()

                final_dp.append(util_target)
            else:
                final_dp.append(n)
                print('utils ', n['name'], 'to be manually configured.')
        

        aspect = {
            "name": "utils",
            "mapping_file": None,
            "first_write": False,
            "update": "never",
            "breakers": [],
            "datapoint": final_dp
        }

        
        

                
        print('total number is', len(utils_dp))
        return [aspect]

    def genRawData(self):
        '''genera aspect dei raw Data'''

        aspects = []
        outputs = []
        raw_data = self.config_machine['raws']

        for raw_payload in raw_data:
            sampling_time = raw_payload['sampling']
            datapoints = raw_payload['vars']

            if len(raw_data) == 1:
                post_name = ''
            else:
                post_name = str(sampling_time)

            dps = []

            if isinstance(datapoints, dict):
                for n, (datapoint, datatype) in enumerate(datapoints.items()):
                    dps.append({
                        "name": "var"+ str(self.station_name) +'_' + str(n),
                        "type": datatype,
                        "input_data": {
                                "var": self.addDp(datapoint)
                        },
                        "used_func": "doNothing"
                    })
            else:
                for n, datapoint in enumerate(datapoints):
                    dps.append({
                        "name": "var"+ str(self.station_name) +'_' + str(n),
                        "type": "double",
                        "input_data": {
                                "var": self.addDp(datapoint)
                        },
                        "used_func": "doNothing"
                    })
            
            
            if 'state' in self.config_machine.keys():
                dps.append(
                    {
                    "name": "state",
                    "type": "int",
                    "input_data": {
                            "var": self.addDp(self.config_machine['state']['var'])
                    },
                    "used_func": "doNothing"
                })


            aspect = {"name": "rawData" + post_name + self.station_name,
                      "mapping_file": None,
                      "first_write": False,
                      "update": int(sampling_time)/1000,
                      "breakers": [],
                      "datapoint": dps}

            output = {
                "influxdb": {
                    "tags": [
                    ],
                    "use_asp_name": False,
                    "host": "influxdb",
                    "port": 8086,
                    "username": "40f",
                    "password": self.influx_pass,
                    "ssl": False,
                    "database": "db0",
                    "measurement": "rawData" + post_name + self.station_name,
                    "retention_policy": {
                        "name": "retention_raw",
                        "days": 365
                    },
                    "continous_query": [
                    "5s", "2m", "1h"
                    ],
                    "aspects_to_write": [
                        "rawData" + post_name + self.station_name
                    ]
                }
            }

            if raw_payload['sendToMqtt'] == True:

                output_mqtt ={
                    "mqtt": {
                        "topic": "factoryedge/M1/mind",
                        "hostname": "eclipse-mosquitto",
                        "port": 1883,
                        "username": None,
                        "password": None,
                        "aspects_to_write": [
                            "rawData" + post_name + self.station_name
                        ]
                    }
                    }
                outputs.append(output_mqtt)


            aspects.append(aspect)
            outputs.append(output)

            if self.snapshot == True:
                snapshot = self.genSnapshot("rawData" + post_name + self.station_name)
                outputs.append(snapshot)
        
        return aspects, outputs

    def genAlarms(self):
        '''genera gli alarms'''

        aspects = []
        outputs = []

        states = self.config_machine['state']
        alarms = self.config_machine['alarms']
        aggrs = self.config_machine['aggr']

        faulty_state = states['faulty']
        state_var = states['var']

        # active Alarms

        dp = {"name": "alarmsResume",
              "type": "bool",
              "input_data": {
                  "path_keyarg": "activeAlarms/activeAlarms"+self.station_name + ".json",
                  "pathcopy_keyarg": "mind/activeAlarms"+self.station_name + ".json.tmp",
                  "states_keyarg": faulty_state,
                  "stateProd": self.addDp(state_var),
              },
              "used_func": "activeAlarmEdge"
              }
        for n, a in enumerate(aggrs):
            dp['input_data']['aggr'+str(n)] = self.addDp(a)

        for n, a in enumerate(alarms):
            number = re.search(r'\d+$', a)
            if number is not None and USE_NUM == True:
                dp['input_data']['al'+str(self.station_name)+'_'+str(number.group())] = self.addDp(a)
            else:
                dp['input_data']['al'+str(self.station_name)+'_'+str(n)] = self.addDp(a)

        aspect_active = {
            "name": "activeAlarms" + self.station_name,
            "mapping_file": None,
            "first_write": True,
            "update": "never",
            "breakers": [],
            "datapoint": [dp]}

        # history alarms

        dps = []
        dps = self.addAggr(dps)

        dps += [{
            "name": "code",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeAlarms" + self.station_name
                    },
            "used_func": "getCodeAlarmEdge"
        },
            {
            "name": "isFirst",
                    "type": "bool",
                    "input_data": {
                        "aspect_keyarg": "activeAlarms" + self.station_name
                    },
            "used_func": "getFirstAlarmEdge"
        },
            {
            "name": "duration",
                    "type": "double",
                    "input_data": {
                        "aspect_keyarg": "activeAlarms" + self.station_name
                    },
            "used_func": "getDurationAlarmEdge"
        }]

        aspect_history = {
            "name": "historyAlarm" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": {
                "write_if_up": {
                    "update_kind": 0,
                    "bool_name": "activeAlarms" + self.station_name+".alarmsResume"
                }
            },
            "breakers": [],
            "datapoint": dps}

        tgs = []
        tgs = self.addAggrTgs(tgs, "historyAlarm" + self.station_name)
        tgs.append("historyAlarm" + self.station_name + '.code')
        tgs.append("historyAlarm" + self.station_name + '.isFirst')

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "historyAlarm" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "aspects_to_write": [
                    "historyAlarm" + self.station_name
                ]
            }
        }

        aspects.append(aspect_history)
        aspects.append(aspect_active)
        outputs.append(output)

        return aspects, outputs

    def genBreak(self):
        '''genera i breakodwns'''

        aspects = []
        outputs = []

        states = self.config_machine['state']
        alarms = self.config_machine['alarms']
        aggrs = self.config_machine['aggr']

        faulty_state = states['faulty']
        external_state = states['external']
        state_var = states['var']

        mode = self.config_machine['breakdowns']['mode']
        params = self.config_machine['breakdowns']['params']

        # active Breakdowns

        dp = {"name": "statesResume",
              "type": "bool",
              "input_data": {
                  "stateProd": self.addDp(state_var),
                  "faults_keyarg": faulty_state + external_state,
                  "oldStateFile_keyarg": "persistence/old_state" + str(self.station_name) + ".json",
                  "alMode_keyarg": mode
                    },
              "used_func": "activeState"
              }

        for n, a in enumerate(alarms):
            number = re.search(r'\d+$', a)
            if number is not None  and USE_NUM == True:
                dp['input_data']['al'+str(self.station_name)+'_'+str(number.group())] = self.addDp(a)
            else:
                dp['input_data']['al'+str(self.station_name)+'_'+str(n)] = self.addDp(a)
        
        used_params = []
        for p, a in enumerate(params):
            dp['input_data']['param'+str(self.station_name)+'_'+str(p)] = self.addDp(a)
            used_params.append('param'+str(self.station_name)+'_'+str(p))


        aspect_active = {
            "name": "activeBreakdowns" + self.station_name,
            "mapping_file": None,
            "first_write": True,
            "update": "never",
            "breakers": [],
            "datapoint": [dp]}

        # history Breakdowns

        dps = []
        dps = self.addAggr(dps)

        for k,p in enumerate(used_params):
            dps.append(
                {
                    "name":  "param_" + str(k) + '_start',
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeBreakdowns" + self.station_name,
                        "param_keyarg" : p
                    },
                    "used_func": "getParamState"
                }
            )
            dps.append(
                {
                    "name":  "param_" + str(k) + '_end',
                    "type": "string",
                    "input_data": {
                        "var" : params[k]
                    },
                    "used_func": "doNothing"
                }
            )

        dps += [{
            "name": "triggerState",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeBreakdowns" + self.station_name
                    },
            "used_func": "getCodeState"
        },
            {
            "name": "cause",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeBreakdowns" + self.station_name
                    },
            "used_func": "getCauseState"
        },
            {
            "name": "duration",
                    "type": "double",
                    "input_data": {
                        "aspect_keyarg": "activeBreakdowns" + self.station_name,
                        "oldStateFile_keyarg": "persistence/old_state" + self.station_name + ".json"
                    },
            "used_func": "getDurationState"
        }]

        aspect_history = {
            "name": "historyBreakdown" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": {
                "write_if_up": {
                    "update_kind": 0,
                    "bool_name": "activeBreakdowns" + self.station_name+".statesResume"
                }
            },
            "breakers": [],
            "datapoint": dps}

        tgs = []
        tgs = self.addAggrTgs(tgs, "historyBreakdown" + self.station_name)
        tgs.append("historyBreakdown" + self.station_name + '.triggerState')
        tgs.append("historyBreakdown" + self.station_name + '.cause')

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "historyBreakdown" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "aspects_to_write": [
                    "historyBreakdown" + self.station_name
                ]
            }
        }

        aspects.append(aspect_history)
        aspects.append(aspect_active)
        outputs.append(output)

        return aspects, outputs

    def genWarnings(self):
        '''genera gli alarms'''

        aspects = []
        outputs = []
        states = self.config_machine['state']

        warnings = self.config_machine['warnings']
        aggrs = self.config_machine['aggr']

        faulty_state = []
        state_var = states['var']

        # active Alarms

        dp = {"name": "alarmsResume",
              "type": "bool",
              "input_data": {
                  "path_keyarg": "activeAlarms/activeWarnings"+self.station_name + ".json",
                  "pathcopy_keyarg": "mind/activeWarnings"+self.station_name + ".json.tmp",
                  "states_keyarg": None,
                  "stateProd": state_var,
              },
              "used_func": "activeAlarmEdge"
              }
        for n, a in enumerate(aggrs):
            dp['input_data']['aggr'+str(n)] = self.addDp(a)

        for n, a in enumerate(warnings):
            number = re.search(r'\d+$', a)
            if number is not None  and USE_NUM == True:
                ## se finisce in intero
                dp['input_data']['al_w'+str(self.station_name)+'_'+str(number.group())] = self.addDp(a)
            else:
                dp['input_data']['al_w'+str(self.station_name)+'_'+str(n)] = self.addDp(a)

        aspect_active = {
            "name": "activeWarnings" + self.station_name,
            "mapping_file": None,
            "first_write": True,
            "update": "never",
            "breakers": [],
            "datapoint": [dp]}

        # history alarms

        dps = []
        dps = self.addAggr(dps)

        dps += [{
            "name": "code",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeWarnings" + self.station_name
                    },
            "used_func": "getCodeAlarmEdge"
        },
            {
            "name": "duration",
                    "type": "double",
                    "input_data": {
                        "aspect_keyarg": "activeWarnings" + self.station_name
                    },
            "used_func": "getDurationAlarmEdge"
        }]

        aspect_history = {
            "name": "historyWarning" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": {
                "write_if_up": {
                    "update_kind": 0,
                    "bool_name": "activeWarnings" + self.station_name+".alarmsResume"
                }
            },
            "breakers": [],
            "datapoint": dps}

        tgs = []
        tgs = self.addAggrTgs(tgs, "historyWarning" + self.station_name)
        tgs.append("historyWarning" + self.station_name + '.code')

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "historyWarning" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "aspects_to_write": [
                    "historyWarning" + self.station_name
                ]
            }
        }

        aspects.append(aspect_history)
        aspects.append(aspect_active)
        outputs.append(output)

        return aspects, outputs

    def genButtons(self):
        '''aggiunge asepcts dei bottoni'''

        aspects = []
        outputs = []

        buttons = self.config_machine['buttons']

        # active buttons

        dp = {"name": "buttonsResume",
              "type": "bool",
              "input_data": {
              },
              "used_func": "getActiveButtons"
              }

        for n, a in enumerate(buttons):
            dp['input_data']['butt'+str(self.station_name)+'_'+str(n)] = self.addDp(a)

        aspect_active = {
            "name": "activeButtons" + self.station_name,
            "mapping_file": None,
            "first_write": True,
            "update": "never",
            "breakers": [],
            "datapoint": [dp]}

        # history buttons

        dps = []
        dps = self.addAggr(dps)

        dps += [{
            "name": "code",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeButtons" + self.station_name
                    },
            "used_func": "getIdButtons"
        },
            {
            "name": "timestamp",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeButtons" + self.station_name
                    },
            "used_func": "getTsButtons"
        }]

        aspect_history = {
            "name": "historyButton" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": {
                "write_if_up": {
                    "update_kind": 0,
                    "bool_name": "activeButtons" + self.station_name+".buttonsResume"
                }
            },
            "breakers": [],
            "datapoint": dps}

        tgs = []
        tgs = self.addAggrTgs(tgs, "historyButton" + self.station_name)
        tgs.append("historyButton" + self.station_name + '.code')

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "historyButton" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "aspects_to_write": [
                    "historyButton" + self.station_name
                ]
            }
        }

        aspects.append(aspect_history)
        aspects.append(aspect_active)
        outputs.append(output)

        return aspects, outputs

    def genRecipe(self):
        '''aggiunge aspects dei della ricetta'''

        aspects = []
        outputs = []

        recipe = self.config_machine['recipe']

        # active params

        

        dp = {"name": "paramsResume",
              "type": "bool",
              "input_data": {
              },
              "used_func": "paramTransition"
              }
            
        dps_raw = []

        if isinstance(recipe, dict):
            for n, (a, datatype) in enumerate(recipe.items()):
                number = re.search(r'\d+$', a)

                if number is not None  and USE_NUM == True:
                    dp['input_data']['param'+str(self.station_name)+'_'+str(number.group())] = self.addDp(a)
                    n = number.group()
                else:
                    dp['input_data']['param'+str(self.station_name)+'_'+str(n)] = self.addDp(a)

                dps_raw.append({
                    "name": "param"+ str(self.station_name) +'_' + str(n),
                    "type": datatype,
                    "input_data": {
                            "var": self.addDp(a)
                    },
                    "used_func": "doNothing"
                })
        else:
            for n, a in enumerate(recipe):
                number = re.search(r'\d+$', a)

                if number is not None  and USE_NUM == True:
                    dp['input_data']['param'+str(self.station_name)+'_'+str(number.group())] = self.addDp(a)
                    n = number.group()
                else:
                    dp['input_data']['param'+str(self.station_name)+'_'+str(n)] = self.addDp(a)

                dps_raw.append({
                    "name": "param"+ str(self.station_name) +'_' + str(n),
                    "type": "double",
                    "input_data": {
                            "var": self.addDp(a)
                    },
                    "used_func": "doNothing"
                })

        aspect_active = {
            "name": "activeParams" + self.station_name,
            "mapping_file": None,
            "first_write": True,
            "update": "on_var",
            "breakers": [],
            "datapoint": [dp]}
        
        aspect_raw = {
            "name": "rawDataParams" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": 10,
            "breakers": ["*"],
            "datapoint": dps_raw}


        # history params

        dps = []
        dps = self.addAggr(dps)

        dps += [{
            "name": "code",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeParams" + self.station_name
                    },
            "used_func": "getIdParamTrans"
        },
            {
            "name": "variationTime",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeParams" + self.station_name
                    },
            "used_func": "getTsParamTrans"
        },
        {
            "name": "from",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeParams" + self.station_name
                    },
            "used_func": "getFromParamTrans"
        },
        {
            "name": "to",
                    "type": "string",
                    "input_data": {
                        "aspect_keyarg": "activeParams" + self.station_name
                    },
            "used_func": "getToParamTrans"
        }]

        aspect_history = {
            "name": "historyParam" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": {
                "write_if_up": {
                    "update_kind": 0,
                    "bool_name": "activeParams" + self.station_name+".paramsResume"
                }
            },
            "breakers": [],
            "datapoint": dps}

        tgs = []
        tgs = self.addAggrTgs(tgs, "historyParam" + self.station_name)
        tgs.append("historyParam" + self.station_name + '.code')

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "historyParam" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "aspects_to_write": [
                    "historyParam" + self.station_name
                ]
            }
        }

        output_raw = {
            "influxdb": {
                "tags": [],
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "rawDataParams" + self.station_name,
                "retention_policy": {
                    "name": "retention_raw",
                    "days": 365
                },
                "continous_query": [
                    "5s", "2m", "1h"
                ],
                "aspects_to_write": [
                    "rawDataParams" + self.station_name
                ]
            }
        }

        aspects.append(aspect_history)
        aspects.append(aspect_active)
        aspects.append(aspect_raw)
        
        outputs.append(output)
        outputs.append(output_raw)

        if self.snapshot == True:
            snapshot = self.genSnapshot("rawDataParams" + self.station_name)
            outputs.append(snapshot)

        return aspects, outputs

    def genStateTrans(self):
        '''agggiunge l'aspect state transition'''

        aspects = []
        outputs = []

        state = self.config_machine['state']
        aggrs = self.config_machine['aggr']
        brk = []
        for n, a in enumerate(aggrs):
            brk.append("stateTransition" +
                       self.station_name + ".aggr" + str(n))

        brk.append("stateTransition" + self.station_name + ".state")

        dps = []
        dps = self.addAggr(dps)
        dps.append({
            "name": "state",
                    "type": "int",
                    "input_data": {
                        "var": self.addDp(state['var'])
                    },
            "used_func": "doNothing"
        })

        aspect = {
            "name": "stateTransition" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": 60,
            "breakers": brk,
            "datapoint": dps
        }
        tgs = []
        tgs = self.addAggrTgs(tgs, "stateTransition" + self.station_name)

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "stateTransition" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "aspects_to_write": [
                    "stateTransition" + self.station_name
                ]
            }
        }

        aspects.append(aspect)
        outputs.append(output)

        if self.snapshot == True:
            snapshot = self.genSnapshot("stateTransition" + self.station_name)
            outputs.append(snapshot)



        return aspects, outputs

    def genCycle(self):
        '''agggiunge l'aspect di history cycle'''

        aspects = []
        outputs = []

        state = self.config_machine['state']
        cycle_id = self.config_machine['cycle']['id']
        aux_var = self.config_machine['cycle']['aux_var']
        brk = []

        brk.append("historyCycle" + self.station_name + ".cycleIdPost")

        dps = []
        dps = self.addAggr(dps, mode='pre')

        dps.append(
            {
                "name": "cycleIdPost",
                "type": "string",
                "input_data": {
                    "var": self.addDp(cycle_id),
                    "stateProd" : self.addDp(state['var']),
                    "prodStates_keyarg" : state['productive']
                },
                "used_func": "getCycleId"
            }
        )

        dps.append(
            {
                "name": "cycleId",
                "type": "string",
                "input_data": {
                    "var": "historyCycle" + self.station_name + ".cycleIdPost",
                },
                "used_func": "doNothingPre"
            }
        )

        dps.append(
            {
                "name": "duration",
                "type": "double",
                "input_data": {
                },
                "used_func": "getDuration"
            }
        )

        for n,var in enumerate(aux_var):
            dps.append(
            {
                "name": "auxCycle" + str(n),
                "type": "infer",
                "input_data": {
                    "var": self.addDp(var)
                },
                "used_func": "doNothingPre"
            }
        )

        aspect = {
            "name": "historyCycle" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": "never",
            "breakers": brk,
            "datapoint": dps
        }
        tgs = []
        tgs = self.addAggrTgs(tgs, "historyCycle" + self.station_name)

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "historyCycle" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "aspects_to_write": [
                    "historyCycle" + self.station_name
                ]
            }
        }

        aspects.append(aspect)
        outputs.append(output)

        return aspects, outputs

    def genPhase(self):
        '''agggiunge l'aspect di history phase'''

        aspects = []
        outputs = []

        state = self.config_machine['state']
        phase_id = self.config_machine['phase']['id']
        aux_var = self.config_machine['phase']['aux_var']
        brk = []

        brk.append("historyPhase" + self.station_name + ".phaseIdPost")

        dps = []
        dps = self.addAggr(dps, mode='pre')

        dps.append(
            {
                "name": "phaseIdPost",
                "type": "string",
                "input_data": {
                    "var": self.addDp(phase_id),
                    "stateProd" : self.addDp(state['var']),
                    "prodStates_keyarg" : state['productive']
                },
                "used_func": "getCycleId"
            }
        )

        dps.append(
            {
                "name": "phaseId",
                "type": "string",
                "input_data": {
                    "var": "historyPhase" + self.station_name + ".phaseIdPost",
                },
                "used_func": "doNothingPre"
            }
        )

        dps.append(
            {
                "name": "cycleId",
                "type": "string",
                "input_data": {
                    "var": "historyCycle" + self.station_name + ".cycleId",
                },
                "used_func": "doNothingPre"
            }
        )

        dps.append(
            {
                "name": "duration",
                "type": "double",
                "input_data": {
                },
                "used_func": "getDuration"
            }
        )

        for n,var in enumerate(aux_var):
            dps.append(
            {
                "name": "auxCycle" + str(n),
                "type": "infer",
                "input_data": {
                    "var": self.addDp(var)
                },
                "used_func": "doNothingPre"
            }
        )

        aspect = {
            "name": "historyPhase" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": "never",
            "breakers": brk,
            "datapoint": dps
        }
        tgs = []
        tgs = self.addAggrTgs(tgs, "historyPhase" + self.station_name)

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "historyPhase" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "aspects_to_write": [
                    "historyPhase" + self.station_name
                ]
            }
        }

        aspects.append(aspect)
        outputs.append(output)

        return aspects, outputs

    def genAggr(self):
        '''creo aspect degli aggr Data'''
        aspects = []
        outputs = []

        state = self.config_machine['state']
        aggrs = self.config_machine['aggr']
        state_var = state['var']
        possible_val_state = state['possible_vals']
        prod_state = state['productive']
        faulty_state = state['faulty']
        other_state = [f for f in possible_val_state if f not in faulty_state]
        main_counter = self.config_machine['mainCounter']

        brk = []
        for n, a in enumerate(aggrs):
            brk.append(a)

        dps = []
        dps = self.addAggr(dps, 'pre')

        dps.append({
            "name": "timeFrom",
                    "type": "string",
                    "input_data": {},
                    "used_func": "getTimeFrom"
        })

        dps.append({
            "name": "timeTo",
                    "type": "string",
                    "input_data": {},
                    "used_func": "getTimeTo"
        })

        for state_val in possible_val_state:

            dps.append({
                "name": "timeState"+str(state_val),
                "type": "double",
                "input_data": {
                        "var": self.addDp(state_var),
                        "label_keyarg": int(state_val)
                },
                "used_func": "sumTimeLabel"
            })
        
        ### contatori totali, bad e goog

        dps.append({
            "name": "totCount",
                    "type": "double",
                    "scale": main_counter['scale'],
                    "input_data": {
                        "var": self.addDp(main_counter['id'])
                    },
            "used_func": "sumOfDiff"
        })

        if 'badCounter' in self.config_machine.keys():

            bad_counter = self.config_machine['badCounter']

            dps.append({
                "name": "badCount",
                "type": "double",
                "scale": bad_counter['scale'],
                "input_data": {
                        "var": self.addDp(bad_counter['id'])
                },
                "used_func": "sumOfDiff"
            })

            if 'goodCounter' not in self.config_machine.keys():

                dps.append({
                    "name": "goodCount",
                    "type": "double",
                    "scale": bad_counter['scale'],
                    "input_data": {
                        "minu": "aggrData" + self.station_name + ".totCount",
                        "sott": "aggrData" + self.station_name + ".badCount"
                    },
                    "used_func": "simpleDiff"
                })

        if 'goodCounter' in self.config_machine.keys():

            good_counter = self.config_machine['goodCounter']

            dps.append({
                "name": "goodCount",
                "type": "double",
                "scale": good_counter['scale'],
                "input_data": {
                        "var": self.addDp(good_counter['id'])
                },
                "used_func": "sumOfDiff"
            })

            if 'badCounter' not in self.config_machine.keys():

                dps.append({
                    "name": "badCount",
                    "type": "double",
                    "scale": good_counter['scale'],
                    "input_data": {
                        "minu": "aggrData" + self.station_name + ".totCount",
                        "sott": "aggrData" + self.station_name + ".goodCount"
                    },
                    "used_func": "simpleDiff"
                })
        
        ### numero di stops
        dps.append({
            "name": "stopCount",
                    "type": "int",
                    "input_data": {
                        "var": self.addDp(state_var),
                        "fromlist_keyarg": other_state,
                        "tolist_keyarg": faulty_state
                    },
            "used_func": "countTransition"
        })

        ### durata produttiva
        dps.append({
                    "name": "totDuration",
                    "type": "float",
                    "input_data": {
                        "var": self.addDp(state_var),
                        "listLabel_keyarg" : prod_state
                    },
                    "used_func": "sumTimeListLabel"
                })
        
        ### contatore ideale facoltativo
        if 'idealSpeed' in self.config_machine.keys():

            ideal_speed = self.config_machine['idealSpeed']
            
            dps.append({
                    "name": "idealSpeed",
                    "type": "float",
                    "scale" : ideal_speed['scale'],
                    "input_data": {
                        "var": self.addDp(ideal_speed['id'])
                    },
                    "used_func": "doNothing"})
            
            dps.append({
                    "name": "idealCount",
                    "type": "double",
                    "scale" : ideal_speed['scale'],
                    "input_data": {
                        "fact1": "aggrData" + self.station_name +".totDuration",
                        "fact2": "aggrData" + self.station_name +".idealSpeed"
                    },
                    "used_func": "simpleProd"}
                    )
        ## contatori generici
        if 'counters' in self.config_machine.keys():

            counters = self.config_machine['counters']
            for n,count in enumerate(counters):
                dps.append({
                "name": "count"+str(n),
                "type": "double",
                "scale": count['scale'],
                "input_data": {
                        "var": self.addDp(count['id'])
                },
                "used_func": "sumOfDiff"
                })

        ## contatori di scarto
        if 'scrapReasons' in self.config_machine.keys():

            scrapReasons = self.config_machine['scrapReasons']
            for n,count in enumerate(scrapReasons):
                dps.append({
                "name": "badCountReason"+str(n),
                "type": "double",
                "scale": count['scale'],
                "input_data": {
                        "var": self.addDp(count['id'])
                },
                "used_func": "sumOfDiff"
                })
        
        cons_count = 0
        ## consumabili generici da integrare
        if 'consIntegral' in self.config_machine.keys():

            cons_integral = self.config_machine['consIntegral']
            for count in cons_integral:
                dps.append({
                "name": "cons"+str(cons_count),
                "type": "double",
                "scale": count['scale'],
                "input_data": {
                        "var": self.addDp(count['id'])
                },
                "used_func": "absTimeIntegral"
                })
                cons_count += 1
        
        ## consumabili generici da sommare
        if 'consSum' in self.config_machine.keys():

            cons_sum = self.config_machine['consSum']
            for count in cons_sum:
                dps.append({
                "name": "cons"+str(cons_count),
                "type": "double",
                "scale": count['scale'],
                "input_data": {
                        "var": self.addDp(count['id'])
                },
                "used_func": "sumOfDiff"
                })
                cons_count += 1
        
        if 'buttons' in self.config_machine.keys():
            dps.append({
                    "name": "buttonsCount",
                    "type": "int",
                    "input_data": {
                        "var":  "activeButtons" + self.station_name +".buttonsResume",
                        "condition_keyarg": True
                    },
                    "used_func": "sumIfCond"}
                    )

        
        brk.append('utils.hourclock')
        aspect = {
            "name": "aggrData" + self.station_name,
            "mapping_file": None,
            "first_write": False,
            "update": 300,
            "breakers": brk,
            "datapoint": dps
        }

        tgs = []
        tgs = self.addAggrTgs(tgs, "aggrData" + self.station_name)

        output = {
            "influxdb": {
                "tags": tgs,
                "use_asp_name": False,
                "host": "influxdb",
                "port": 8086,
            #    "timeField" : "aggrData" + self.station_name + ".timeFrom",
                "username": "40f",
                "password": self.influx_pass,
                "ssl": False,
                "database": "db0",
                "measurement": "aggrData" + self.station_name,
                "retention_policy": {
                    "name": "retention_prod",
                    "days": 900
                },
                "continous_query": [
                    "30m"
                    ],
                "aspects_to_write": [
                    "aggrData" + self.station_name
                ]
            }
        }

        aspects.append(aspect)
        outputs.append(output)

        return aspects, outputs

#### classi per generazione dati in cloud

def s(name, path):
    if name.startswith(path): 
        return True
    else:
        return False

def getInfluxToJsonInputs(name):
    '''ottiene le informazioni necessarie all'influx to json a partire da un name
    invalid_types, precision, raw, keyAggr, aggregations, output_name '''

    if len(name.split('_')) == 1:
        machine = ''
    else:
        machine = '_' + name.split('_')[1]

    if s(name, 'aggrData'):
        return 'string', 'ms', '20D', 'time(1h)', ["time(30m)", "time(1h)", "time(1D)"], ["processData" + machine + "_{unixTS}"]
    
    elif s(name, 'historyAlarm'):
        return 'string', 'ms', 'time(10s)', None, ["time(30m)", "time(1D)"], ["alarms" + machine + "_{unixTS}"]
    
    elif s(name, 'historyWarning'):
        return 'string', 'ms', 'time(10s)', None, ["time(30m)", "time(1D)"], ["warnings" + machine + "_{unixTS}"]

    elif s(name, 'historyBreakdown'):
        return 'string', 'ms', 'time(10s)', None, ["time(30m)", "time(1D)"], ["breakdowns" + machine + "_{unixTS}"]
    
    elif s(name, 'stateTransition'):
        return None, 'ms', 'time(5m)', None, [], ["stateTransition" + machine + "_{unixTS}"]
    
    elif s(name, 'historyCycle'):
        return None, 'ms', "time(10s)", None, [], ["historyCycle" + machine + "_{unixTS}"]

    elif s(name, 'historyPhase'):
        return None, 'ms', "time(10s)", None, [], ["historyPhase" + machine + "_{unixTS}"]
    
    elif s(name, 'historyParam'):
        return None, 'ms', "time(5m)", None, [], ["historyParam" + machine + "_{unixTS}"]
    
    elif s(name, 'historyButton'):
        return None, 'ms', "time(5m)", None, [], ["historyButton" + machine + "_{unixTS}"]
    
    elif s(name, 'rawData'):
        return ["string", "boolean"], 'ms', "time(1s)", None, ["time(5s)", "time(2m)", "time(30m)","time(1h)"], [name + machine + "_{unixTS}"]

def genCloud(cloudConfig, bsw_outputs, influx_pass, output_path):

    if cloudConfig['active'] == True:
        if not os.path.isdir(f'{output_path}/EDGE/config/E2C'):
            os.mkdir(f'{output_path}/EDGE/config/E2C/')

        if not os.path.isdir(f'{output_path}/EDGE/config/E2C/factoryedge/'):
            os.mkdir(f'{output_path}/EDGE/config/E2C/factoryedge/')
        
        pth_cfg = f'{output_path}/EDGE/config/E2C/factoryedge/config.json'
        pth_itj = f'{output_path}/EDGE/config/E2C/influx-to-json/config.json'

        if not os.path.isdir(f'{output_path}/EDGE/config/E2C/influx-to-json/'):
            os.mkdir(f'{output_path}/EDGE/config/E2C/influx-to-json/')
        
        dev_name = cloudConfig['name']
        plat = cloudConfig['platform']

        if plat == 'azure':
            pubblisher = [
                    {
            "connectionString": "TODO: CONNECTION STRING TO BE COMPILED",
            "protocol": "mqttWs",
            "module": "og-pub-iothub.js",
            "fileSync": [
                {
                    "dir": "./sync/" + str(dev_name),
                    "skip": [
                        ".tmp"
                    ]
                },
                {
                    "dir": "./sync/" + str(dev_name) + "/rawPickles",
                    "cloudPath" : "pickles/",
                    "skip": [
                        ".tmp"
                    ]
                }
            ],
            "config": {
                "publishTime": 5000,
                "publishPolicy": {}
            },
            "wdtLimit": 720000,
            "datapoints": {}}]

        elif plat == 'mindsphere':

            pubblisher = [ {
                    "name": "mindconnect",
                    "module": "og-pub-mindconnect-2.js",
                    "wdtLimit": 720000,
                    "config": {
                        "dataSourceConfig": {
                        "configurationId": "ds",
                        "uploadFromAgent": True
                        },
                        "publishTime": 5000,
                        "publishPolicy": {
                        "M1": {}
                        }
                    },
                    "datapoints": {
                    },
                    "fileSync": [
                        {
                        "dir": "./sync/" + str(dev_name),
                        "skip": [
                            ".tmp"
                        ]
                        },
                        {
                            "dir": "./sync/" + str(dev_name) + "/rawPickles",
                            "cloudPath" : "pickles/",
                            "skip": [
                                ".tmp"
                            ]
                        }
                    ]
                    }
                ]

        fac_edge_conf = {
                "configId": "AUTOGEN",
                "lastModDate": str(datetime.utcnow()),
                "chunkSize": 100,
                "maxBufferSize": 10000,
                "dropBufferElements": 100,
                "persistentBuffer": False,
                "devices": [
                ],
                "publishers": pubblisher
                }

        with open(pth_cfg, 'w') as wf:
            json.dump(fac_edge_conf, wf, indent=4)
        
        measures = []

        for out in bsw_outputs:
            if list(out.keys())[0] == 'influxdb':
                name = out['influxdb']['measurement']
                tags = [t.split('.')[1] for t in out['influxdb']['tags']]
                ret = out['influxdb']['retention_policy']['name']

                invalid_types, precision, raw, keyAggr, aggregations, output_name = getInfluxToJsonInputs(name)

                p = {"policy": ret,
                    "name": name,
                    "primaryKeys": tags,
                    "invalidTypes": invalid_types,
                    "precision": precision,
                    "checkLast": "1m",
                    "structure": "auto",
                    "ext": "json",
                    "raw": raw,
                    "keysAggr": keyAggr,
                    "aggregations": aggregations,
                    "output": output_name}

                if invalid_types is None:
                    p.pop('invalidTypes', None)
                if keyAggr is None:
                    p.pop('keysAggr', None)

                measures.append(p
                    )



        influx_to_json = {
                "pollingTime": 30,
                "pollingTimeUpdater": 300,
                "ssl": False,
                "cachePath": "./cache/",
                "basePathTemp": [
                    "temp",
                    "{deviceId}"
                ],
                "basePathSync": [
                    "sync",
                    "{deviceId}"
                ],
                "clients": [{
                "redisData": {
                    "host": "redis",
                    "port": 6379,
                    "password": None,
                    "database": 0
                },
                "classesFile": dev_name,
                "tz": "Europe/Rome",
                "host": "influxdb",
                "port": 8086,
                "username": "40f",
                "database": "db0",
                "password": influx_pass,
                "deviceId": dev_name,
                "components": [
                ],
                "measurementsRaw": [],
                "measurements": measures
                }]
        }

        with open(pth_itj, 'w') as wf:
            json.dump(influx_to_json, wf, indent=4)

#### configurazione del factoryedge

def genFacEdgeConf(facedgenumber, profile_content, output_path):

    pth = f'{output_path}/EDGE/config/factoryedge{facedgenumber}/config.json'

    if 'opcua' in profile_content['driverModule']:

        cfg = {
            "configId": "autogen",
            "lastModDate": str(datetime.utcnow()),
            "redisHost": "redis",
            "redisPort": 6379,
            "brokerBusUrl": "mqtt://eclipse-mosquitto",
            "devices": [
                {
                    "name": "plc" + str(facedgenumber),
                    "profileId": "profile",
                    "driverConfig": {
                        "endpointUrl": "TODO Sopc.tcp://XXX.XXX.XXX.XXX:4840",
                        "userAuthentication": False,
                        "customCert": False,
                        "chunksize": 1000
                    },
                    "pollingTime": "TODO",
                    "wdtEnabled": True,
                    "wdtLimit": 30,
                    "redisIndex": 0
                }
            ],
            "publishers": []
        }
    
    elif 's7' in profile_content['driverModule']:

        cfg = {
            "configId": "autogen",
            "lastModDate": str(datetime.utcnow()),
            "redisHost": "redis",
            "redisPort": 6379,
            "devices": [
                {
                    "name": "plc" + str(facedgenumber),
                    "profileId": "profile",
                    "driverConfig": {
                        "host": "TODO xxx.xxx.xxx.xxx",
                        "port": 102,
                        "rack": 0,
                        "slot": 1
                    },
                    "pollingTime": "TODO",
                    "wdtEnabled": True,
                    "wdtLimit": 30,
                    "redisIndex": 0
                }
            ],
            "publishers": []
        }
 
    elif 'modbus' in profile_content['driverModule']:

        cfg = {
            "configId": "autogen",
            "lastModDate": str(datetime.utcnow()),
            "redisHost": "redis",
            "redisPort": 6379,
            "devices": [
                {
                    "name": "plc" + str(facedgenumber),
                    "profileId": "profile",
                    "driverConfig": {
                        "host": "TODO xxx.xxx.xxx.xxx",
                        "port": 502,
                        "timeout": 20000,
                        "id": 1,
                        "chunkSize": 120,
                        "byteOrder": "be",
                        "wordOrder": "be",
                        "maxSyncReaders": 3
                    },
                    "pollingTime": "TODO",
                    "wdtEnabled": True,
                    "wdtLimit": 30,
                    "redisIndex": 0
                }
            ],
            "publishers": []
            }


    print('configured factoryedge', facedgenumber, 'remember to edit PLC IP and polling time')
    with open(pth, 'w') as wf:
        json.dump(cfg, wf, indent=4)

### configurazione del docker compose

def genCompose(factoryedges, cloud_config, pass_influx, output_path):
    '''genera il docker compose'''

    doccomp = {'version': '2.4', 
               'services': 
               {'redis': {'container_name': 'redis', 'image': 'redis:5.0.10', 'restart': 'always', 'mem_limit': '256M', 'ports': ['6379:6379'], 'networks': ['mat']}, 
                'influxdb': {'container_name': 'influxdb', 'image': 'influxdb:1.8.2', 'restart': 'always', 'volumes': ['./dynamics/influxdb/data:/var/lib/influxdb'], 'environment': ['INFLUXDB_DB=db0', 'INFLUXDB_ADMIN_USER=40f', 'INFLUXDB_ADMIN_PASSWORD=<PASSWORD>', 'INFLUXDB_HTTP_AUTH_ENABLED=true', 'INFLUXDB_DATA_INDEX_VERSION=tsi1'], 'ports': ['8086:8086'], 'mem_limit': '2048M', 'networks': ['mat']}, 
                'eclipse-mosquitto': {'container_name': 'eclipse-mosquitto', 'image': 'eclipse-mosquitto:1.6.12', 'restart': 'always', 'mem_limit': '256M', 'ports': ['1883:1883', '1884:1884'], 'networks': ['mat']}, 
                'bsw': {'container_name': 'bsw', 'image': 'matcontainerregistry.azurecr.io/mat-edge-bsw:latest', 'init': True, 'restart': 'always', 'volumes': ['./config/bsw/config.json:/app/config.json', './config/bsw/mapping.json:/app/mapping.json', './config/bsw/customMethod/:/app/customMethod/', './dynamics/bsw/activeAlarms/:/app/activeAlarms/', './dynamics/E2C/factoryedge/sync/ASSETIDTOSUB/:/app/mind/', './dynamics/E2C/factoryedge/sync/ASSETIDTOSUB/rawPickles:/app/mind/rawPickles/', './dynamics/bsw/logs/:/app/logs/', './dynamics/bsw/persistence/:/app/persistence/'], 'mem_limit': '1024M', 'stop_grace_period': '5s', 'depends_on': ['redis', 'influxdb'], 'networks': ['mat']}, 
                'influx-to-json': {'container_name': 'influx-to-json', 'image': 'matcontainerregistry.azurecr.io/mat-bsw-edge-writer-mdsp:V1.1', 'restart': 'always', 'volumes': ['./config/E2C/influx-to-json/config.json:/app/config.json', './dynamics/E2C/influx-to-json/cache/:/app/cache/', './dynamics/E2C/influx-to-json/logs/:/app/logs/', './dynamics/E2C/influx-to-json/temp/:/app/temp/', './dynamics/E2C/json-to-npz/sync/:/app/sync/'], 'mem_limit': '256M', 'depends_on': ['influxdb'], 'networks': ['mat']}, 
                'json-to-npz': {'container_name': 'json-to-nz', 'image': 'matcontainerregistry.azurecr.io/mat-bsw-npz-edge:V1.2', 'restart': 'always', 'volumes': ['./config/E2C/influx-to-json/config.json:/app/config.json', './dynamics/E2C/json-to-npz/sync/:/app/sync/', './dynamics/E2C/json-to-npz/rotate/:/app/rotate/', './dynamics/E2C/factoryedge/sync/:/app/factoryedge/sync/', './dynamics/E2C/json-to-npz/tmp/:/app/factoryedge/tmp/', './dynamics/E2C/json-to-npz/logs/:/app/logs/'], 'environment': ['F40_ENVIROMENT=EDGE', 'F40_POLLING_TIME=20', 'F40_WORKER=writer'], 'mem_limit': '512M'},
                'factoryedge-E2C': {'container_name': 'factoryedge-E2C', 'image': 'matcontainerregistry.azurecr.io/factoryedge-e2azure:V1.1', 'restart': 'always', 'volumes': ['./config/E2C/factoryedge/config.json:/app/config.json', './config/E2C/factoryedge/profiles/:/app/profiles/', './dynamics/E2C/factoryedge/logs/:/app/logs/', './dynamics/E2C/factoryedge/temp/:/app/temp/', './dynamics/E2C/factoryedge/sync/:/app/sync/'], 'mem_limit': '512M', 'depends_on': ['eclipse-mosquitto'], 'networks': ['mat']}}, 'networks': {'mat': {'name': 'mat'}}}
    
    doccomp['services']['influxdb']['environment'] =  ['INFLUXDB_DB=db0', 'INFLUXDB_ADMIN_USER=40f', 'INFLUXDB_ADMIN_PASSWORD={}'.format(pass_influx), 'INFLUXDB_HTTP_AUTH_ENABLED=true', 'INFLUXDB_DATA_INDEX_VERSION=tsi1']
    doccomp = json.loads(json.dumps(doccomp).replace('ASSETIDTOSUB', cloud_config['name']))
    if cloud_config['active'] == False:
        doccomp['services'].pop('influx-to-json', None)
        doccomp['services'].pop('json-to-npz', None)
        doccomp['services'].pop('factoryedge-E2C', None)

    for fac in factoryedges:
        fac_ = {
            "container_name" : "factoryedge" + str(fac),
            "image" : "matcontainerregistry.azurecr.io/factoryedge-plc-mat:V1.0",
            "restart" : "always",
            "volumes" : [
                "./config/factoryedge{}/config.json:/app/config.json".format(str(fac)),
                "./config/factoryedge{}/profiles/:/app/profiles/".format(str(fac)),
                "/opt/mat/dynamics/factoryedge{}/logs/:/app/logs/".format(str(fac))

            ],
            "mem_limit" : "256M",
            "depends_on" : ["redis"],
            "networks" : ["mat"]
        }
        doccomp['services']['factoryedge'+str(fac)] = fac_

    with open(f'{output_path}/EDGE/docker-compose.yml', 'w') as wf:
        yaml.dump(doccomp, wf, indent=4)   

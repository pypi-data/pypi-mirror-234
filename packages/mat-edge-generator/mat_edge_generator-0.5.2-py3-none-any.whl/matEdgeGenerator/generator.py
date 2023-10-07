import json, os, shutil

from matEdgeGenerator.lib import bswParser, genFacEdgeConf, genCloud, genCompose


def generateConfiguration(config_path, output_path):


    ## carica configurazioni del bsw
    with open(f'{config_path}/configBsw.json') as rf:
        config = json.load(rf)

    ## carica profiles
    profiles = {}
    for k, profile in enumerate(os.listdir(f'{config_path}/profiles')):
        with open(os.path.join(f'{config_path}/profiles', profile)) as rf:
            profiles[str(k+1)] = json.load(rf)

    if os.path.isdir(f'{output_path}/EDGE/config/'):
        shutil.rmtree(f'{output_path}/EDGE/config/')
    if os.path.isfile(f'{output_path}/EDGE/docker-compose.yml'):
        os.remove(f'{output_path}/EDGE/docker-compose.yml')


    aspects = []
    outputs = []
    all_utils = []

    for id_machine, payload in config.items():

        if len(config.keys()) == 1:
            station_name = ''
        else:
            station_name = '_' + id_machine

        parser = bswParser(payload, station_name, profiles, config_path)
        


        ##### rawData
        if 'alarms' in payload.keys():
            aspects_als, outputs_als = parser.genAlarms()
            aspects += aspects_als
            outputs += outputs_als
        
        if 'breakdowns' in payload.keys():
            aspects_break, outputs_break = parser.genBreak()
            aspects += aspects_break
            outputs += outputs_break
        
        if 'warnings' in payload.keys():
            aspects_als, outputs_als = parser.genWarnings()
            aspects += aspects_als
            outputs += outputs_als
        
        if 'buttons' in payload.keys():
            aspects_als, outputs_als = parser.genButtons()
            aspects += aspects_als
            outputs += outputs_als
        
        if 'recipe' in payload.keys():
            aspects_als, outputs_als = parser.genRecipe()
            aspects += aspects_als
            outputs += outputs_als
        
        if 'state' in payload.keys():
            aspects_als, outputs_als = parser.genStateTrans()
            aspects += aspects_als
            outputs += outputs_als
        
        if 'mainCounter' in payload.keys():
            aspects_als, outputs_als = parser.genAggr()
            aspects += aspects_als
            outputs += outputs_als
        
        if 'cycle' in payload.keys():

            if 'phase' in payload.keys():
                aspects_phase, outputs_phase = parser.genPhase()
                aspects += aspects_phase
                outputs += outputs_phase
            aspects_cycle, outputs_cycle = parser.genCycle()
            aspects += aspects_cycle
            outputs += outputs_cycle

            

        
        if 'raws' in payload.keys():
            aspects_raw, outputs_raw = parser.genRawData()
            aspects += aspects_raw
            outputs += outputs_raw
        

        if len(parser.utils_dp) > 0:
            all_utils += parser.utils_dp

    all_utils_f = []
    for a in all_utils:
        if a not in all_utils_f:
            all_utils_f.append(a)

    aspect = parser.genUtils(all_utils_f)
    aspects+=aspect


    print('configuration completed:\n')
    print('\nRemember to check hosts for influxdb, redis and Mqtt')

    aspects.reverse()

    inputs = parser.genInput(profiles)

        
    final = {
        "input_info" : inputs,
        "output_info" : outputs,
        "aspects" : aspects,
        "general_param" : {
            "output_frequency": 5,
            "init_string": "",
            "generate_number_mapping": False,
            "truncate_len": 56,
            "log_info": "error",
            "verbose": True,
            "equalizer" : True,
            "dummyPickle": {
            "active": True,
            "destination": "mind/rawPickles/",
            "hourPeriod": 24
            },
            "persistence": {
                "active": False,
                "period": 120,
                "folder_path": "persistence",
                "time_tollerance": 7200
            }
        }
    }

    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    
    if not os.path.isdir(f'{output_path}/EDGE/'):
        os.mkdir(f'{output_path}/EDGE/')
    
    if not os.path.isdir(f'{output_path}/EDGE/config'):
        os.mkdir(f'{output_path}/EDGE/config')
    
    if not os.path.isdir(f'{output_path}/EDGE/config/bsw'):
        os.mkdir(f'{output_path}/EDGE/config/bsw')

    with open(f'{output_path}/EDGE/config/bsw/config.json', 'w') as wf:
        json.dump(final, wf, indent=4)

    for k, profile in profiles.items():
        if not os.path.isdir(f'{output_path}/EDGE/config/factoryedge'+ k):
            os.mkdir(f'{output_path}/EDGE/config/factoryedge'+ k)
            
        if not os.path.isdir(f'{output_path}/EDGE/config/factoryedge'+ k + '/profiles'):
            os.mkdir(f'{output_path}/EDGE/config/factoryedge'+ k + '/profiles')

        with open(f'{output_path}/EDGE/config/factoryedge'+ k + '/profiles/profile.json', 'w') as rf:
            json.dump(profile, rf, indent=4)
        
        genFacEdgeConf(k, profile, output_path)
    
    if os.path.isfile(f'{config_path}/cloudConfig.json'):
        with open(f'{config_path}/cloudConfig.json') as rf:
            cfg_cloud = json.load(rf)
        genCloud(cfg_cloud, outputs, parser.influx_pass, output_path)
    
    genCompose(profiles, cfg_cloud, parser.influx_pass, output_path)
        

#generateConfiguration(config_bsw, profiles)
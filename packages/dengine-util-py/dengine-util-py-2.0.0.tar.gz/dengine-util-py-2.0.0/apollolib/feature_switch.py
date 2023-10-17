import json

import apollolib

sd_balance_v2_namespace = 'sd-balance-v2'
config_toggle = 'config_toggle'

def get_feature_switch(feature_name):
    config = apollolib.client.get_config(sd_balance_v2_namespace, config_toggle)
    if config is None:
        return False

    feature_switch = config.get('feature_switch', '')
    if feature_switch is None:
        return False
    
    flag = json.loads(feature_switch)
    if flag[feature_name] is True:
        return True
    elif flag[feature_name] is False:
        return False
    else:
        return False

def get_rider_dispach_model_city_list():
    config = apollolib.client.get_config(sd_balance_v2_namespace, config_toggle)
    if config is None:
        return []

    city_list = config.get('rider_dispach_model_city_list', '[]')
    if city_list is None :
        return []

    return json.loads(city_list)

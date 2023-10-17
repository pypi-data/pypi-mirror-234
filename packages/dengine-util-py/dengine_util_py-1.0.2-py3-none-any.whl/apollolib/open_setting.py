from apollolib

OPEN_SETTING_NAME_SPACE = "sailing_open_setting_info"
OPEN_SETTING_CITY_CONFIG_NAME = "sailing_setting_city_info"
VIRTUAL_CITY_CONFIG_NAME = "virtual_city"


def get_enable_open_city_by_delivery_mode():
    """
    获取有效的配送模式开成城市列表，剔除虚拟和压测城市
    :return: key(String)=城市ID（eg：52090100），value(String)=国家编码（eg：MX）
    """
    # 虚拟和压测城市列表
    vp_cities = get_virtual_and_pressure_cities()

    # 获取开城列表，剔除非配送模式以及压测和虚拟城市
    config = apollolib.client.get_config(OPEN_SETTING_NAME_SPACE, OPEN_SETTING_CITY_CONFIG_NAME)
    city_to_country_dict = dict()
    for cityKey, cityInfo in config.items():
        if cityInfo.get("deliveryType") != 1:
            continue
        country_code = cityInfo.get("countryCode")
        city_id = cityKey.lstrip("city_")
        if city_id in vp_cities:
            continue
        city_to_country_dict[city_id] = country_code
    return city_to_country_dict


def get_virtual_and_pressure_cities():
    """
    获取虚拟城市列表.
    :return: key
    """
    config = apollolib.client.get_config(OPEN_SETTING_NAME_SPACE, VIRTUAL_CITY_CONFIG_NAME)
    city_to_country_dict = dict()
    for values in config.values():
        for country_code, cities in values.items():
            for city_id in cities:
                city_to_country_dict[city_id] = country_code
    return city_to_country_dict

import datetime
import json

from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from util import metric
from util.log import logger
from util.time import (get_hour_time_stamp, get_local_hour, get_time_stamp,
                       get_timezone_by_city_id, get_weekend)

from featurepalette.service import FeaturePalette

feature_palette_online_host = '10.14.128.13'
feature_palette_online_port = '30352'

feature_palette_test_host = '10.96.121.213'
feature_palette_test_port = '8790'

class FeaturePaletteClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = None

    def connect(self):
        transport = TSocket.TSocket(self.host, self.port)
        transport = TTransport.TFramedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = FeaturePalette.Client(protocol)
        transport.open()

    def disconnect(self):
        if self.client:
            transport = self.client._iprot.trans
            transport.close()
            self.client = None

    def get_feature_by_name(self, entity, group, key, ids, channel):
        """根据特征名获取特征

        Args:
            entity (string): 特征实体
            group (string): 特征组
            key (string): 特征名
            ids (list): 特征ID
            channel (int): 频道(0:线上 1:测试)

        Returns:
            dict: 特征结果
        """
        start_time = datetime.datetime.now()
        trace_info = {'caller':'sd-balance-strategy', 'callee':'featurepalette'}
        get_feature_name = FeaturePalette.FeatureName(Entity=entity, Group=group, Key=key)
        feature_req = FeaturePalette.GetFeatureByNameReq(ids, [get_feature_name], channel=channel)
        response = self.client.GetFeatureByName(trace_info, feature_req)
        if response.header.errno != 0:
            logger.error(
                "msg=FeaturePalette get_feature_by_name failed||traceID={}||errno={}||msg={}".format(
                    response.header.trace["traceid"],
                    response.header.errno, 
                    response.header.msg))
        else :
            logger.info(
                "msg=FeaturePalette get_feature_by_name success||traceID={}||errno={}||msg={}||value={}".format(
                    response.header.trace["traceid"],
                    response.header.errno, 
                    response.header.msg, 
                    response.Values))
        cost_time = int((datetime.datetime.now()-start_time).total_seconds()*1000)
        value_status = response.Values.get(ids[0])[':'.join([entity, group, key])].ValueStatus
        metric.count('get_feature_by_name.type', 1, {'featureKey':key, 'valueStatus': value_status})
        metric.rpc('get_feature_by_name.latency', cost_time)
        return response

    def update_feature_by_name(self, entity, group, id, key, value):
        """根据特征名更新特征

        Args:
            entity (string): 特征实体
            group (string): 特征组
            id (string): 特征ID
            key (string): 特征名
            value (string): 特征值

        Returns:
            dict: 更新结果
        """
        start_time = datetime.datetime.now()
        trace_info = {'caller':'sd-balance-strategy', 'callee':'featurepalette'}
        update_feature_name = {key: value}
        update_feature_req = FeaturePalette.UpdateFeatureReq(entity, group, id, update_feature_name, get_time_stamp())
        response = self.client.UpdateFeatureByName(trace_info, update_feature_req)
        if response.header.errno != 0:
            logger.error(
                "msg=FeaturePalette update_feature_by_name failed||traceID={}||errno={}||msg={}".format(
                    response.header.trace['traceid'], 
                    response.header.errno, 
                    response.header.msg))
        else :
            logger.info(
                "msg=FeaturePalette update_feature_by_name success||traceID={}||errno={}||msg={}".format(
                    response.header.trace['traceid'], 
                    response.header.errno, 
                    response.header.msg))
        cost_time = int((datetime.datetime.now()-start_time).total_seconds()*1000)
        metric.rpc('update_feature_by_name.latency', cost_time)
        return response

    def intert_feature_for_test_name(self, entity, group, id, key, value, channel, tickey, ttl):
        start_time = datetime.datetime.now()
        trace_info = {'caller':'sd-balance-strategy', 'callee':'featurepalette'}
        insert_feature_name = {key: value}
        insert_feature_req = FeaturePalette.InsertFeatureForTESTReq(Entity=entity, Group=group, ID=id, FeatureValueMap=insert_feature_name, timestamp=get_time_stamp(), ttlAddSecond=ttl, ticket=tickey, channel=channel)
        response = self.client.InsertFeatureForTESTByName(trace_info, insert_feature_req)
        if response.header.errno != 0:
            logger.error(
                "msg=FeaturePalette intert_feature_for_test_name failed||traceID={}||errno={}||msg={}".format(
                    response.header.trace['traceid'],
                    response.header.errno,
                    response.header.msg))
        else :
            logger.info(
                "msg=FeaturePalette intert_feature_for_test_name success||traceID={}||errno={}||msg={}".format(
                    response.header.trace['traceid'],
                    response.header.errno,
                    response.header.msg))
        cost_time = int((datetime.datetime.now()-start_time).total_seconds()*1000)
        metric.rpc('intert_feature_for_test_name.latency', cost_time)
        return response

    def get_q(self, city_id, channel):
        """获取城市时空价值特征

        Args:
            city_id (string): 城市ID
            channel (int): 频道

        Returns:
            string: 时空价值
        """
        # mock data
        # return json.dumps([{'from_hotzoneid': '192679248582',
        #     'from_hotzone_no': '52270100_22',
        #     'to_hotzoneid': '167966409395',
        #     'to_hotzone_no': '52270100_37',
        #     'value': 1.3,
        #     'reward': 1},
        #    {'from_hotzoneid': '169623159509',
        #     'from_hotzone_no': '52270100_0',
        #     'to_hotzoneid': '227001238209',
        #     'to_hotzone_no': '52270100_1',
        #     'value': 1.1,
        #     'reward': 1},
        #    {'from_hotzoneid': '169623159509',
        #     'from_hotzone_no': '52270100_0',
        #     'to_hotzoneid': '24403772137',
        #     'to_hotzone_no': '52270100_3',
        #     'value': 1.0,
        #     'reward': 1},
        #    {'from_hotzoneid': '169623159509',
        #     'from_hotzone_no': '52270100_0',
        #     'to_hotzoneid': '167966409395',
        #     'to_hotzone_no': '52270100_37',
        #     'value': 0.0,
        #     'reward': 1}])
        self.connect()
        timezone = get_timezone_by_city_id(city_id)
        object_id = '_'.join([city_id, str(get_weekend(timezone)),str(get_local_hour(timezone))])
        response = self.get_feature_by_name('city', 'SDrepositioning', 'q', [object_id], channel)
        self.disconnect()
        return response.Values.get(object_id)['city:SDrepositioning:q'].StrValue

    def get_pred_shortage(self, city_id, channel):
        """获取城市策略热区缺口

        Args:
            city_id (string): 城市ID
            channel (int): 频道

        Returns:
            string: 城市缺口
        """
        # mock data
        # return json.dumps(([{'hotzoneid': '167966409395',
        #        'avg': 2.91,
        #        'var': 1.2},
        #       {'hotzoneid': '192679248582',
        #        'avg': -4.3,
        #        'var': 1.0},
        #       {'hotzoneid': '169623159509',
        #        'avg': 2.4,
        #        'var': 3.0}
        #       ]))
        self.connect()
        object_id = city_id+'_'+str(get_hour_time_stamp())
        response = self.get_feature_by_name('city', 'supplyment', 'sdGap_hourly_fcst', [object_id], channel)
        self.disconnect()
        return response.Values.get(object_id)['city:supplyment:sdGap_hourly_fcst'].StrValue
    
    def get_hyperparameters(self, city_id, channel):
        """获取城市超参

        Args:
            city_id (string): 城市ID
            channel (int): 频道

        Returns:
            string: 城市超参
        """
        # mock data
        # return json.dumps([{'avg_threshold': 2,
        #             'var_threshold': 100,
        #             'insufficiency_prob': 0.5,
        #             'sufficiency_prob': 0.5,
        #             'receive_order_prob': 0.4
        #             }])
        self.connect()
        object_id = city_id
        response = self.get_feature_by_name('city', 'SDrepositioningParameters', 'parameters', [object_id], channel)
        self.disconnect()
        return response.Values.get(object_id)['city:SDrepositioningParameters:parameters'].StrValue
    
    def update_dispach_command(self, object_id, data):
        """更新策略热区调度方案

        Args:
            object_id (string): 特征ID
            data (string): 调度方案

        Returns:
            dict: 更新结果
        """
        self.connect()
        command = json.dumps(data)
        response = self.update_feature_by_name('sd-area', 'supplyment', object_id, 'rider_dispatch', command)
        self.disconnect()
        return response

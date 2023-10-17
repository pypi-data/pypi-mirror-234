from util.log import logger

from apollo.apollo import Apollo


class ApolloClient:
    _apolloInstance = None

    def __init__(self):
        if self._apolloInstance is None:
            apolloInstance = Apollo()
            inited, err_msg = apolloInstance.init()
            if not inited:
                logger.error("_sd_balance_strategy_apollo_init_failed||msg={}", err_msg)
                raise Exception("_sd_balance_strategy_apollo_init_failed, msg=" + err_msg)
            self._apolloInstance = apolloInstance

    def get_config(self, namespace, config_name):
        ret = self._apolloInstance.get_config(namespace, config_name)
        if not ret.is_valid():
            logger.warning("_sd_balance_strategy_apollo_get_config||namespace={}||configName={}||msg={}", namespace,
                            config_name, ret.get_err_msg())
            return
        return ret.get_all_values()

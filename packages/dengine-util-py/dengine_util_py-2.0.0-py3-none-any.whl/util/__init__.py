from util.metric import set_namespace
from util.service import get_cluster, get_service_name

set_namespace('collect.{0}.{1}'.format(get_cluster(), get_service_name()))

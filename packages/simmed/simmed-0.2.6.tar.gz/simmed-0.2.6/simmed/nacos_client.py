from concurrent.futures import ThreadPoolExecutor
import json
import socket
import time
import nacos
from pyctuator.pyctuator import Pyctuator
import simmed.config as config

executor = ThreadPoolExecutor(1)

# no auth mode
if config.NACOS_ENABLE:
    client = nacos.NacosClient(
        config.NACOS_ADDRESS, namespace=config.NAMESPACE)
# auth mode
# client = nacos.NacosClient(SERVER_ADDRESSES, namespace=NAMESPACE, username="nacos", password="nacos")


def get_local_ip():
    """
    查询本机ip地址
    :return:
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


if config.APP_ADDRESS is None:
    config.APP_ADDRESS = get_local_ip()


def regis_server_to_nacos(app):

    if not config.NACOS_ENABLE:
        return

    Pyctuator(
        app,
        config.APPNAME,
        app_url=f"http://{config.APP_ADDRESS}:{config.PORT}",
        pyctuator_endpoint_url=f"http://{config.APP_ADDRESS}:{config.PORT}/pyctuator",
        registration_url=None,
        app_description="Demonstrate Spring Boot Admin Integration with Flask",
    )

    client.add_naming_instance(config.APPNAME, config.APP_ADDRESS, str(
        config.PORT), cluster_name="", group_name=config.GROUP)
    executor.submit(send_heartbeat)


def send_heartbeat():
    while True:
        try:
            client.send_heartbeat(config.APPNAME, config. APP_ADDRESS,
                                  str(config.PORT), cluster_name="", group_name=config.GROUP)
        except Exception as ex:
            print("nacos send heartbeat exception:", ex)

        time.sleep(10)


def get_service_host(service_name, clusters=""):
    if not config.NACOS_ENABLE:
        return None

    ins_list = client.list_naming_instance(
        service_name, clusters, config.NAMESPACE, config.GROUP, True)["hosts"]
    # 多个实例需要考虑排序和权重
    if ins_list and len(ins_list) > 0:
        return "{}:{}".format(ins_list[0]['ip'], ins_list[0]['port'])
    return None


def get_config(evn_name):
    if not config.NACOS_ENABLE:
        return None

    config_str = client.get_config(data_id=config.APPNAME, group=config.GROUP)
    if not config_str:
        return None

    configlist = json.loads(config_str)
    if evn_name and evn_name in configlist:
        return configlist[evn_name]
    else:
        return configlist

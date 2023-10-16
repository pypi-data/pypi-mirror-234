import hashlib
import importlib
from itertools import groupby
import json
from operator import itemgetter
import uuid
from pymongo import MongoClient
import os
import random
import redis
from flask import request, g, redirect, Blueprint,  current_app
from flask_compress import Compress
from flask_cors import CORS
from flasgger import Swagger
import requests
from simmed.pymongos import ShardMongoClient
from simmed.zipkin import flask_start_zipkin, flask_stop_zipkin, set_tags, with_zipkin_request
from simmed.jsonencoder import Flask
from datetime import datetime

import logging
import simmed.nacos_client as nacos_client
import simmed.config as config


def init_flask_app(app_name: str = "", app_desc: str = ""):
    """_summary_

    初始化应用
    init: app, compress, nacos, zipkin, config

    Args:
        app_name (str): 服务名称
        app_desc (str): 服务描述

    Raises:
        Exception: 参数必须

    Returns:
        _type_: flask app
    """
    if app_name:
        config.APPNAME = app_name
    if app_desc:
        config.APPDESC = app_desc

    if not config.APPNAME or not config.APPDESC:
        raise Exception("APPNAME和APPDESC不能为空! 服务名称和服务描述,影响url路径。 ")

    current_path = os.getcwd()
    # print("current_path", current_path)

    app = Flask(__name__, static_folder=current_path+"/static",
                static_url_path="/static", template_folder=current_path+"/templates")

    app.config['COMPRESS_MIN_SIZE'] = 0
    Compress(app)
    Swagger(app)
    CORS(app, supports_credentials=True)

    nacos_client.regis_server_to_nacos(app)

    # 设置ncoas日志等级
    logging.getLogger("nacos").setLevel('ERROR')

    nacos_config = get_config(config.FLASK_ENV)
    if nacos_config:
        # 定义一个空的 Config 类，以便稍后更新配置
        class Config:
            pass
        app.config.from_object(Config)
        app.config.update(nacos_config)

        if 'ZIPKIN_HOST' in nacos_config:
            config.ZIPKIN_HOST = str(nacos_config['ZIPKIN_HOST'])
        if 'ZIPKIN_PORT' in nacos_config:
            config.ZIPKIN_PORT = int(nacos_config['ZIPKIN_PORT'])
        if 'ZIPKIN_SAMPLE_RATE' in nacos_config:
            config.ZIPKIN_SAMPLE_RATE = float(
                nacos_config['ZIPKIN_SAMPLE_RATE'])
        if 'ZIPKIN_ENABLE' in nacos_config:
            config.ZIPKIN_ENABLE = bool(nacos_config['ZIPKIN_ENABLE'])
        if 'LOG_ON' in nacos_config:
            config.LOG_ON = bool(nacos_config['LOG_ON'])
        if 'LOG_BY_MQ' in nacos_config:
            config.LOG_BY_MQ = bool(nacos_config['LOG_BY_MQ'])
        if 'LOG_LEVEL' in nacos_config:
            config.LOG_LEVEL = int(nacos_config['LOG_LEVEL'])

        if 'REDIS_HOST' in nacos_config:

            if "REDIS_PASSWORD" not in nacos_config:
                app.config['REDIS_STORE'] = redis.StrictRedis(host=nacos_config["REDIS_HOST"], port=int(
                    nacos_config["REDIS_PORT"]), decode_responses=True, encoding_errors='ignore')
            else:
                app.config['REDIS_STORE'] = redis.StrictRedis(host=nacos_config["REDIS_HOST"], port=int(
                    nacos_config["REDIS_PORT"]), password=nacos_config["REDIS_PASSWORD"], decode_responses=True, encoding_errors='ignore')

        if 'MONGO_HOST' in nacos_config:
            if "MONGO_SHARD" in nacos_config and int(nacos_config['MONGO_SHARD']) == 1:
                app.config['MONGOCLIENT_CONN'] = get_shard_mongo_connection(
                    nacos_config["MONGO_HOST"], int(nacos_config["MONGO_PORT"]), nacos_config["MONGO_USER"],
                    nacos_config["MONGO_PASSWORD"], nacos_config.get("MONGO_REPLICASET"))
            else:
                app.config['MONGOCLIENT_CONN'] = get_mongo_connection(
                    nacos_config["MONGO_HOST"], int(nacos_config["MONGO_PORT"]), nacos_config["MONGO_USER"],
                    nacos_config["MONGO_PASSWORD"], nacos_config.get("MONGO_REPLICASET"))

    @app.route('/')
    def index():
        return redirect('/apidocs')

    @app.route("/heartbeat", methods=['GET'])
    def heartbeat():
        """
        心跳
        ---
        tags: ['系统']
        responses:
            200:
                description: 成功返回 ok
        """
        return "ok"

    @app.route("/generatedoc", methods=['GET'])
    def generatedoc():
        """
        生成文档
        ---
        tags: ['系统']
        responses:
            200:
                description: 成功返回 success
        """
        file_path = "apispec_1.json"
        try:
            url = request.host_url+file_path
            result = requests.get(url).text
            swagger = json.loads(result)

        except Exception as ex:
            print("generateDoc exception:"+ex)

        apidoc = {
            "ModuleName": config.APPNAME,
            "ModuleText": config.APPDESC,
            "ModuleUrl": "api/"+config.APPNAME+"/{controller}",
            "Services": []
        }

        def get_params(swg, name=''):
            parameter = {
                "MaxLength": swg['max_length'] if 'max_length' in swg else 0,
                "Name":  name,
                "Text": swg['description'] if "description" in swg and swg['description'] else '',
                "TypeName": swg['type'] if "type" in swg else 'object',
                "Nullable":  "否" if 'required' in swg and swg['required'] else "是",
            }
            if not name:
                parameter['Name'] = parameter['TypeName']

            if 'properties' in swg:
                parameter['Properties'] = []
                for pro in swg['properties']:
                    parameter['Properties'].append(
                        get_params(swg['properties'][pro], pro))

            if 'items' in swg:
                parameter['TypeName'] = 'array'
                parameter['Properties'] = []
                parameter['Properties'].append(get_params(swg['items']))

            return parameter

        apis = []
        for path in swagger['paths']:
            if 'post' in swagger['paths'][path]:
                method = swagger['paths'][path]['post']

                if 'parameters' in method:

                    input_parameters = []
                    output_parameters = None
                    need_login = False

                    params = method['parameters']
                    for param in params:
                        param_in = param['in']
                        if param_in == "body" and 'schema' in param:
                            in_param = param['schema']['properties']['params']['items']
                            parameter = get_params(in_param)
                            input_parameters.append(parameter)
                        if param_in == "header" and param['name'] == 'WeAppAuthorization':
                            need_login = True

                    response_param = method['responses']['200']['schema']['properties']
                    if 'result' in response_param:
                        output_parameters = get_params(
                            response_param['result'])

                    m2 = hashlib.md5()
                    m2.update((path).encode("utf8"))
                    apiId = m2.hexdigest()

                    apis.append({
                        "ServiceName": path.split('/')[3].split('?')[0],
                        "ServiceText": method['tags'][0],
                        "Id": apiId,
                        "ApiName": path.split('=')[1],
                        "ApiText": method['summary'],
                        "LoginCheck": 1 if need_login else 0,
                        "NeedLogin": "是" if need_login else '否',
                        "ParentId": "0",
                        "InputParams": input_parameters,
                        "OutputParams": output_parameters
                    })

        apis.sort(key=itemgetter('ServiceName'))
        for ServiceName, items in groupby(apis, key=itemgetter('ServiceName')):
            items = list(items)
            m5 = hashlib.md5()
            m5.update((config.APPNAME+'/'+ServiceName).encode("utf8"))
            serviceId = m5.hexdigest()

            apidoc["Services"].append({
                "Id": serviceId,
                "ServiceName": ServiceName,
                "ServiceText": items[0]['ServiceText'],
                "Apis": items
            })

        result = rpc_rest_service("doc", "/api/doc/module", "Save", apidoc)
        logging.debug(result)
        return "success"

    @app.before_request
    def before():
        """
        针对app实例定义全局拦截器,开始请求
        """
        # print('request.endpoint', request.endpoint)
        # print('request.path', request.path)

        if request.endpoint not in ['static', 'flasgger.apispec_1', 'flasgger.apidocs'] and request.path not in ['/generatedoc', '/heartbeat']:

            flask_start_zipkin()

            requestCorpId = request.headers['request-corpid'] if 'request-corpid' in request.headers else ''
            weAppAuthorization = request.headers['weappauthorization'] if 'weappauthorization' in request.headers else ''
            clientName = request.headers['User-Agent'] if 'User-Agent' in request.headers else ''
            browserInfo = clientName.split('/')[0]

            rpc_method = str(request.method)
            if request.content_type == 'application/json':
                request_data = json.loads(request.data)
                rpc_method = request_data['method'] if 'method' in request_data else rpc_method

            set_zipkin_tags({
                "http.url":  str(request.url),
                "http.host":  str(request.host),
                "http.path": str(request.path),
                "req.requestCorpId": requestCorpId,
                "req.weAppAuthorization": weAppAuthorization,
                "req.clientName": clientName,
                "req.content.type": str(request.content_type),
                "req.method": rpc_method,
                "req.endpoint": str(request.endpoint),
                "req.client": str(request.remote_addr)
            })

            ClientRequestId = datetime.utcnow().strftime(
                '%Y%m%d%H%M%S%f')+'-'+uuid.uuid4().hex
            audit_info = {
                "ClientRequestId": str(request.args['ClientRequestId']) if 'ClientRequestId' in request.args else ClientRequestId,
                "BaseClientRequestId": str(
                    request.args['BaseClientRequestId']) if 'BaseClientRequestId' in request.args else None,
                "RequestCorpId": requestCorpId,
                "AppId": str(request.args['AppId']) if 'AppId' in request.args else None,
                "ActionUrl": str(request.url)[7:],
                "ModuleName": config.APPNAME,
                "ActionName": str(request.method),
                "ServiceName": str(request.path).split('/')[-1],
                "MethodName": rpc_method,
                "Parameters": str(request.data, 'utf8'),
                "BeginTime": datetime.now(),
                "ClientIpAddress": str(request.remote_addr),
                "ClientName": clientName,
                "BrowserInfo": browserInfo,
                "HasException": False
            }

            span = g.get('_zipkin_span')
            if span and span.zipkin_attrs:
                audit_info['ParentSpanId'] = span.zipkin_attrs.parent_span_id
                audit_info['SpanId'] = span.zipkin_attrs.span_id
                audit_info['TraceId'] = span.zipkin_attrs.trace_id
                audit_info['Sampled'] = span.zipkin_attrs.is_sampled
            g._audit_info = audit_info

        pass

    @app.after_request
    def after(response):
        """
        针对app实例定义全局拦截器,有异常不支持
        """
        if request.endpoint not in ['static', 'flasgger.apispec_1', 'flasgger.apidocs'] and request.path not in ['/generatedoc', '/heartbeat'] and response.content_type in ['text/html', 'text/xml', 'application/json']:
            if str(request.method).lower() == "post":
                logging.debug("api response: %s",
                              str(response.data, 'utf8'))
            audit_info = g.get('_audit_info')
            audit_info['Output'] = str(response.data, 'utf8')
        return response

    @app.teardown_request
    def teardown(exception):
        """
        针对app实例定义全局拦截器,忽略异常
        """
        if exception:
            log.error(exception)
        if request.endpoint not in ['static', 'flasgger.apispec_1', 'flasgger.apidocs'] and request.path not in ['/generatedoc', '/heartbeat']:
            audit_info = g.get('_audit_info')
            if audit_info is not None:
                audit_info['EndTime'] = datetime.now()
                duration = audit_info['EndTime'] - audit_info['BeginTime']
                audit_info['ExecutionDuration'] = duration.microseconds
                if exception:
                    logging.exception("api exception: %s", str(exception))
                    set_zipkin_tags({
                        "req.headers": str(request.headers).rstrip(),
                        "req.form": json.dumps(request.form),
                        "req.exception": str(exception)
                    })
                    audit_info['HasException'] = True
                    audit_info['Exception'] = str(exception)
                log_save('AuditInfo', json.dumps(
                    audit_info, ensure_ascii=False, indent=4, sort_keys=True, default=str))
            flask_stop_zipkin()
        pass

    if not current_app:
        ctx = app.app_context()
        ctx.push()

    # 动态添加模块
    if os.path.exists('apis'):

        for filename in os.listdir('apis'):

            if filename != ".DS_Store":

                blueprint_name = filename.replace(".py", "")
                module_name = "apis."+blueprint_name
                module = importlib.import_module(module_name)

                for name, blueprint in module.__dict__.items():
                    if isinstance(blueprint, Blueprint):
                        app.register_blueprint(blueprint)

    return app


def init_app_config(app_name: str = "", app_desc: str = ""):
    '''
    模拟一个 app.config
    :return:
    '''
    if app_name:
        config.APPNAME = app_name
    if app_desc:
        config.APPDESC = app_desc

    # 定义一个空的 Config 类，以便稍后更新配置
    class AppConfig:
        config = dict()

    app_config = AppConfig()
    nacos_config = get_config(config.FLASK_ENV)
    if nacos_config:

        # app.config.from_object(Config)
        app_config.config.update(nacos_config)

        if 'REDIS_HOST' in nacos_config:

            if "REDIS_PASSWORD" not in nacos_config:
                app_config.config['REDIS_STORE'] = redis.StrictRedis(host=nacos_config["REDIS_HOST"], port=int(
                    nacos_config["REDIS_PORT"]), decode_responses=True, encoding_errors='ignore')
            else:
                app_config.config['REDIS_STORE'] = redis.StrictRedis(host=nacos_config["REDIS_HOST"], port=int(
                    nacos_config["REDIS_PORT"]), password=nacos_config["REDIS_PASSWORD"], decode_responses=True,
                                                                     encoding_errors='ignore')

        if 'MONGO_HOST' in nacos_config:
            if "MONGO_SHARD" in nacos_config and int(nacos_config['MONGO_SHARD']) == 1:
                app_config.config['MONGOCLIENT_CONN'] = get_shard_mongo_connection(
                    nacos_config["MONGO_HOST"], int(nacos_config["MONGO_PORT"]), nacos_config["MONGO_USER"],
                    nacos_config["MONGO_PASSWORD"], nacos_config.get('MONGO_REPLICASET'))
            else:
                app_config.config['MONGOCLIENT_CONN'] = get_mongo_connection(
                    nacos_config["MONGO_HOST"], int(nacos_config["MONGO_PORT"]), nacos_config["MONGO_USER"],
                    nacos_config["MONGO_PASSWORD"], nacos_config.get('MONGO_REPLICASET'))

    return app_config

def set_zipkin_tags(tag):
    """_summary_
    保存zipkin链路标签日志
    Args:
        tag (_type_): dict()
    """
    set_tags(tag)


def get_config(env_name):
    """
    从nacos配置中心获取配置
    Args:
        env_name (_type_): 环境, 如: local_dev

    Returns:
        _type_: json object
    """
    if not env_name:
        env_name = config.FLASK_ENV
    return nacos_client.get_config(env_name)


def rpc_rest_service(service_name, api, method, *params):
    """
    服务rpc公共方法
    Returns:
        _type_: 1.json object, 2.error string
    """
    headers = {
        'Content-Type': 'application/json'
    }

    weAppAuthorization = request.headers['weappauthorization'] if request.headers and 'weappauthorization' in request.headers else ''
    if weAppAuthorization:
        headers['WeAppAuthorization'] = weAppAuthorization

    requests_json = {
        "id": str(random.randint(10000, 99999)),
        "jsonrpc": "2.0",
        "method": method,
        "params": params
    }

    set_zipkin_tags({
        "rpc.{}.api".format(requests_json["id"]): api,
        "rpc.{}.serviceName".format(requests_json["id"]): service_name,
        "rpc.{}.method".format(requests_json["id"]): method
    })

    host = nacos_client.get_service_host(service_name)
    if not host:
        set_zipkin_tags({
            "rpc.{}.error".format(requests_json["id"]): "注册中心未找到服务实例!"
        })
        print(service_name+"注册中心未找到服务实例")
        host = config.SERVER_HOST

    set_zipkin_tags({
        "rpc.{}.host".format(requests_json["id"]): host
    })
    body = json.dumps(requests_json, ensure_ascii=False,
                      indent=4, sort_keys=True, default=str)
    logging.debug("request:" + body)

    try:
        def func(req_headers):
            return requests.post(
                "http://{}{}".format(host, api), headers=req_headers,  data=body.encode("utf-8"))

        response = with_zipkin_request(func, headers)
        rsp_text = response.text
        result = json.loads(rsp_text.encode('utf8'))

        logging.debug("response:" + rsp_text)

        if "result" in result:
            return result["result"], None
        else:
            return None, result["error"]["message"] if "error" in result else result

    except Exception as ex:

        logging.exception("rpc exception:"+str(ex))
        set_zipkin_tags({
            "rpc.{}.params".format(requests_json["id"]): body if body else "None",
            "rpc.{}.exception".format(requests_json["id"]): str(ex)
        })
        return None, str(ex)


def log_save(logtype, logstr):
    if not config.LOG_ON:
        return

    if config.LOG_BY_MQ:
        '''
        通过MQ发送日志,待完善...
        '''
        pass
    else:
        rpc_rest_service("logs", "/api/logs/logsave", "SaveToMQ", json.dumps({
            "logType": logtype,
            "logStr": logstr
        }, ensure_ascii=False))


def get_mongo_connection(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD, replicaSet):
    """获取MongoDB连接"""
    if not MONGO_USER or not MONGO_PASSWORD:
        if replicaSet:
            conn = MongoClient(MONGO_HOST, MONGO_PORT, replicaset=replicaSet)
        else:
            conn = MongoClient(MONGO_HOST, MONGO_PORT)
        return conn
    else:
        uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
        if replicaSet:
            conn = MongoClient(uri, replicaset=replicaSet)
        else:
            conn = MongoClient(uri)
        return conn


def get_shard_mongo_connection(MONGO_HOST, MONGO_PORT, MONGO_USER, MONGO_PASSWORD, replicaset):
    """获取MongoDB分片集群连接"""
    if not MONGO_USER or not MONGO_PASSWORD:
        if replicaset:
            conn = ShardMongoClient(MONGO_HOST, MONGO_PORT, replicaset=replicaset)
        else:
            conn = ShardMongoClient(MONGO_HOST, MONGO_PORT)
        return conn
    else:
        uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
        if replicaset:
            conn = ShardMongoClient(uri, replicaset=replicaset)
        else:
            conn = ShardMongoClient(uri)
        return conn


class Log:
    """
    日志记录
    Trace 0,Debug 1,Information 2,Warning 3,Error 4,Critical 5
    """

    def trace(self, logstr):
        if config.LOG_LEVEL <= 0:
            logging.debug(logstr)
            log_save("Trace", logstr)

    def debug(self, logstr):
        if config.LOG_LEVEL <= 1:
            logging.debug(logstr)
            log_save("Debug", logstr)

    def info(self, logstr):
        if config.LOG_LEVEL <= 2:
            logging.info(logstr)
            log_save("Information", logstr)

    def warning(self, logstr):
        if config.LOG_LEVEL <= 3:
            logging.warn(logstr)
            log_save("Warning", logstr)

    def error(self, logstr):
        if config.LOG_LEVEL <= 4:
            logging.error(logstr)
            log_save("Error", logstr)

    def critical(self, logstr):
        if config.LOG_LEVEL <= 5:
            logging.critical(logstr)
            log_save("Critical", logstr)


log = Log()

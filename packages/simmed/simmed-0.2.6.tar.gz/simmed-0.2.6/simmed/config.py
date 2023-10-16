import os

env = os.environ.get

SERVER_HOST = env('SERVER_HOST', 'localhost')  # 服务总线，debug远程调试兼容模式

# zipkin
ZIPKIN_HOST = env('ZIPKIN_HOST', 'localhost')  # 配置中心获取
ZIPKIN_PORT = int(env('ZIPKIN_PORT', '9411'))
ZIPKIN_SAMPLE_RATE = float(env('ZIPKIN_SAMPLE_RATE', '100.0'))
ZIPKIN_ENABLE = env('ZIPKIN_ENABLE', 'True') == 'True'

# nacos
NACOS_ENABLE = env('NACOS_ENABLE', 'True') == 'True'
# APPNAME = env('APPNAME', 'specialdisease')
# APPDESC = env('APPDESC', '科研平台')
APPNAME = env('APPNAME', '')
APPDESC = env('APPDESC', '')
GROUP = env('GROUP', 'DEFAULT_GROUP')
NAMESPACE = env('NAMESPACE', '')  # 开发环境需要设置 local_dev
APP_ADDRESS = env('APP_ADDRESS', None)
NACOS_ADDRESS = env('NACOS_ADDRESS', 'localhost:8848')  # 通过环境变量获取

# flask
PORT = int(env('PORT', '5000'))
FLASK_ENV = env('FLASK_ENV', '')  # 通过环境变量获取，决定获取配置的组 local_dev

# logs
LOG_ON = env('LOG_ON', 'True') == 'True'
LOG_BY_MQ = env('LOG_BY_MQ', 'False') == 'True'
LOG_LEVEL = int(env('LOG_LEVEL', '0'))

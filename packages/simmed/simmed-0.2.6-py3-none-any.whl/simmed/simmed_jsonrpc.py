from jsonrpc import JSONRPCResponseManager


class SimMedError(Exception):
    def __init__(self, message, code: int = -1):
        super().__init__("{},{}".format(code, message))


class SimMedJSONRPCResponseManager:

    @classmethod
    def del_error(cls, response):
        if response.error and 'data' in response.error:

            if response.error['data']['type'] == 'SimMedError':
                msg = response.error['data']['message']
                response.error['code'] = int(msg[:msg.index(',')])
                response.error['message'] = msg[msg.index(',')+1:]
            else:
                response.error['message'] = response.error['data']['message']
            del response.error['data']

    @classmethod
    def handle_with_exception(cls, request_str, dispatcher, context=None):
        response = JSONRPCResponseManager.handle(
            request_str, dispatcher, context)

        if isinstance(response.data, list):
            for predata in response.responses:
                cls.del_error(predata)
        else:
            cls.del_error(response)

        return response

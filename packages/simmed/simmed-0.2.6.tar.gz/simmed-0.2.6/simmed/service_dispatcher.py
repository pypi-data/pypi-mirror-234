from jsonrpc import Dispatcher


def get_dispatcher(app, path, serviceObj):

    dispatcher = Dispatcher()
    method_list = [method for method in dir(
        serviceObj.__class__) if method.startswith('__') is False]

    for method in method_list:
        view_func = getattr(serviceObj, method)
        dispatcher.add_method(view_func)
        app.add_url_rule(path+"?method="+method,
                         view_func=view_func, methods=["POST"])
    return dispatcher

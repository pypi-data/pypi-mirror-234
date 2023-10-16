from datetime import date, datetime

from pydantic import BaseModel
from pydantic.fields import Undefined
from typing import get_origin, get_args
from flasgger import swag_from
import typing
from simmed.rpcrequest import RpcRequest
from simmed.rpcresponse import RpcResponse


def get_field_type_str(typeinfo):
    '''获取swagger属性类型'''

    if typeinfo == object:
        return 'object'
    elif typeinfo == str:
        return 'string'
    elif typeinfo == int:
        return 'integer'
    elif typeinfo == bool:
        return 'boolean'
    elif typeinfo == list:
        return 'array'
    elif typeinfo == dict:
        return 'object'
    else:
        return ''


def get_schema(cls):
    '''获取类型结构,生成swagger文档属性'''

    if not cls:
        return None

    schema = {
        'description': cls.__doc__ if cls.__doc__ is not None else ''
    }

    if cls in [object, str, int, bool]:
        schema['type'] = get_field_type_str(cls)
        schema['description'] = ''
        return schema

    fields = {}
    required = []
    type_hints = typing.get_type_hints(cls)

    for field_name, model_field in cls.__fields__.items():

        field_info = model_field.field_info
        field_type = type_hints.get(field_name, None)

        fields[field_name] = {
            'type': get_field_type_str(field_type),
            'description': field_info.description
        }

        if get_origin(field_type) is list:

            fields[field_name]['type'] = 'array'
            args = get_args(field_type)
            if len(args) > 0:
                in_type = args[0]
                # 嵌套一个BaseModel类型
                if issubclass(in_type, BaseModel):
                    fields[field_name]['items'] = {
                        'type': 'object',
                        'description': in_type.__doc__ if in_type.__doc__ is not None else ''
                    }
                else:
                    fields[field_name]['items'] = {
                        'type': get_field_type_str(in_type),
                        'description': field_info.description
                    }
                if in_type != cls:
                    tmp_schema = get_schema(in_type)
                    if 'properties' in tmp_schema:
                        fields[field_name]['items']['properties'] = tmp_schema['properties']

        elif get_origin(field_type) is dict:
            fields[field_name]['type'] = 'object'

        else:

            if issubclass(field_type, BaseModel):
                fields[field_name]['type'] = 'object'
                tmp_schema = get_schema(field_type)
                if 'properties' in tmp_schema:
                    fields[field_name]['properties'] = tmp_schema['properties']

        if 'required' in field_info.extra and field_info.extra['required']:
            required.append(field_name)
            fields[field_name]['required'] = field_info.extra['required']

        if field_info.default and field_info.default != Undefined and isinstance(field_info.default, tuple) is False:
            fields[field_name]['example'] = field_info.default

        if field_info.min_length:
            fields[field_name]['min_length'] = field_info.min_length

        if field_info.max_length:
            fields[field_name]['max_length'] = field_info.max_length

    schema['properties'] = fields
    schema['required'] = required
    return schema


def get_swagger(method, request_cls, response_cls, title='', description='', tags=[], validation=True, needlogin=True):

    rpc_request_base = get_schema(RpcRequest)
    rpc_response_base = get_schema(RpcResponse)

    request_schema = get_schema(request_cls)
    response_schema = get_schema(response_cls)

    rpc_request_base['properties']['method']['example'] = method
    if request_schema:
        rpc_request_base['properties']['params']['items'] = request_schema
    else:
        raise Exception("json-rpc不支持无参请求接口!")

    if response_schema:
        rpc_response_base['properties']['result'] = response_schema

    doc = {
        'summary': title,
        'description': description if description else title,
        'tags': tags,
        # 'security': {'basicAuth': []},
        'parameters':  [{
            'in': 'body',
            'required': True,
            'type': 'object',
            'description': RpcRequest.__doc__,
            'schema': rpc_request_base
        }],
        'responses': {
            '200': {
                'description': RpcResponse.__doc__,
                'schema': rpc_response_base
            }
        }
    }

    if needlogin:
        doc['parameters'].append({
            'in': 'header',
            'name': 'WeAppAuthorization',
            'required': True,
            'type': 'string',
            'description': '登陆SessionKey'
        })

    return swag_from(doc, validation=validation)


def get_validate_schema(cls):
    '''获取类型校验schame'''

    if not cls:
        return None

    if cls in [object, str, int, bool, bytearray, bytes, date, datetime, float, set]:
        return {
            'type': get_validate_field_type_str(cls)
        }

    schema = {}
    type_hints = typing.get_type_hints(cls)

    for field_name, model_field in cls.__fields__.items():

        field_info = model_field.field_info
        field_type = type_hints.get(field_name, None)

        schema[field_name] = {
            'type': get_validate_field_type_str(field_type)
        }

        if get_origin(field_type) is list:

            schema[field_name]['type'] = 'list'
            args = get_args(field_type)
            if len(args) > 0:
                in_type = args[0]
                if in_type != cls:
                    tmp_schema = get_validate_schema(in_type)
                    if issubclass(in_type, BaseModel) or get_origin(in_type) is dict:
                        schema[field_name]['schema'] = {
                            'type': 'dict',
                            'schema': tmp_schema
                        }
                    else:
                        schema[field_name]['schema'] = tmp_schema

        elif get_origin(field_type) is dict:
            schema[field_name]['type'] = 'dict'
            schema[field_name]['allow_unknown'] = True

        else:
            if issubclass(field_type, BaseModel):
                schema[field_name]['type'] = 'dict'
                schema[field_name]['schema'] = get_validate_schema(field_type)

        # if 'required' in field_info.extra and field_info.extra['required']:
        #     schema[field_name]['required'] = field_info.extra['required']

        if field_info.ge is not None or field_info.gt is not None:
            schema[field_name]['min'] = field_info.ge if field_info.ge else field_info.gt

        if field_info.le is not None or field_info.lt is not None:
            schema[field_name]['max'] = field_info.le if field_info.le else field_info.lt

        # str约束min_length list约束min_items  cerberus不区分list与str类型field_info区分
        if field_info.min_length is not None or field_info.min_items is not None:
            schema[field_name]['minlength'] = field_info.min_length if field_info.min_length else field_info.min_items

        if field_info.max_length is not None or field_info.max_items is not None:
            schema[field_name]['maxlength'] = field_info.max_length if field_info.max_length else field_info.max_items

        if field_info.regex:
            schema[field_name]['regex'] = field_info.regex

        if field_info.extra:
            for extra_key, extra_value in field_info.extra.items():
                if extra_key in schema[field_name]:
                    continue
                schema[field_name][extra_key] = extra_value

    return schema


def get_validate_field_type_str(typeinfo):
    '''获取校验属性类型'''

    if typeinfo == bool:
        return 'boolean'
    elif typeinfo == bytearray or typeinfo == bytes:
        return 'binary'
    elif typeinfo == date:
        return 'date'
    elif typeinfo == datetime:
        return 'datetime'
    elif typeinfo == dict or typeinfo == object:
        return 'dict'
    elif typeinfo == float:
        return 'float'
    elif typeinfo == int:
        return 'integer'
    elif typeinfo == list:
        return 'list'
    elif typeinfo == set:
        return 'set'
    elif typeinfo == str:
        return 'string'
    else:
        return ''

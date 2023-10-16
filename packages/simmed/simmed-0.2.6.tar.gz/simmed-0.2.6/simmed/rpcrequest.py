from pydantic import BaseModel, Field
from typing import List


class RpcRequest(BaseModel):
    '''JSON-PRC请求'''
    id: str = Field(default='1', description='请求Id', required=True)
    jsonrpc: str = Field(
        default='2.0', description='JSON-PRC版本', required=True)
    method: str = Field(default='', description='方法签名', required=True)
    params: List[object] = Field(default=[], description='请求参数', required=True)

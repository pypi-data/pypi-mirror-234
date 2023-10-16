from pydantic import BaseModel, Field


class RpcResponse(BaseModel):
    '''JSON-PRC响应'''
    id: str = Field(default='1', description='请求Id', required=True)
    jsonrpc: str = Field(
        default='2.0', description='JSON-PRC版本', required=True)

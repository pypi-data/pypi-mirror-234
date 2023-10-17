import ujson
from fastapi.routing import serialize_response
from typing import Dict, List, Optional, Any
from aiohttp import JsonPayload


async def unzip_body_object(
    all_params: Dict[str, Any],
    necessary_params: Optional[Dict[str, str]] = None,
) -> Optional[JsonPayload]:
    if necessary_params:
        total_body = len(necessary_params)
        response_body_dict = {}
        for key in necessary_params.keys():
            value = all_params.get(key)
            _body_dict = await serialize_response(response_content=value)
            if (type(_body_dict) == dict or type(_body_dict) == list) and total_body > 1:
                response_body_dict.update({key: _body_dict})
            elif type(_body_dict) == dict:
                response_body_dict.update(_body_dict)
            elif type(_body_dict) == list:
                response_body_dict = _body_dict
            elif type(_body_dict) == str:
                response_body_dict.update({key: _body_dict})
        return JsonPayload(value=response_body_dict, dumps=ujson.dumps)
    return None

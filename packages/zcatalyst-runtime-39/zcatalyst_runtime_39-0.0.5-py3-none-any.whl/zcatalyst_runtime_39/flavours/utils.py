import json

from flask import request, g

def get_catalyst_headers() -> dict:
    catalyst_headers = {}
    for header in request.headers.keys():
        header_lower = header.lower()
        if header_lower.startswith('x-zc-'):
            catalyst_headers[header] = request.headers.get(header)

    return catalyst_headers

def get_catalyst_body() -> dict:
    catalyst_body = request.get_data()
    return json.loads(catalyst_body) if catalyst_body else {}

def send_json_response(status_code: int, message: dict = None) -> None:
    g.response.status_code = status_code

    if message:
        g.response.content_type = 'application/json; charset=utf-8'
        g.response.mimetype = 'application/json'

        message_str = json.dumps(message)
        g.response.set_data(message_str)


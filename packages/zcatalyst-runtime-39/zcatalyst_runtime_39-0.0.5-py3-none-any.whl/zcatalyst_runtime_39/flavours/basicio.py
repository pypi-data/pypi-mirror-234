import os
import time
import logging

from flask import request, g

from flavours import FlavourHandler
from flavours.utils import get_catalyst_body, send_json_response

class Context:
    __max_execution_time_ms = int(os.getenv('CATALYST_MAX_TIMEOUT', -1))
    __logger = logging.getLogger()

    def __init__(self) -> None:
        max_execution_buffer_time_ms = 500
        max_execution_hidden_time_ms = self.__max_execution_time_ms - max_execution_buffer_time_ms

        self.__endtime_timestamp = int(time.time() * 1000) + max_execution_hidden_time_ms
        
    def close(self) -> None:
        # `send_json_response` will be called in `init.py`.
        pass

    def log(self, *args):
        Context.__logger.info(*args)

    def get_remaining_execution_time_ms(self):
        time_remaining = self.__endtime_timestamp - int(time.time() * 1000)
        return 0 if time_remaining < 0 else time_remaining

    def get_max_execution_time_ms(self):
        return Context.__max_execution_time_ms

class BasicIO:
    def __init__(self) -> None:
        self.__request_body = get_catalyst_body()
        self.__query_string = request.args.to_dict()

    def get_argument(self, key: str):
        return self.__request_body.get(key) or self.__query_string.get(key)

    def get_all_arguments(self):
        arguments = self.__request_body.copy()
        arguments.update(self.__query_string)

        return arguments

    def set_status(self, status_code: int):
        g.response.status_code = status_code

    def write(self, message: str):
        g.response.set_data(g.response.get_data(as_text=True) or '' + message)

class BasicIOHandler(FlavourHandler):
    def construct_function_parameters():
        return (Context(), BasicIO())

    def return_error_response(error):
        send_json_response(500, { 'error': error })
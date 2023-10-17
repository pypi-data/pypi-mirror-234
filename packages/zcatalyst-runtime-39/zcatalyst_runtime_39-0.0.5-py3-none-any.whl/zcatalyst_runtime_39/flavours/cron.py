import os
import time

from flavours import FlavourHandler
from flavours.utils import get_catalyst_body, send_json_response

class CronDetails:
    def __init__(self) -> None:
        self.__catalyst_body = get_catalyst_body()

    def get_cron_param(self, key):
        data = self.__catalyst_body.get('data')
        return data.get(key) if data else None

    def get_all_cron_params(self):
        return self.__catalyst_body.get('data')

    def get_remaining_execution_count(self):
        return self.__catalyst_body.get('remaining_count')

    def get_cron_details(self):
        return self.__catalyst_body.get('cron_details')

    def get_project_details(self):
        return self.__catalyst_body.get('project_details')

class Context():
    __max_execution_time_ms = int(os.getenv('CATALYST_MAX_TIMEOUT', -1)) 

    def __init__(self) -> None:
        max_execution_buffer_time_ms = 500
        max_execution_hidden_time_ms = self.__max_execution_time_ms - max_execution_buffer_time_ms

        self.__endtime_timestamp = int(time.time() * 1000) + max_execution_hidden_time_ms

    def close_with_success(self):
        send_json_response(200)

    def close_with_failure(self):
        send_json_response(530)

    def get_remaining_execution_time_ms(self):
        time_remaining = self.__endtime_timestamp - int(time.time() * 1000)
        return 0 if time_remaining < 0 else time_remaining

    def get_max_execution_time_ms(self):
        return Context.__max_execution_time_ms


class CronHandler(FlavourHandler):
    def construct_function_parameters():
        return (CronDetails(), Context())

    def return_error_response(error):
        send_json_response(532, { 'error': error })
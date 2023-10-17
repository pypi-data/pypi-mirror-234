import os
import json
import threading
from importlib.util import spec_from_file_location, module_from_spec

from flask import g

from init_handler import InitHandler
from flavours.utils import get_catalyst_headers, send_json_response

CUSTOMER_CODE_ENTRYPOINT = None

class FlavourHandler:
    def __init__(self) -> None:
        with open(InitHandler.get_code_location().joinpath('catalyst-config.json'), 'r') as config_file:
            catalyst_config = json.loads(config_file.read())
            entry_point = catalyst_config['execution']['main'] or 'main.py'
            self.__entrypoint = InitHandler.get_code_location().joinpath(entry_point)
            self.__flavour = os.getenv('CATALYST_FUNCTION_TYPE', catalyst_config['deployment']['type'])

    def __get_flavour(self):
        if self.__flavour == 'basicio':
            from flavours.basicio import BasicIOHandler
            return BasicIOHandler
        elif self.__flavour == 'applogic' or self.__flavour == 'advancedio':
            from flavours.applogic import ApplogicHandler
            return ApplogicHandler
        elif self.__flavour == 'cron':
            from flavours.cron import CronHandler
            return CronHandler
        elif self.__flavour == 'event':
            from flavours.event import EventHandler
            return EventHandler
        elif self.__flavour == 'integration':
            from flavours.integration import IntegrationHandler
            return IntegrationHandler
        else:
            raise Exception(f'unsupported function type: {self.__flavour}')
        
    def __construct_function_parameters(self):
        threading.current_thread().__setattr__('__zc_local', { 'catalyst_headers': get_catalyst_headers() })

        return self.__get_flavour().construct_function_parameters()

    def invoke_handler(self):
        global CUSTOMER_CODE_ENTRYPOINT
        if not CUSTOMER_CODE_ENTRYPOINT:
            spec = spec_from_file_location('', self.__entrypoint)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            CUSTOMER_CODE_ENTRYPOINT = module.handler

        RET = CUSTOMER_CODE_ENTRYPOINT(*(self.__construct_function_parameters()))

        if self.__flavour == 'basicio':
            # Refer: !25. Useful when `context.close()`` is not called by user.
            send_json_response(g.response.status_code, { 'output': g.response.get_data(as_text=True) })
        elif RET and (self.__flavour == 'applogic' or self.__flavour == 'advancedio'):
            # User can return their own response object from applogic functions.
            g.response = RET

    def return_error_response(self, error = None):
        return self.__get_flavour().return_error_response(error)


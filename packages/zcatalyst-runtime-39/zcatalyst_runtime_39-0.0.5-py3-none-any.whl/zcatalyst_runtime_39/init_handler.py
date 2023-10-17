import os
import time
import multiprocessing
from pathlib import Path

MAXIMUM_INIT_WAIT_TIME = 10

class InitHandler:
    __catalyst_listen_port = os.getenv('X_ZOHO_CATALYST_SERVER_LISTEN_PORT')
    __sparkler_listen_port = os.getenv('X_ZOHO_SPARKLET_SERVER_LISTEN_PORT')

    __is_local = os.getenv('X_ZOHO_CATALYST_IS_LOCAL') == 'true'

    __code_location = Path(os.getenv('X_ZOHO_CATALYST_CODE_LOCATION', '/catalyst'))

    __function_loaded = os.getenv('X_ZOHO_CATALYST_FUNCTION_LOADED') == 'true'

    def get_worker_count():
        if InitHandler.__is_local:
            return 2
        
        return multiprocessing.cpu_count()
    
    def get_thread_count():
        return 8

    def get_listen_port() -> int:
        # default port is 9000
        port = 9000
        if InitHandler.__sparkler_listen_port:
            del os.environ['X_ZOHO_SPARKLET_SERVER_LISTEN_PORT']
            port = int(InitHandler.__sparkler_listen_port)
        
        if InitHandler.__catalyst_listen_port:
            del os.environ['X_ZOHO_CATALYST_SERVER_LISTEN_PORT']
            port = int(InitHandler.__catalyst_listen_port)

        return port
    
    def is_local() -> bool:
        return InitHandler.__is_local

    def get_code_location() -> Path:
        return InitHandler.__code_location
    
    def is_success() -> bool:
        return InitHandler.__function_loaded

    def mark_init() -> None:
        InitHandler.__function_loaded = True

    def return_on_success() -> bool:
        current_init_wait_time = 0
        while not InitHandler.is_success():
            if current_init_wait_time < MAXIMUM_INIT_WAIT_TIME:
                time.sleep(.1) # Each 100ms
                current_init_wait_time += .1
            else:
                return False
            
        return True
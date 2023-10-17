import os
import sys
import time
import zipfile
import logging
import signal

from flask import Flask, request, Response, g, current_app

from log_handler import LogHandler
from init_handler import InitHandler
from flavours import FlavourHandler
from flavours.utils import send_json_response

ZIP_LOCATION: str = '/tmp/code.zip'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(LogHandler())

# To support user function to import their own modules and prefer
# locally installed modules over globally installed modules.
sys.path.insert(0, InitHandler.get_code_location().as_posix())

if not InitHandler.is_local():
    def init_signal_handler(_sig, _frame):
        InitHandler.mark_init()

    signal.signal(signal.SIGPWR, init_signal_handler)

app = Flask(__name__)

def internal_request_handler():
    if request.path == '/init':
        if InitHandler.is_success():            
            # Will be caught by uncaught exception handler
            raise Exception('init already completed')
        
        init_start_time = int(time.time() * 1000)

        with open(ZIP_LOCATION, 'wb') as code_zip:
            while True:
                chunk = request.stream.read(1048576)

                if not chunk:
                    break
                code_zip.write(chunk)
                
        with zipfile.ZipFile(ZIP_LOCATION, 'r') as code_zip:
            code_zip.extractall(InitHandler.get_code_location())
            os.remove(ZIP_LOCATION)
            
        if not InitHandler.is_local():
            process_group_id = os.getpgid(os.getpid())
            os.killpg(process_group_id, signal.SIGPWR)

        g.response.headers.add('x-catalyst-init-time-ms', f'{int(time.time() * 1000)} - {init_start_time}')
        send_json_response(200, { 'message': 'success' })
    elif request.path == '/ruok':
        send_json_response(200, { 'message': 'iamok' })
    else:
        raise Exception('unexpected internal path')

FLAVOUR_HANDLER: FlavourHandler = None

def customer_request_handler():
    try:
        global FLAVOUR_HANDLER
        if not FLAVOUR_HANDLER:
            FLAVOUR_HANDLER = FlavourHandler()

        FLAVOUR_HANDLER.invoke_handler()
    except Exception as e:
        logger.exception(repr(e))
        FLAVOUR_HANDLER.return_error_response(repr(e))

@app.route('/', methods=['HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@app.route('/<path:_path>', methods=['HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def router(_path = None):
    g.response = Response()
    
    if request.headers.get('x-zoho-catalyst-internal') == 'true':        
        internal_request_handler()
    else:
        if not InitHandler.return_on_success():
            # Will be caught by uncaught exception handler
            raise Exception('init not completed')

        logger.info(f'Execution started at: {int(time.time() * 1000)}')
        customer_request_handler()
    return g.response

@app.errorhandler(Exception)
def error_handler(e):
    # We caught all customer request exceptions in `customer_request_handler` 
    # itself, so we're marking this exception as an internal failure.  
    with app.app_context():
        setattr(current_app, '__internal_failure', True)
    logger.exception(repr(e))
    send_json_response(500, { 'error': repr(e) })
    return g.response

def run_production_server():
    from gunicorn.app.base import BaseApplication

    # Gunicorn custom application
    # Refer: https://docs.gunicorn.org/en/stable/custom.html
    class CatalystApplication(BaseApplication):
        def __init__(self, app, options = {}):
            self.app = app
            self.options = options

            super().__init__()

        def init(self, parser, opts, args):
            return super().init(parser, opts, args)

        def load(self):
            return self.app
        
        def load_config(self):
            for k, v in self.options.items():
                if k not in self.cfg.settings:
                    print('invalid: ', k)
                    continue

                try:
                    self.cfg.set(k.lower(), v)
                except Exception:
                    raise Exception(f'Invalid value for: {k}: {v}')
                
    # Gunicorn server hooks
    # Refer: https://docs.gunicorn.org/en/stable/settings.html#server-hooks

    # Hook: when_ready
    def when_ready(_server):
        """Called just after the server is started."""

        if InitHandler.is_local():
            return

        # Updates the status of the function to runtime.
        # 
        #    +---------------------+-----------------+------------------------+-------------------+
        #    |  ENCODING (1 byte)  |  PATH (1 byte)  |  CONTENT_LEN (4 byte)  |  STATUS (1 byte)  |
        #    +---------------------+-----------------+------------------------+-------------------+
        # 
        # First 1 byte is the encoding, for status it is always 1.
        # Second 1 byte is the path, for status it is always 0.
        # Third 4 bytes are the content length. For status(unsigned-8bit) this will always be 1. (big-endian)
        # Next 1 byte is status.

        status_frame = bytearray()
        status_frame[0:1] = (1).to_bytes(1, 'big')
        status_frame[1:2] = (0).to_bytes(1, 'big')
        status_frame[2:6] = (1).to_bytes(4, 'big')
        status_frame[6:7] = (1).to_bytes(1, 'big')

        status_fd = int(os.getenv('X_ZOHO_SPARKLET_STATUS_FD'))
        del os.environ['X_ZOHO_SPARKLET_STATUS_FD']

        pid = os.getpid()
        status_fd = open(f'/proc/{pid}/fd/{status_fd}', 'wb', buffering=0)

        status_fd.write(status_frame)

    # Hook: post_request
    def post_request(_worker, _req, _environ, _resp):
        """Called after a worker processes the request."""

        # Since, `error_handler`` marked this as an internal failure, we're exiting
        # from gunicorn worker process after response is sent.
        with app.app_context():
            if getattr(current_app, '__internal_failure', False):
                os._exit(signal.SIGUSR1)

    # Hook: child_exit
    def child_exit(_server, _worker):
        """Called just after a worker has been exited, in the master process."""

        os._exit(signal.SIGUSR1)

    options = {
        'bind': f'0.0.0.0:{InitHandler.get_listen_port()}',
        'workers': InitHandler.get_worker_count(),
        'threads': InitHandler.get_thread_count(),
        'pythonpath': f'{InitHandler.get_code_location()},',
        'preload_app': True,
        'loglevel': 'warning',
        'timeout': 0,
        # Server hooks
        'when_ready': when_ready,
        'child_exit': child_exit,
        'post_request': post_request,
    }

    CatalystApplication(app, options).run()

def run_development_server():
    # To disable Flask's server banner and console logs
    from flask import cli
    cli.show_server_banner = lambda *args: None
    logging.getLogger('werkzeug').disabled = True

    app.run('0.0.0.0', InitHandler.get_listen_port())

if __name__ == "__main__":
    try:
        if not InitHandler.is_local():
            run_production_server()
        else:
            run_development_server()
    except Exception as e:
        logger.exception(e)
        os._exit(signal.SIGUSR1)
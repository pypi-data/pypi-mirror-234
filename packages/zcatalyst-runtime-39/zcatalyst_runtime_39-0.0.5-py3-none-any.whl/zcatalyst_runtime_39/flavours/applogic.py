from flask import request

from flavours import FlavourHandler
from flavours.utils import send_json_response

class ApplogicHandler(FlavourHandler):
    def construct_function_parameters():
        return (request,)

    def return_error_response(error):
        send_json_response(500, { 'error': error })
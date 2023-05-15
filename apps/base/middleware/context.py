"""
Track context  Middleware.
"""
import json
import os
from urllib.request import urlopen


class ContextMiddleware:
    """ """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("Initializing...")

    def __call__(self, request):

        request.path_list = request.get_full_path().split("/")
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

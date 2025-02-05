# your_project/middleware.py

from django.http import HttpResponse

class SetCOOPHeader:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Set Cross-Origin-Opener-Policy header to allow popups across origins
        response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'

        return response

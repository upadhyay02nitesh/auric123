# middleware.py

from django.shortcuts import render
from django.conf import settings

class UnderConstructionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the site is in under-construction mode
        if getattr(settings, 'UNDER_CONSTRUCTION', False):
            return render(request, 'app/under_construction.html')
        
        return self.get_response(request)

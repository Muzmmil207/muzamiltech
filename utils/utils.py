from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest


def get_url(request=None):
    request = request or HttpRequest()
    domain = get_current_site(request).domain
    return "{0}{1}".format(domain, request.get_full_path())

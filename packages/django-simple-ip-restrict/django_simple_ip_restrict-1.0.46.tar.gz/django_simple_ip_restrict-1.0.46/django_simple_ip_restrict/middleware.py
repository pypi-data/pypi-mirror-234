import logging
from functools import partial

from django.conf import settings
from django.http import HttpResponseForbidden
from django.urls import get_resolver, exceptions
from django.urls.resolvers import URLResolver, URLPattern, RoutePattern, RegexPattern
from netaddr import IPAddress, IPNetwork

DEFAULT_PROTECTED_NAMESPACES = ["admin"]


logger = logging.getLogger(__name__)


def ip_filter(get_response):
    protected_namespaces = frozenset(
        getattr(settings, "IP_PROTECTED_NAMESPACES", DEFAULT_PROTECTED_NAMESPACES)
    )
    whitelist = [
        IPNetwork(subnet) for subnet in getattr(settings, "IP_NETWORKS_WHITELIST", [])
    ]

    def middleware(request):
        if hasattr(request, "urlconf"):
            urlconf = request.urlconf
            set_urlconf(urlconf)
            resolver = get_resolver(urlconf)
        else:
            resolver = get_resolver()
        try:
            resolver_match = resolver.resolve(request.path_info)
        except exceptions.Resolver404:
            pass
        else:
            if not protected_namespaces.isdisjoint(resolver_match.namespaces):
                if "HTTP_X_FORWARDED_FOR" in request.META:
                    ip_address = IPAddress(request.META["HTTP_X_FORWARDED_FOR"].split(",")[0])
                else:
                    ip_address = IPAddress(request.META["REMOTE_ADDR"])
                if not any(ip_address in subnet for subnet in whitelist):
                    logger.warn(
                        "IP %s tried to access protected url %s",
                        ip_address,
                        request.path,
                    )
                    return HttpResponseForbidden()

        response = get_response(request)
        return response

    return middleware

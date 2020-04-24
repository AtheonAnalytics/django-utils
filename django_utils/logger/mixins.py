import logging

from .requests import resolve_logging_level


class APILoggingMixin(object):
    """ Logging for inbound API calls """

    def finalize_response(self, request, response, *args, **kwargs):

        extra = {
            'response_type': 'inbound',
            'response_code': response.status_code,
            'response_data': response.data,
            'http_method': request.method,
            'url': request.path,
            'remote_address': self._get_real_ip(request=request)
        }
        logger = logging.getLogger(__name__)
        level = resolve_logging_level(response.status_code)
        getattr(logger, level)(f'API {response.status_code} {request.path}', extra=extra)

        return super(APILoggingMixin, self).finalize_response(
            request, response, *args, **kwargs)

    def _get_real_ip(self, request):
        """ Respect reverse proxy forwarding IP address """
        real_ip = request.META.get('HTTP_X_REAL_IP', None) or \
            request.META.get('HTTP_X_FORWARDED_FOR', None)
        if real_ip:
            return real_ip
        else:
            return request.META.get('REMOTE_ADDR')

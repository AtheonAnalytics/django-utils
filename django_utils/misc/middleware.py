
class RealIPMiddleware(object):
    """ Real IP middleware to replace REMOTE_ADDR with real user ip address """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        real_ip = request.META.get('HTTP_X_REAL_IP', None) or \
            request.META.get('HTTP_X_FORWARDED_FOR', None)
        if real_ip:
            request.META['REMOTE_ADDR'] = real_ip
        response = self.get_response(request)
        return response


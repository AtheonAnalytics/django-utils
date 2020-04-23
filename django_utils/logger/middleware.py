import logging

from django.urls import reverse

logger = logging.getLogger('admin_activity')


class AdminActivityMiddleware(object):
    """
    Log django admin activity
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('admin:index')) and request.method == 'POST':
            extra = {
                'user': request.user,
                'path': request.path,
                'post': request.POST
            }
            logger.info('admin_activity', extra=extra)
        response = self.get_response(request)
        return response


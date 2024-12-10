from django.utils.deprecation import MiddlewareMixin
from mainweb.models import AppVisitStatistics
import logging

# Get the django logger
logger = logging.getLogger('django')

class Throttle(MiddlewareMixin):

    def process_response(self, request, response):
        url = request.path
        if not response.status_code == 404:
            if url != '/':
                AppVisitStatistics.save_app_requests(url.split('/')[1], url)
        return response

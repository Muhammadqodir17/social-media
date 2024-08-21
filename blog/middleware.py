from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


class CacheResponseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'GET':
            user_id = request.user.id if request.user.is_authenticated else 'anonymous'
            cache_key = f'response_cache_{user_id}_{request.path}'

            cached_response = cache.get(cache_key)
            if cached_response:
                return HttpResponse(cached_response.content, status=cached_response.status_code)

    def process_response(self, request, response):
        if request.method == 'GET' and response.status_code == 200:
            user_id = request.user.id if request.user.is_authenticated else 'anonymous'
            cache_key = f'response_cache_{user_id}_{request.path}'

            cache.set(cache_key, response, timeout=60 * 15)

        return response

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        response = Response({
            'error': 'An unexpected error occurred'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if isinstance(exc, (ObjectDoesNotExist, Http404)):
        response.data = {'error': 'The requested resource was not found'}
        response.status_code = status.HTTP_404_NOT_FOUND

    return response


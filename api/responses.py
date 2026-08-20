from rest_framework.response import Response
from rest_framework import status


class ResponseSerializer(Response):
    '''
    Standardized API response serializer.

    All API responses should follow this format:
    {
        "success": bool,
        "data": dict|list|None,
        "errors": dict|str|None,
        "meta": dict|None
    }
    '''

    def __init__(self, data=None, errors=None, meta=None, status=status.HTTP_200_OK, template_name=None):
        if data is None:
            data = {}
        if errors is None:
            errors = {}

        # Ensure the response follows the standard format
        if isinstance(data, dict) and 'success' not in data:
            data['success'] = True

        super().__init__(
            data=data,
            status=status,
            template_name=template_name
        )
        self.meta = meta or {}

    @classmethod
    def success(cls, data=None, meta=None, status=status.HTTP_200_OK):
        '''Create a successful response.'''
        if data is None:
            data = {}
        response_data = {'success': True}
        if data is not None:
            response_data['data'] = data
        return cls(
            data=response_data,
            errors=None,
            meta=meta,
            status=status
        )

    @classmethod
    def error(cls, errors, status=status.HTTP_400_BAD_REQUEST):
        '''Create an error response.'''
        if isinstance(errors, str):
            errors = {'detail': errors}
        return cls(
            data={'success': False, 'data': None, 'errors': errors},
            errors=errors,
            meta=None,
            status=status
        )
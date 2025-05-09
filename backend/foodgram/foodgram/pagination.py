from rest_framework import pagination


class StandardPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'

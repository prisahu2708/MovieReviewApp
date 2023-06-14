from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class WatchlistPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 3
class WatchlistLOPagination(LimitOffsetPagination):
    default_limit = 5   



    
from rest_framework.pagination import PageNumberPagination


class ModelPagination(PageNumberPagination):
    page_size = 20

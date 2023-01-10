from django_filters import rest_framework as filters


class ProductFilterBackend(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name')

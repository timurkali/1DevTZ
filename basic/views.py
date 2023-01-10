from django.db import transaction
from rest_framework import viewsets, status, mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from basic import models, serializers, filters, tasks, constants as const
from user import utils as user_utils


class ProductViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = models.Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
    filterset_class = filters.ProductFilterBackend
    pagination_class = PageNumberPagination
    permission_classes = (permissions.AllowAny,)


class OrderLineViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):

    queryset = models.OrderLine.objects.all()
    serializer_class = serializers.OrderLineSerializer
    permission_classes = (permissions.IsAuthenticated,)


class OrderViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):

    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return models.Order.objects.filter(user_id=self.request.user.pk)

    @action(detail=True, methods=('POST',), url_path='add-order-line')
    @transaction.atomic
    def add_order_line(self, request, pk):
        order = self.get_object()
        context = {'order': order, 'exist_products': order.get_exist_products()}

        serializer = serializers.OrderLineCreateSerializer(
            data=request.data,
            many=True,
            context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tasks.update_order_lines_total.delay(order.pk)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=('PATCH',))
    def pay(self, request, pk):
        order = self.get_object()
        wallet = user_utils.get_wallet(request.user, order.currency)

        if order.status != const.ORDER_STATUSES.NEW:
            return Response({'order': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if not wallet:
            return Response({'wallet': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        if wallet.amount < order.total:
            return Response({'wallet': 'Money not enough'}, status=status.HTTP_400_BAD_REQUEST)

        wallet.amount -= order.total
        order.status = const.ORDER_STATUSES.PAID

        wallet.save(update_fields=('amount',))
        order.save(update_fields=('status',))

        return Response(status=status.HTTP_204_NO_CONTENT)

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shop.models import Product, Order
from shop.serializers import ProductSerializer, ProductListSerializer, OrderSerializer, OrderListSerializer, \
    OrderRetrieveSerializer, UploadImageSerializer, OrderStatusSerializer


class ProductViewSet(ModelViewSet):
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.queryset.filter(category__name=self.request.query_params.get('category'))

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductListSerializer
        if self.action == "upload_image":
            return UploadImageSerializer
        return ProductSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[permissions.IsAdminUser]
    )
    def upload_image(self, request, pk=None):
        plane = self.get_object()
        serializer = self.get_serializer(plane, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(ModelViewSet):
    model = Order
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(
        detail=True
    )
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        order.status = order.StatusChoices.CANCELLED
        order.save()
        return Response({"message": "order has been cancelled"}, status=status.HTTP_200_OK)

    @action(
        detail=True
    )
    def complete_order(self, request, pk=None):
        order = self.get_object()
        order.status = order.StatusChoices.COMPLETED
        order.save()
        return Response({"message": "order has been completed"}, status=status.HTTP_200_OK)

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        if self.action == 'retrieve':
            return OrderRetrieveSerializer
        return OrderSerializer

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from products.models import Product, Basket
from products.serializer import ProductSerializer, BasketSerializer


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class BasketModelViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.select_related('product')
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            product_id = request.data['product_id']
            products = Product.objects.filter(id=product_id)
            if not products.exists():
                return Response(
                    {'product': 'There is not exist product with this id'},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                obj, is_crated = Basket.update_or_create(product_id, self.request.user)
                status_code = status.HTTP_201_CREATED if is_crated else status.HTTP_200_OK
                serializer = self.get_serializer(obj)
                return Response(serializer.data, status=status_code)
        except KeyError:
            return Response({'This field is required'}, status=status.HTTP_400_BAD_REQUEST)

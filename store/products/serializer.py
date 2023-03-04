from rest_framework import serializers
from rest_framework import fields
from products.models import Product, ProductCategory, Basket


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name', queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'image',
                  'category')


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    sum = fields.DecimalField(max_digits=8, decimal_places=2, required=False)
    total_quantity = serializers.SerializerMethodField()
    total_sum = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ('id', 'product', 'quantity', 'sum', 'total_quantity',
                  'total_sum', 'created_timestamp')

    def get_total_quantity(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_quantity()

    def get_total_sum(self, obj):
        return Basket.objects.filter(user_id=obj.user.id).total_sum()

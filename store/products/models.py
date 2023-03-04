from django.conf import settings
from django.db import models
import stripe

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


# Создаем модель категорий товаров
class ProductCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


# Создаем модель с карточкой товаров
class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products_images', null=True,
                              blank=True)
    stripe_product_price_id = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """Достаем из объекта цены id и сохраняем в БД"""
        stripe_product_price = self.stripe_product_price()
        self.stripe_product_price_id = stripe_product_price['id']
        super().save()

    def stripe_product_price(self):
        """Создаем объект цены"""
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency="rub")
        return stripe_product_price


class BasketQuerySet(models.QuerySet):
    """Создаем свой менеджер для использования методов
    подсчета ко всем объектам"""

    def total_sum(self):
        return "{:.2f}".format(sum(basket.sum() for basket in self))

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def create_stripe_product(self):
        line_items = []
        for basket in self:
            item = {
                'price': basket.product.stripe_product_price_id,
                'quantity': basket.quantity
            }
            line_items.append(item)
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return \
            f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def de_json(self):
        baskets_item = {
            'name': self.product.name,
            'quantity': self.quantity,
            'price': "{:.2f}".format(self.product.price),
            'sum': "{:.2f}".format(self.sum())
        }
        return baskets_item

    @classmethod
    def update_or_create(cls, product_id, user):
        baskets = Basket.objects.filter(user=user, product_id=product_id)
        if not baskets.exists():
            obj = Basket.objects.create(
                user=user, product_id=product_id, quantity=1)
            is_created = True
            return obj, is_created
        else:
            basket = baskets.last()
            basket.quantity += 1
            basket.save()
            is_created = False
            return basket, is_created

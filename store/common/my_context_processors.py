from products.models import Basket


def get_baskets(request):
    user = request.user
    baskets = None
    if user.is_authenticated:
        baskets = Basket.objects.filter(user=user)
    else:
        return []
    return {'baskets': baskets}

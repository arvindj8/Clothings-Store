from products.models import Basket


def get_baskets(request):
    baskets = None
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)
    else:
        return []
    return {'baskets': baskets}

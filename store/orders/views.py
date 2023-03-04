from http import HTTPStatus

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from common.mixins import TitleMixin
from orders.forms import OrderCreateForm
from orders.models import Order
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'success.html'
    title = 'Спасибо за заказ!'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'canceled.html'
    title = 'Заказ не оформлен'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'order-create.html'
    form_class = OrderCreateForm
    title = 'Store - Оформление заказа'
    success_url = reverse_lazy('orders:create_order')

    def post(self, request, *args, **kwargs):
        baskets = Basket.objects.filter(user=request.user)
        super().post(self, request, *args, **kwargs)

        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.create_stripe_product(),
            mode='payment',
            metadata={'order_id': self.object.id},
            success_url='{}{}'.format(
                settings.DOMAIN_NAME, reverse('orders:success_order')
            ),
            cancel_url='{}{}'.format(
                settings.DOMAIN_NAME, reverse('orders:canceled_order'))
        )
        return redirect(checkout_session.url, code=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload

        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Check if the order is already paid (for example, from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            # Fulfill the purchase
            fulfill_order(session)

    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']

        # Fulfill the purchase
        fulfill_order(session)

    # elif event['type'] == 'checkout.session.async_payment_failed':
    #     session = event['data']['object']
    #
    #     # Send an email to the customer asking them to retry their order
    #     create_order(session)
    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_status_order_after_payment()


class OrdersTemplateView(TitleMixin, ListView):
    template_name = 'orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()

    def get_queryset(self):
        super().get_queryset()
        return Order.objects.filter(initiator=self.request.user)


class OrderDetailView(TitleMixin, DetailView):
    model = Order
    template_name = 'order.html'
    title = 'Store - Заказ'

    def get_object(self, queryset=None):
        order = get_object_or_404(Order, id=self.kwargs.get('id'))
        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['order'] = self.get_object()
        return context

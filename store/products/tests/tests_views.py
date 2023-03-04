from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from products.views import IndexView


class TestsViews(TestCase):
    def test_views_template_show_correct(self):
        get_page = reverse('products:index')
        response = self.client.get(get_page)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, )



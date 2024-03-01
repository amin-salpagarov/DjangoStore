from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import Product, ProductCategory


class IndexViewTestCase(TestCase):
    def test_view(self):
        path = reverse("index")
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["title"], "Store")
        self.assertTemplateUsed(response, "products/index.html")


class ProductListViewTestCase(TestCase):
    fixtures = ["categories.json", "goods.json"]

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse("products:index")
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(list(response.context["object_list"]), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.first()
        path = reverse("products:category")
        response = self.client.get(path)

        self._common_test(response)
        self.assertEqual(
            list(response.content["object_list"]),
            list(self.products.filter(category_id=category.id)),
        )

    def _common_test(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["title"], "Store - Каталог")
        self.assertTemplateUsed(response, "products/products.html")

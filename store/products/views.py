from typing import Any

from common.views import TitleMixin
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = "products/index.html"
    title = "Store"


class ProductsListView(ListView):
    model = Product
    template_name = "products/products.html"
    paginate_by = 2

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get("category_id")
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        categories = cache.get("categories")
        if not categories:
            context["categories"] = ProductCategory.objects.all()
            cache.set("categories", context["categories"], 30)
        else:
            context["categories"] = categories

        context["title"] = "Store - Каталог"
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)

    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.filter(user=request.user, id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])

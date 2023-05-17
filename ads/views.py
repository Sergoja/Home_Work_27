import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Ad, Category


def home(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse([{
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "description": ad.description,
                "price": ad.price,
                "address": ad.address,
                "is_published": ad.is_published
            } for ad in self.object_list], safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data["name"]
        ad.author = ad_data["author"]
        ad.description = ad_data["description"]
        ad.price = ad_data["price"]
        ad.address = ad_data["address"]
        ad.is_published = ad_data["is_published"]

        ad.save()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "description": ad.description,
            "price": ad.price,
            "address": ad.address,
            "is_published": ad.is_published,
        })


class AdsDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author,
            "description": ad.description,
            "price": ad.price,
            "address": ad.address,
            "is_published": ad.is_published,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{"id": cat.pk, "name": cat.name} for cat in self.object_list], safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        new_category = Category.objects.create(name=category_data.get("name"))

        return JsonResponse({
            "id": new_category.id,
            "name": new_category.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)

        self.object.name = cat_data["name"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })

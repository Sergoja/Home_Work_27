import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Ad, Category


def home(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdView(View):
    def get(self, request):

        ads = Ad.objects.all()

        search_text = request.GET.get("text", None)
        if search_text:
            ads = ads.filter(text=search_text)
            if not ads:
                return JsonResponse({"error": "Not found"}, status=404)

        response = []
        for ad in ads:
            response.append({
                "id": ad.id,
                "name": ad.name,
                "author": ad.author,
                "description": ad.description,
                "price": ad.price,
                "address": ad.address,
                "is_published": ad.is_published
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
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


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):
    def get(self, request):

        categories = Category.objects.all()

        search_text = request.GET.get("text", None)
        if search_text:
            categories = categories.filter(text=search_text)
            if not categories:
                return JsonResponse({"error": "Not found"}, status=404)

        response = []
        for category in categories:
            response.append({
                "id": category.id,
                "name": category.name,
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Ad()
        category.name = category_data["name"]

        category.save()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
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


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })

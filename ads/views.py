import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ads.models import Ad


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



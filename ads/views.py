import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from Home_Work_27 import settings
from ads.models import Ad, Category
from users.models import User


def home(request):
    return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list.order_by("-price"), settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)

        return JsonResponse(
            {"total": paginator.count,
             "num_pages": paginator.num_pages,
             "items": [{"id": ad.id,
                        "name": ad.name,
                        "author": ad.author,
                        "description": ad.description,
                        "price": ad.price,
                        "category": ad.category,
                        "is_published": ad.is_published,
                        "image": ad.image.url if ad.image else None
                        } for ad in page_object]}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class AdCreateView(CreateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        author = get_object_or_404(User, pk=data.pop("author_id"))
        category = get_object_or_404(Category, pk=data.pop("category_id"))
        ad = Ad.objects.create(author=author, category=category, **data)

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author.username,
            "description": ad.description,
            "price": ad.price,
            "category": ad.category.name,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None
        })


class AdsDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "description": ad.description,
            "price": ad.price,
            "category": ad.category.name,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        if "name" in data:
            self.object.name = data.get("name")
        if "description" in data:
            self.object.description = data.get("description")
        if "price" in data:
            self.object.price = data.get("price")
        if "category_id" in data:
            category = get_object_or_404(Category, pk=data.get("category_id"))
            self.object.category = category

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "description": self.object.description,
            "price": self.object.price,
            "category": self.object.category.name,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImageView(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "description": self.object.description,
            "price": self.object.price,
            "category": self.object.category.name,
            "is_published": self.object.is_published,
            "image": self.object.image.url,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{"id": cat.pk, "name": cat.name} for cat in self.object_list.order_by("name")], safe=False)


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

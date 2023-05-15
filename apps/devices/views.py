import json
from datetime import datetime
from io import BytesIO
from operator import mul

import requests
from PIL import Image

from apps.articles.models import Article, Category
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import slugify

from .models import (
    Brand,
    Device,
    DeviceAttribute,
    DeviceAttributeValue,
    DeviceSource,
    DeviceType,
    DeviceTypeAttribute,
    Media,
)


def devices(request):
    context = {}
    return render(request, "apps/devices/devices.html", context=context)


def brands(request):
    context = {}
    return render(request, "apps/devices/brands.html", context=context)


def device_details(request, brand, model):
    camera = DeviceTypeAttribute.objects.get(name="camera")
    print(camera.children.all())
    device = Device.objects.filter(slug=model, brand__name=brand).first()
    main_attribute_value = (
        DeviceAttributeValue.objects.filter(device=device)
        .filter(
            Q(
                device_attribute__device_type_attribute__name="display",
                device_attribute__attribute="resolution_(h_x_w)",
            )
            | Q(
                device_attribute__device_type_attribute__name="processor",
                device_attribute__attribute="cpu",
            )
            | Q(
                device_attribute__device_type_attribute__name="front_camera",
                device_attribute__attribute="resolution",
            )
            | Q(
                device_attribute__device_type_attribute__name="software",
                device_attribute__attribute="os_version",
            )
            | Q(
                device_attribute__device_type_attribute__name="battery",
                device_attribute__attribute="capacity",
            )
        )
        .values(
            "device_attribute__device_type_attribute__name", "device_attribute__attribute", "value"
        )
    )
    articles = Article.objects.exclude(image_url=None).order_by("?")[:4]
    context = {"device": device, "attributes": main_attribute_value, "articles": articles}
    return render(request, "apps/devices/device-details.html", context=context)


def devices_by_brand(request, brand):
    devices = Device.objects.filter(brand__slug=brand)
    context = {"devices": devices}
    return render(request, "apps/devices/devices-by-brand.html", context=context)


def search_devices(request):
    context = {}
    return render(request, "apps/devices/search-devices.html", context=context)


def insert_devices_data(request):
    context = {
        "new_categories": 0,
        "new_brand": 0,
        "new_devices": 0,
    }

    if request.method == "POST":
        from_date = datetime.strptime(request.POST.get("day"), "%Y-%m-%d")
        to_date = datetime.strptime(request.POST.get("to_day"), "%Y-%m-%d")
        day = "{0:%Y-%m-%d}".format(from_date)
        to_day = "{0:%Y-%m-%d}".format(to_date)

        category = request.POST.get("category")
        device_type = DeviceType.objects.get(id=request.POST.get("type", 1))
        device_category, device_category_ = Category.objects.get_or_create(
            name=category,
            slug=slugify(category),
        )

        context["new_categories"] += device_category_
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {settings.TECHSPECS_API_KEY}",
        }
        url = "https://api.techspecs.io/v4/all/products"
        payload = {"category": [category], "from": day, "to": to_day}
        response = requests.post(url, json=payload, headers=headers, params={"page": 0})
        data = response.json()

        data = data["data"]
        context["total_results"] = data["total_results"]
        while int(data["page"]) < data["total_pages"]:
            # print(f'data["page"] {data["page"]}')
            items = data["items"]
            for item in items:
                brand, brand_ = Brand.objects.get_or_create(
                    name=item["product"]["brand"], slug=slugify(item["product"]["brand"])
                )
                context["new_brand"] += brand_
                device, is_created = Device.objects.get_or_create(
                    brand=brand,
                    model=item["product"]["model"],
                    version=item["product"]["version"],
                    slug=slugify(item["product"]["model"]),
                    category=device_category,
                    type=device_type,
                )
                context["new_devices"] += is_created
                if is_created:
                    DeviceSource.objects.create(
                        device=device,
                        web_id=item["product"]["id"],
                        source=response.url,
                    )
                    for img in item["image"]:
                        if item["image"][img]:
                            Media.objects.create(
                                device=device,
                                image=item["image"][img],
                                alt_text=f"{img} - {device.model}",
                                is_feature=img == "front",
                            )
            try:
                response = requests.post(
                    url, json=payload, headers=headers, params={"page": int(data["page"]) + 1}
                )
                # print(response.url)
                data = response.json()
                data = data["data"]
            except Exception as e:
                context["exception"] = e
                break

    return render(request, "dashboard/new-devices.html", context)


def update_devices_data(request):
    context = {
        "new_devices": 0,
    }

    def update_devices(device_obj: Device, dic: dict):
        device_obj.released = datetime.strptime(dic["date"]["released"], "%Y-%m-%d")
        device_obj.announced = datetime.strptime(dic["date"]["announced"], "%Y %b %d")
        device_obj.status = "updated once"
        device_obj.save()
        print(device_obj.status)
        for img in dic["image"]:
            if dic["image"][img]:
                Media.objects.get_or_create(
                    device=device_obj,
                    image=dic["image"][img],
                    alt_text=f"{img} - {device_obj.model}",
                    is_feature=img == "front",
                )

        return

    if request.method == "POST":
        status = request.POST.get("status", "")
        category = Category.objects.get(id=request.POST.get("category", 0))
        device_type = DeviceType.objects.get(id=request.POST.get("type", 1))

        """If New Inserted Status"""
        while Device.objects.filter(status=status, category=category) and status == "new inserted":
            device = Device.objects.filter(status=status, category=category).first()
            device_source = device.source(src="https://api.techspecs.io/v4/")

            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "Authorization": f"Bearer {settings.TECHSPECS_API_KEY}",
            }
            url = (
                "https://api.techspecs.io/v4/product/detail"  # ?productId=63e96260ff7af4b68a304280"
            )
            try:
                response = requests.get(
                    url, headers=headers, params={"productId": device_source.web_id}
                )
            except Exception as e:
                context["exception"] = e
            with open("files/token.json") as data:
                data = json.loads(data.read())
                print(data["status"])
            # data = response.json()
            # data = data.get("data", {})
            products = data["data"]["items"]
            if products:
                for product in products:
                    device_record = Device.manager.get_or_none(
                        device_Source__web_id=product["product"]["id"]
                    )
                    if device_record:
                        update_devices(device_record, product)
                    else:
                        brand, brand_ = Brand.objects.get_or_create(
                            name=product["product"]["brand"],
                            slug=slugify(product["product"]["brand"]),
                        )
                        device, is_created = Device.objects.get_or_create(
                            brand=brand,
                            model=product["product"]["model"],
                            version=product["product"]["version"],
                            slug=slugify(product["product"]["model"]),
                            category=category,
                            type=device_type,
                        )
                        context["new_devices"] += is_created
                        id = product["product"]["id"]
                        if is_created:
                            DeviceSource.objects.create(
                                device=device,
                                web_id=product["product"]["id"],
                                source=f"https://api.techspecs.io/v4/product/detail?productId={id}",
                                # source=response.url,
                            )
                            device_record = device
                            update_devices(device_record, product)

                    device_record.refresh_from_db()
                    device_record.parent = device
                    device_record.save()
                    context["new_devices"] += 1
                    del product["product"]
                    del product["image"]
                    del product["date"]

                    for key, values in product.items():
                        type_attribute, _ = DeviceTypeAttribute.objects.get_or_create(name=key)
                        type_attribute.device_type_attributes.add(device_record.type)
                        type_attribute.save()

                        def device_attributes_data(type_attributes_obj, key, value):
                            device_attribute, _ = DeviceAttribute.objects.get_or_create(
                                device_type_attribute=type_attributes_obj, attribute=key
                            )
                            DeviceAttributeValue.objects.get_or_create(
                                device_attribute=device_attribute, device=device_record, value=value
                            )
                            return

                        for key in values:
                            value = values[key]
                            if type(value) == dict:
                                (
                                    children_type_attribute,
                                    _,
                                ) = DeviceTypeAttribute.objects.get_or_create(
                                    name=key, parent=type_attribute
                                )
                                print(value)
                                for k, v in value.items():

                                    device_attributes_data(children_type_attribute, k, v)
                            else:
                                print("value", value)
                                device_attributes_data(type_attribute, key, value)
            break
    return render(request, "dashboard/update-devices.html", context)

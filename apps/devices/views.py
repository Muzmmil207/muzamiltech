from datetime import datetime
from io import BytesIO
from operator import mul

import requests
from PIL import Image

from django.conf import settings
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render
from django.template.defaultfilters import slugify

from .models import Brand, Device, DeviceCategory, DeviceSource, Media


def device_details(request, brand, model):
    context = {}
    return render(request, "apps/devices/device-details.html", context=context)


def devices_by_brand(request, brand):
    context = {}
    return render(request, "apps/devices/devices-by-brand.html", context=context)


def insert_devices_data(request):
    context = {
        "new_categories": 0,
        "new_brand": 0,
        "new_devices": 0,
    }
    if request.method == "POST":
        date = datetime.strptime(request.POST.get("day"), "%Y-%m-%d")
        day = "{0:%Y-%m-%d}".format(date)
        category = request.POST.get("category")
        device_category, device_category_ = DeviceCategory.objects.get_or_create(
            name=category, slug=slugify(category)
        )
        context["new_categories"] += device_category_
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": f"Bearer {settings.TECHSPECS_API_KEY}",
        }
        url = "https://api.techspecs.io/v4/all/products"
        payload = {"category": [category], "from": day}
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
            except:
                break

    return render(request, "dashboard/new-devices.html", context)


def update_devices_data(request):
    context = {
        "new_devices": 0,
    }

    def update_devices(device_obj: Device, dic: dict):
        device_obj.info = dic.get("info", F("info"))
        new_device_record.mpn = dic.get("info").split("-")[-1].strip()
        device_obj.status = "updated once"
        DeviceSource.objects.create(
            device=device_obj,
            web_id=dic["id"],
            source=response.url,
        )

        images = dic["images"]
        higher_pixels = 0
        for image in images:
            image["is_feature"] = False
            resp = requests.get(image["url"])
            # Read the content of the resp into a BytesIO object
            bytes_io_obj = BytesIO(resp.content)
            # Open the image from the BytesIO object
            img_obj = Image.open(bytes_io_obj)
            # Get the size of the image
            img_pixels = mul(img_obj.size[0], img_obj.size[1])

            if img_pixels > higher_pixels:
                higher_pixels = img_pixels
                image["is_feature"] = True
            print(img_pixels)  # Output: (width, height)

        for image in images:
            Media.objects.create(
                device=device_obj,
                image=image["url"],
                alt_text=device_obj.model,
                is_feature=image["is_feature"],
            )

        return device_obj

    if request.method == "POST":
        status = request.POST.get("status")
        category = DeviceCategory.objects.get(id=request.POST.get("category", 0))
        devices = Device.objects.filter(status=status, category=category)
        """If New Inserted Status"""
        if status == "new inserted":
            for device in devices:
                device_model = device.model.replace(" ", "+")

                headers = {
                    "Authorization": f"Bearer {settings.DEVICE_SPECS_API_KEY}",
                }
                url = f"https://api.device-specs.io/api/fuzzy-search/search?query={device_model}"
                try:
                    response = requests.get(
                        url, headers=headers
                    )  # , params={"query": device_model})
                except Exception as e:
                    context["exception"] = e
                print(response.url)
                data = response.json()
                data = data[category.name.lower()]
                if len(data) > 0:
                    first_row = data.pop(0)
                    for row in data:
                        new_device_record = device
                        new_device_record.pk = None
                        new_device_record.id = None
                        update_devices(new_device_record, row)
                        new_device_record.device = device
                        new_device_record.save()
                        context["new_devices"] += 1

                    update_devices(device, first_row)

        """If Updated Once Status"""
        if status == "updated once":
            for device in devices:
                device_model = device.model.replace(" ", "+")
                device_source = device.source()
                # headers = {
                #     "Authorization": f"Bearer {settings.DEVICE_SPECS_API_KEY}",
                # }
                # url = f"https://api.device-specs.io/api/smartphones/{device_source.web_id}?populate=*"
                # try:
                #     response = requests.get(
                #         url, headers=headers
                #     )  # , params={"query": device_model})
                # except Exception as e:
                #     context["exception"] = e
                # print(response.url)
                # data = response.json()
                # data = data[category.name.lower()]

    return render(request, "dashboard/update-devices.html", context)

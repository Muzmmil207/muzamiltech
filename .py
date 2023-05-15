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
        category = DeviceCategoryType.objects.get(id=request.POST.get("category", 0))
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

    return render(request, "dashboard/update-devices.html", context)


class DeviceCategoryType(AbstractModel):
    """
    Devices Categories table
    """

    class Meta:
        verbose_name = "Devices category"
        verbose_name_plural = "Devices categories"
        db_table = "device_category_type"

    name = models.CharField(
        max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name="category name",
        help_text="format: required, max-100",
    )
    device_type = models.ForeignKey("DeviceType", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DeviceTypeAttribute(Model):
    """
    Device type attributes link table
    """

    class Meta:
        unique_together = ("Device_attribute", "Device_type")
        db_table = "devices_types_attributes"

    Device_attribute = models.ForeignKey(
        DeviceAttribute,
        related_name="Device_attribute",
        on_delete=models.PROTECT,
    )
    Device_type = models.ForeignKey(
        DeviceType,
        related_name="Device_type",
        on_delete=models.PROTECT,
    )

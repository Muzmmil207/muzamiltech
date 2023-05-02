from rest_framework import serializers

from apps.articles.models import Article
from apps.devices.models import Device


############################
# Articles App Serializers #
############################
class ArticlesSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "description",
            "image_url",
            "published_at",
        ]
        read_only = True


##########################
# Device App Serializers #
##########################


class DevicesSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()

    class Meta:
        model = Device
        fields = [
            "id",
            "mpn",
            "model",
            "slug",
            "category",
            "brand",
            "image",
        ]
        read_only = True

from rest_framework import serializers
from .models import Url

class urlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        #fields = ('url','visit_count','short_url')
        fields = '__all__'
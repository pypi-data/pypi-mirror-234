from rest_framework import serializers

from api.mapper.models import File

class FileSerializer(serializers.Serializer):
    class Meta:
        model = File
        fields = ('file',)

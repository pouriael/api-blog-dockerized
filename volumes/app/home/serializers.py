from rest_framework import serializers

class PersonSerializers(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()
    email = serializers.EmailField()
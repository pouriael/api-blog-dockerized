from unittest import result
from rest_framework import serializers
from .models import *
from .custom_relational import *
 
class QuestionSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    user =UserEmailRelationalField(read_only=True,)

    class Meta:
        model = Question
        fields = '__all__'

    def get_answers(self, obj):
        result = obj.answers.all()
        return AnswerSerializer(instance=result, many=True).data

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'
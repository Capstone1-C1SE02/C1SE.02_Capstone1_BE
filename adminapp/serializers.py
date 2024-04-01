from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'   


class AcademicProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_Program
        fields = '__all__'

     
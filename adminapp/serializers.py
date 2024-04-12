from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
class LogoutSerializer(serializers.Serializer):
    pass

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'   

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_Year
        fields = '__all__'   

class AcademicProgramSerializer(serializers.ModelSerializer):
    major = MajorSerializer(source='MajorID',many=False)
    class Meta:
        model = Academic_Program
        fields = '__all__'   

class YearBasedAcademiProgramSerializer(serializers.ModelSerializer):
    academic_year = AcademicYearSerializer(source='AcademicYearID',many=False)  # Sử dụng source để chỉ định tên trường trong model academicyear
    program = AcademicProgramSerializer(source='ProgramID',many=False)          # Sử dụng source để chỉ định tên trường trong model academicprogram
    
    class Meta:
        model = Year_Based_Academic_Program
        fields = ['YBAP_ID', 'academic_year', 'program']

class DegreeBookSerializer(serializers.ModelSerializer):
    student = StudentSerializer(source='StudentID',many=False)
    class Meta:
        model = Degree_Book
        fields = '__all__'

class DegreeInfomationSerializer(serializers.ModelSerializer):
    degreeBook = DegreeBookSerializer(source='DegreeBookID',many=False)
    class Meta:
        model = Degree_Infomation
        fields = '__all__'





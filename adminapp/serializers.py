from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    
class LogoutSerializer(serializers.Serializer):
    pass


class MajorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields =['MajorID','MajorName','Description','MajorCode']  

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_Year
        fields = '__all__'   

class AcademicProgramSerializer(serializers.ModelSerializer):
    MajorName = serializers.SerializerMethodField()
    class Meta:
        model = Academic_Program
        fields = ['ProgramID','ProgramName', 'ProgramCode', 'ModeofStudy', 'DurationOfTraning', 'Description', 'MajorID','MajorName'] 
    def get_MajorName(self, obj):
        return obj.MajorID.MajorName
    
class AcademicProgramPostMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Academic_Program
        fields = '__all__'


class YearBasedAcademiProgramSerializer(serializers.ModelSerializer):
    programName = serializers.CharField(source='ProgramID.ProgramName')
    majorID = serializers.IntegerField(source='ProgramID.MajorID.MajorID')
    majorName = serializers.CharField(source='ProgramID.MajorID.MajorName')
    academicYear = serializers.CharField(source='AcademicYearID.Year')
    
    class Meta:
        model = Year_Based_Academic_Program
        fields = ['YBAP_ID', 'ProgramID', 'programName', 'majorID', 'majorName', 'AcademicYearID', 'academicYear']
    
    
class StudentDetailSerializer(serializers.ModelSerializer):
    yearbasedacademicprogram = YearBasedAcademiProgramSerializer(source='YBAP_ID',many=False)
    program_name = serializers.SerializerMethodField()
    major_name = serializers.SerializerMethodField()
    StudentName = serializers.SerializerMethodField()

    class Meta:
        model = Student
        exclude = ['FirstName', 'LastName']

    def get_StudentName(self, obj):
        # Phương thức để lấy giá trị của trường StudentName
        return f"{obj.LastName} {obj.FirstName}"
    
    def get_program_name(self, obj):
        if obj.YBAP_ID and obj.YBAP_ID.ProgramID:
            return obj.YBAP_ID.ProgramID.ProgramName
        return None
    
    def get_major_name(self, obj):
        if obj.YBAP_ID and obj.YBAP_ID.ProgramID and obj.YBAP_ID.ProgramID.MajorID:
            return obj.YBAP_ID.ProgramID.MajorID.MajorName
        return None


class StudentPostMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    

class DegreeBookSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer(source='StudentID',many=False)
    class Meta:
        model = Degree_Book
        fields = '__all__'

class DegreeBookSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer(source='StudentID',many=False)
    class Meta:
        model = Degree_Book
        fields = '__all__'

class DegreeBookPostMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree_Book
        fields = '__all__'


class DegreeInformationSerializer(serializers.ModelSerializer):
    degreeBook = DegreeBookSerializer(source='DegreeBookID',many=False)
    
    class Meta:
        model = Degree_Information
        fields = '__all__'


class RetrievalByTextSerializer(serializers.Serializer):
    student = StudentDetailSerializer(source='StudentID',many=False)
    degreeBook = DegreeBookSerializer(source='DegreeBookID',many=False)

    class Meta:
        model = Degree_Information
        fields = ['StudentName', 'MajorName', 'ProgramName', 'Classification','BirthOfDate','MSSV','NumberInTheDegreeBook','YearOfGraduation','SerialNumber']

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes


from .models  import *
from .serializers import *

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực thông tin đăng nhập
        user = authenticate(username=username, password=password)

        if user is not None:
            # Tạo token nếu xác thực thành công
            refresh = RefreshToken.for_user(user)
            message = "Succesfully"
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response({"token:":tokens ,"message":message}, status=status.HTTP_200_OK)
        else:
            # Trả về lỗi nếu xác thực thất bại
            return Response({"error": "Incorrect username or password."}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

####### Academic Year API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicYearList(APIView):
    def get(self, request, format=None):
        academicYear = Academic_Year.objects.all()
        serializer = AcademicYearSerializer(academicYear, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = AcademicYearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicYearDetail(APIView):
    def get_object(self, pk):
        try:
            return Academic_Year.objects.get(pk=pk)
        except Academic_Year.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        academicYear = self.get_object(pk)
        serializer = AcademicYearSerializer(academicYear)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        academicYear = self.get_object(pk)
        serializer = AcademicYearSerializer(academicYear, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academicYear = self.get_object(pk)
        academicYear.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

####### Student API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentList(APIView):
    def get(self, request, format=None):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentDetail(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
####### Academic Program API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicProgramList(APIView):
    def get(self, request, format=None):
        academicProgram = Academic_Program.objects.all()
        serializer = AcademicProgramSerializer(academicProgram, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = AcademicProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicProgramDetail(APIView):
    def get_object(self, pk):
        try:
            return Academic_Program.objects.get(pk=pk)
        except Academic_Program.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        academicProgram = self.get_object(pk)
        serializer = AcademicProgramSerializer(academicProgram)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        academicProgram = self.get_object(pk)
        serializer = AcademicProgramSerializer(academicProgram, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academicProgram = self.get_object(pk)
        academicProgram.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

####### Major  API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class MajorList(APIView):
    def get(self, request, format=None):
        major = Major.objects.all()
        serializer = MajorSerializer(major, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = MajorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class MajorDetail(APIView):
    def get_object(self, pk):
        try:
            return Major.objects.get(pk=pk)
        except Major.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        major = self.get_object(pk)
        serializer = MajorSerializer(major)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        major = self.get_object(pk)
        serializer = MajorSerializer(major, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        major = self.get_object(pk)
        major.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

####### Year Based Academic Program  API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class YearBasedAcademicProgramList(APIView):
    def get(self, request, format=None):
        YBAP_param = Year_Based_Academic_Program.objects.all()
        serializer = YearBasedAcademiProgramSerializer(YBAP_param, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = YearBasedAcademiProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class YearBasedAcademicProgramDetail(APIView):
    def get_object(self, pk):
        try:
            return Year_Based_Academic_Program.objects.get(pk=pk)
        except Year_Based_Academic_Program.objects.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        YBAP_param = self.get_object(pk)
        serializer = YearBasedAcademiProgramSerializer( YBAP_param)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        YBAP_param = self.get_object(pk)
        serializer = YearBasedAcademiProgramSerializer(YBAP_param, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        YBAP_param = self.get_object(pk)
        YBAP_param.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    



####### Degree Book  API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeBookList(APIView):
    def get(self, request, format=None):
        degreebook = Degree_Book.objects.all()
        serializer = DegreeBookSerializer(degreebook, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = DegreeBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeBookDetail(APIView):
    def get_object(self, pk):
        try:
            return Degree_Book.objects.get(pk=pk)
        except Degree_Book.objects.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        degreebook = self.get_object(pk)
        serializer = DegreeBookSerializer( degreebook)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        degreebook = self.get_object(pk)
        serializer = DegreeBookSerializer(degreebook, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        degreebook = self.get_object(pk)
        degreebook.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

####### Degree Infomation  API ########
#######################################
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeInfomationList(APIView):
    def get(self, request, format=None):
        degreeinfo = Degree_Infomation.objects.all()
        serializer = DegreeInfomationSerializer(degreeinfo, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = DegreeInfomationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeInfomationDetail(APIView):
    def get_object(self, pk):
        try:
            return Degree_Infomation.objects.get(pk=pk)
        except Degree_Infomation.objects.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        degreeinfo = self.get_object(pk)
        serializer = DegreeInfomationSerializer( degreeinfo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        degreeinfo = self.get_object(pk)
        serializer = DegreeInfomationSerializer(degreeinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        degreeinfo = self.get_object(pk)
        degreeinfo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
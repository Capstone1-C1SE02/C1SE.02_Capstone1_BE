from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.http import JsonResponse
from datetime import datetime

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
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)

####### Student API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class StudentList(APIView):
    def get(self, request, format=None):
        student = Student.objects.all()
        serializer = StudentDetailSerializer(student, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):

        ##### get data from request
        program_name = request.data.get('ProgramName')
        major_name = request.data.get('MajorName')
        first_name = request.data.get('FirstName')
        last_name = request.data.get('LastName')
        gender = request.data.get('Gender')
        date_of_birth = request.data.get('DateOfBirth')
        address = request.data.get('Address')
        nation = request.data.get('Nation')
        nationality = request.data.get('Nationality')
        phone_number = request.data.get('PhoneNumber')
        email = request.data.get('Email')
        mssv = request.data.get('MSSV')
        year_of_admission = request.data.get('YearOfAdmission')

        ### Check requirement data
        if not program_name:
            return Response({"message": "ProgramName is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not major_name:
            return Response({"message": "MajorName is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not first_name:
            return Response({"message": "FirstName is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not last_name:
            return Response({"message": "LastName is required."}, status=status.HTTP_400_BAD_REQUEST)
        if gender is None:
            return Response({"message": "Gender is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not date_of_birth:
            return Response({"message": "DateOfBirth is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not address:
            return Response({"message": "Address is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not nation:
            return Response({"message": "Nation is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not nationality:
            return Response({"message": "Nationality is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not phone_number:
            return Response({"message": "PhoneNumber is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not email:
            return Response({"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not mssv:
            return Response({"message": "MSSV is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not year_of_admission:
            return Response({"message": "YearOfAdmission is required."}, status=status.HTTP_400_BAD_REQUEST)

        ### Query 
        try:
            program = Academic_Program.objects.get(ProgramName=program_name)
            major = Major.objects.get(MajorName=major_name)
            year = Academic_Year.objects.get(Year = year_of_admission)
            ybap = Year_Based_Academic_Program.objects.get(AcademicYearID=year.AcademicYearID, ProgramID=program.ProgramID)
            
            student = Student.objects.create(
                FirstName = first_name,
                LastName = last_name,
                Gender = gender,
                DateOfBirth = datetime.strptime(date_of_birth, "%Y-%m-%d"),
                Address = address,
                Nation = nation,
                Nationality = nationality,
                PhoneNumber = phone_number,
                Email = email,
                MSSV = mssv,
                YearOfAdmission = year_of_admission,
                YBAP_ID = ybap
            )
            ##  Tạo student để trả nếu have time
            # student_data = Student.objects.create(
            #     FirstName = first_name,
            #     LastName = last_name,
            #     Gender = gender,
            #     DateOfBirth = datetime.strptime(date_of_birth, "%Y-%m-%d"),
            #     Address = address,
            #     Nation = nation,
            #     Nationality = nationality,
            #     PhoneNumber = phone_number,
            #     Email = email,
            #     MSSV = mssv,
            #     YearOFAdmission = year_of_admission,
            #     YBAP_ID = ybap
            # )
            return Response({ "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)

        except Academic_Program.DoesNotExist :
            return Response({'error': 'Chương trình không tồn tại'}, status=status.HTTP_404_NOT_FOUND)
        except Major.DoesNotExist:
            return Response({'error': 'Chuyên ngành không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

    
    
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
        serializer = StudentDetailSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentDetailSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student = self.get_object(pk)
        student.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    
####### Academic Program API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AcademicProgramList(APIView):
    def get(self, request, format=None):
        academicProgram = Academic_Program.objects.all()
        serializer = AcademicProgramSerializer(academicProgram, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = AcademicProgramPostMethodSerializer(data=request.data)
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
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
        

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
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
        

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
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    



####### Degree Book  API ########
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeBookList(APIView):
    def get(self, request, format=None):
        degreebook = Degree_Book.objects.all()
        serializer = DegreeBookSerializer(degreebook, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        ## get data from request
        first_name = request.data.get('FirstName')
        last_name = request.data.get('LastName')
        mssv = request.data.get('MSSV')
        number_of_graduation_decision = request.data.get('NumberOfGraduationDecision')
        graduation_decision_date = request.data.get('GraduationDecisionDate')
        number_in_the_degree_book = request.data.get('NumberInTheDegreeBook')
        if not first_name:
            raise serializers.ValidationError("FirstName is required.")
        if not last_name:
            raise serializers.ValidationError("LastName is required.")
        if not mssv:
            raise serializers.ValidationError("MSSV is required.")
        if not number_of_graduation_decision:
            raise serializers.ValidationError("NumberOfGraduationDecision is required.")
        if not graduation_decision_date:
            raise serializers.ValidationError("GraduationDecisionDate is required.")
        if not number_in_the_degree_book:
            raise serializers.ValidationError("NumberInTheDegreeBook is required.")
        
        ### query student
        try:
            student = Student.objects.get(FirstName=first_name, LastName=last_name, MSSV=mssv)
        except Student.DoesNotExist:
            return Response({"message": "Thông tin sinh viên của bạn không chính xác!! Vui lòng kiểm tra lại."}, status=status.HTTP_400_BAD_REQUEST)

        degree_book = Degree_Book.objects.create(
            NumberOfGraduationDecision=number_of_graduation_decision,
            GraduationDecisionDate=datetime.strptime(graduation_decision_date, "%Y-%m-%d"),
            NumberInTheDegreeBook=number_in_the_degree_book,
            StudentID=student
        )
        degree_book_data = {
            "DegreeBookID": degree_book.DegreeBookID,
            "NumberOfGraduationDecision": degree_book.NumberOfGraduationDecision,
            "GraduationDecisionDate": degree_book.GraduationDecisionDate,
            "NumberInTheDegreeBook": degree_book.NumberInTheDegreeBook,
            "StudentID": degree_book.StudentID_id  # Chú ý: Đây là ID của sinh viên được liên kết với Degree_Book
        }
        return Response({"data": degree_book_data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeBookDetail(APIView):
    def get_object(self, pk):
        try:
            return Degree_Book.objects.get(pk=pk)
        except Degree_Book.objects.DoesNotExist:
            raise Http404("Degree Book not found")

    def get(self, request, pk, format=None):
        degreebook = self.get_object(pk)
        serializer = DegreeBookSerializer(degreebook)
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
        degreeinfo = Degree_Information.objects.all()
        serializer = DegreeInformationSerializer(degreeinfo, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = DegreeInformationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Tạo mới thành công"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class DegreeInfomationDetail(APIView):
    def get_object(self, pk):
        try:
            return Degree_Information.objects.get(pk=pk)
        except Degree_Information.objects.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        degreeinfo = self.get_object(pk)
        serializer = DegreeInformationSerializer( degreeinfo)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        degreeinfo = self.get_object(pk)
        serializer = DegreeInformationSerializer(degreeinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        degreeinfo = self.get_object(pk)
        degreeinfo.delete()
        return Response({"message": "Xóa thành công"}, status=status.HTTP_204_NO_CONTENT)
    



####### Degree Information Retrival throught Text API  ########

class RetrievalThroughTextAPI(APIView):
    def post(self, request, format=None):
        serialNumber = request.data.get('SerialNumber')
        numberInDegreeBook = request.data.get('NumberInTheDegreeBook')
        studentName = request.data.get('StudentName')
        
        if not (serialNumber and numberInDegreeBook and studentName):
            return Response({"message": "Dữ liệu không hợp lệ"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            degree_information = Degree_Information.objects.get(
                SerialNumber=serialNumber,
                DegreeBookID__NumberInTheDegreeBook=numberInDegreeBook,
                DegreeBookID__StudentID__StudentName=studentName,
            )
            student_name = degree_information.DegreeBookID.StudentID.StudentName
            major_name = degree_information.DegreeBookID.StudentID.YBAP_ID.program.MajorName
            program_name = degree_information.DegreeBookID.StudentID.YBAP_ID.program.ProgramName
            classification = degree_information.Classification
            birth_of_date = degree_information.DegreeBookID.StudentID.DateOfBirth
            mssv = degree_information.DegreeBookID.StudentID.MSSV
            number_in_degree_book = degree_information.DegreeBookID.NumberInTheDegreeBook
            year_of_graduation = degree_information.YearOfGraduation
            
            # Trả về dữ liệu
            data = {
                'StudentName': student_name,
                'MajorName': major_name,
                'ProgramName': program_name,
                'Classification': classification,
                'BirthOfDate': birth_of_date,
                'MSSV': mssv,
                'NumberInTheDegreeBook': number_in_degree_book,
                'YearOfGraduation': year_of_graduation,
                'SerialNumber': serialNumber
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        except Degree_Information.DoesNotExist:
            return Response({"message": "Không tìm thấy thông tin"}, status=status.HTTP_404_NOT_FOUND)
        
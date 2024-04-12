from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken


from .models import *
from .serializers import *

class LoginTestCase(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_success(self):
        url = '/api/login'
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        # Kiểm tra token được trả về có hợp lệ không
        access_token = response.data['access']
        refresh_token = response.data['refresh']
        decoded_access_token = RefreshToken(access_token).payload
        decoded_refresh_token = RefreshToken(refresh_token).payload
        self.assertEqual(decoded_access_token['user_id'], str(self.user.id))
        self.assertEqual(decoded_refresh_token['user_id'], str(self.user.id))

    def test_login_failure(self):
        url = '/api/login'
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StudentAPITest(APITestCase):
    def setUp(self):
        # Tạo dữ liệu student
        self.student_data = {
            'StudentID': 1,
            'FirstName': 'John',
            'LastName': 'Doe',
            'Gender': '1',
            'DateOfBirth': '1990-01-01',
            'Address': '123 Main St, City',
            'Nation': 'Kinh',
            'Nationality': 'Vietnamese',
            'PhoneNumber': '123456789',
            'Email': 'john.doe@example.com',
            'MSSV': '123456',
            'YearOfAdmission': '2018'
        }
        # Tạo student object
        self.student = Student.objects.create(**self.student_data)
        # Tạo người dùng
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Tạo token JWT
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        

    ### Unit test for get list student
    def test_get_student_list(self):
        url = '/api/student'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        student = Student.objects.first()
        serializer = StudentSerializer(student)
        self.assertEqual(response.data, serializer.data)
    
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


# from django.contrib.auth.models import User
# from ecommerce.models import Item, Order
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APIClient
# from rest_framework.test import APITestCase
# from rest_framework import status


# class EcommerceTestCase(APITestCase):
    """
    Test suite for Items and Orders
    """
    def setUp(self):

        Item.objects.create(title= "Demo item 1",description= "This is a description for demo 1",price= 500,stock= 20)
        Item.objects.create(title= "Demo item 2",description= "This is a description for demo 2",price= 700,stock= 15)
        Item.objects.create(title= "Demo item 3",description= "This is a description for demo 3",price= 300,stock= 18)
        Item.objects.create(title= "Demo item 4",description= "This is a description for demo 4",price= 400,stock= 14)
        Item.objects.create(title= "Demo item 5",description= "This is a description for demo 5",price= 500,stock= 30)
        self.items = Item.objects.all()
        self.user = User.objects.create_user(
            username='testuser1', 
            password='this_is_a_test',
            email='testuser1@test.com'
        )
        Order.objects.create(item = Item.objects.first(), user = User.objects.first(), quantity=1)
        Order.objects.create(item = Item.objects.first(), user = User.objects.first(), quantity=2)
        
        #The app uses token authentication
        self.token = Token.objects.get(user = self.user)
        self.client = APIClient()
        
        #We pass the token in all calls to the API
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_get_all_items(self):
        '''
        test ItemsViewSet list method
        '''
        self.assertEqual(self.items.count(), 5)
        response = self.client.get('/item/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_item(self):
        '''
        test ItemsViewSet retrieve method
        '''
        for item in self.items:
            response = self.client.get(f'/item/{item.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_is_more_than_stock(self):
        '''
        test Item.check_stock when order.quantity > item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertEqual(i.check_stock(current_stock + 1), False)

    def test_order_equals_stock(self):
        '''
        test Item.check_stock when order.quantity == item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertEqual(i.check_stock(current_stock), True)

    def test_order_is_less_than_stock(self):
        '''
        test Item.check_stock when order.quantity < item.stock
        '''
        for i in self.items:
            current_stock = i.stock
            self.assertTrue(i.check_stock(current_stock - 1), True)
    
    def test_create_order_with_more_than_stock(self):
        '''
        test OrdersViewSet create method when order.quantity > item.stock
        '''
        for i in self.items:
            stock = i.stock
            data = {"item": str(i.id), "quantity": str(stock+1)}
            response = self.client.post(f'/order/', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_less_than_stock(self):
        '''
        test OrdersViewSet create method when order.quantity < item.stock
        '''
        for i in self.items:
            data = {"item": str(i.id), "quantity": 1}
            response = self.client.post(f'/order/',data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_order_with_equal_stock(self):
        '''
        test OrdersViewSet create method when order.quantity == item.stock
        '''
        for i in self.items:
            stock = i.stock
            data = {"item": str(i.id), "quantity": str(stock)}
            response = self.client.post(f'/order/',data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_orders(self):
        '''
        test OrdersViewSet list method
        '''
        self.assertEqual(Order.objects.count(), 2)
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_get_one_order(self):
        '''
        test OrdersViewSet retrieve method
        '''
        orders = Order.objects.filter(user = self.user)
        for o in orders:
            response = self.client.get(f'/order/{o.id}/')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
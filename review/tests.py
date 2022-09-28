from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from review import models as core_models

class TestCasebooking(APITestCase):

    def setup_user(self, name, email, is_admin):
        self.User_obj = get_user_model()
        self.user = self.User_obj.objects.create_user(
            name,
            email=email,
            password='test',
            is_superuser = is_admin,
            is_staff = is_admin
        )
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token {}'.format(
            self.token.key)
        
    def test_employee_cant_manage_employees(self):

        # create admin user
        self.setup_user("employee", "employee@employee.com", False)
        data = {
            "name": "employee0"
        }

        # create employee as admin
        created_employee = self.client.post('/api/employee/', data)
        # check if employee exists
        self.assertEqual(created_employee.status_code, 403)       

    def test_admin_can_manage_employees(self):

        # create admin user
        self.setup_user("admin", "admin@admin.com", True)
        data = {
            "name": "employee1"
        }

        # create employee as admin
        created_employee = self.client.post('/api/employee/', data)
        # check if employee exists
        self.assertEqual(created_employee.data['results']['id'], 1)       
        # check if employee created is created by admin user
        self.assertEqual(core_models.Employee.objects.all().first().manager.username, "admin")



'''
Admin view 

Add/remove/update/view employees
+ Model Employee

Add/update/view performance reviews 
+ Review

+ Assign employees to participate in another employee's performance review 
'''



'''
Employee view 

+ List of performance reviews requiring feedback

+ Submit feedback 
'''
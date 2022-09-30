from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from review import models as core_models

class TestCasePerformanceReview(APITestCase):

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
        
    '''
    Admin view 
    '''
    def test_employee_cant_manage_employees(self):

        # create admin user
        self.setup_user("employee", "employee@employee.com", False)
        data = {
            "name": "employee0"
        }

        # create employee as employee
        created_employee = self.client.post('/api/employee/', data)
        # check if status_code is 403
        self.assertEqual(created_employee.status_code, 403)       

    def test_admin_can_manage_employees(self):

        '''
        + Model Employee: Add/remove/update/view employees
        '''
        # create admin user
        self.setup_user("admin", "admin@admin.com", True)
        data = {
            "username": "employee1",#TODO: check if this fields are saved on database by viewset
            "first_name": "first1",
            "last_name": "last1",
            "password": "1234",
            "email": "emplo@emplo.com"
        }

        # create employee as admin
        created_employee = self.client.post('/api/employee/', data)
        # check if employee exists
        new_employee_id = created_employee.data['results']['id']
        self.assertEqual(new_employee_id, 1)    
        # check if employee has first_name
        new_employee_first_name = created_employee.data['results']['first_name']
        self.assertEqual(new_employee_first_name, "first1")  
        # check if employee has last_name
        new_employee_last_name = created_employee.data['results']['last_name']
        self.assertEqual(new_employee_last_name, "last1")       
        # check if employee created is created by admin user
        self.assertEqual(core_models.Employee.objects.all().first().manager.username, "admin")

        # retrieve employee by id
        ret_employee = self.client.get(f'/api/employee/{new_employee_id}/')
        self.assertEqual(ret_employee.data['results']['id'], 1)     
        
        # partial update employee by id
        data = {
            "first_name": "first1_changed",
            "last_name": "last1_changed"
        }
        patch_employee = self.client.patch(f'/api/employee/{new_employee_id}/', data)
        self.assertEqual(patch_employee.data['results']['id'], 1)     
        # check if employee has changed first_name
        patch_employee_first_name = patch_employee.data['results']['first_name']
        self.assertEqual(patch_employee_first_name, "first1_changed")  
        # check if employee has changed last_name
        patch_employee_last_name = patch_employee.data['results']['last_name']
        self.assertEqual(patch_employee_last_name, "last1_changed")
          
        # delete employee by id
        self.assertEqual(core_models.Employee.objects.all().count(), 1)    
        ret_employee = self.client.delete(f'/api/employee/{new_employee_id}/')
        self.assertEqual(core_models.Employee.objects.all().count(), 0)

    def test_admin_can_manage_review(self):
        '''
        Add/update/view performance reviews 
        + Review

        + Assign employees to participate in another employee's performance review, !!??
        '''
        self.setup_user("admin2", "admin2@admin2.com", True)
        # create employee for review test
        data = {
            "username": "employee1",#TODO: check if this fields are saved on database by viewset
            "first_name": "first1",
            "last_name": "last1",
            "password": "1234",
            "email": "emplo@emplo.com"
        }

        # create employee as admin2
        created_employee = self.client.post('/api/employee/', data)
        data = {
            "employee_id": 1,
            "rate": 5,
            "text": "text text text text text text",
        }
        
        # create review as admin2
        created_review = self.client.post('/api/review/', data)
        # check if review exists
        new_review_id = created_review.data['results']['id']
        self.assertEqual(new_review_id, 1) 

        # retrieve review by id
        ret_review = self.client.get(f'/api/review/{new_review_id}/')
        self.assertEqual(ret_review.data['results']['id'], 1)

        # partial update review by id
        data = {
            "rate": 2,
            "text": "Text changed"
        }
        patch_review = self.client.patch(f'/api/review/{new_review_id}/', data)
        self.assertEqual(patch_review.data['results']['id'], 1)     
        # check if review has changed first_name
        patch_review_rate = patch_review.data['results']['rate']
        self.assertEqual(patch_review_rate, 2)  
        # check if review has changed last_name
        patch_review_text = patch_review.data['results']['text']
        self.assertEqual(patch_review_text, "Text changed")


'''
Employee view 

+ List of performance reviews requiring feedback

+ Submit feedback 
'''
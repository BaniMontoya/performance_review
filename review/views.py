from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from review import models as review_models
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User

class EmployeeViewSet(ViewSet):

    permission_classes = (IsAdminUser,)

    def list(self, request):
        return Response({"Message": "Error"}, status=400)


    def create(self, request):
        
        employee_user = User.objects.create_user(username='name',
                                 email='todo@change.with_var',
                                 password='1234')
        employee = review_models.Employee.objects.create(manager=request.user, user=employee_user)
        return Response({"results": {"id":employee.id}}, status=201)


    def retrieve(self, request, pk=None):
        return Response({"Message": "Error"}, status=400)


    def update(self, request, pk=None):
        return Response({"Message": "Error"}, status=400)


    def destroy(self, request, pk=None):
        return Response({"Message": "Error"}, status=401)



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
        data = request.data

        employee_user = User.objects.create_user(
            username=data.get("username", 1),
            email=data.get("email", 1),
            password=data.get("password", 1),
            first_name=data.get("first_name", 1),
            last_name=data.get("last_name", 1)
        )
        employee = review_models.Employee.objects.create(
            manager=request.user, user=employee_user)
        return Response({
            "results": {
                "id": employee.id,
                "first_name": employee.user.first_name,
                "last_name": employee.user.last_name
            }
        }, status=201)

    def retrieve(self, request, pk=None):
        employee = review_models.Employee.objects.filter(id=pk).first()
        if employee:
            return Response({"results": {"id": employee.id}}, status=200)
        else:
            return Response({"results": "User not exists"}, status=404)

    def update(self, request, pk=None):
        data = request.data

        return Response({"Message": "Error"}, status=400)

    def destroy(self, request, pk=None):
        return Response({"Message": "Error"}, status=401)

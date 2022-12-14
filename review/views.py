from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from review import models as review_models
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User


class EmployeeViewSet(ViewSet):

    permission_classes = (IsAdminUser,)

    def list(self, request):

        return Response({"Message": "Not implement function for Employee."}, status=404)

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
            return Response({"results": "Employee not exists"}, status=404)

    def partial_update(self, request, pk=None):
        
        data = request.data
        employee = review_models.Employee.objects.filter(id=pk).first()
        if employee:
            employee.user.first_name = data.get("first_name", employee.user.first_name)
            employee.user.last_name = data.get("last_name", employee.user.last_name)
            employee.user.save()
            employee = review_models.Employee.objects.filter(id=pk).first()
            return Response({
                "results": {
                    "id": employee.id,
                    "first_name": employee.user.first_name,
                    "last_name": employee.user.last_name
                }}, status=200)
        else:
            return Response({"results": "Employee not exists"}, status=404)

    def destroy(self, request, pk=None):

        employee = review_models.Employee.objects.filter(id=pk).first()
        if employee:
            employee.delete()
            return Response({"results": {"id": employee.id}}, status=200)
        else:
            return Response({"results": "Employee not exists"}, status=404)

class ReviewViewSet(ViewSet):

    permission_classes = (IsAuthenticated,)

    def list(self, request):

        return Response({"Message": "Not implement function for Review."}, status=404)

    def create(self, request):

        data = request.data
        employee = review_models.Employee.objects.filter(id=int(data.get("employee_id",0))).first()
        if employee:
            review = review_models.Review.objects.create(
                reviewer=request.user, 
                employee=employee,
                rate=data.get("rate",0),
                text=data.get("text","")
                )
            return Response({
                "results": {
                    "id": review.id,
                    "rate": review.rate,
                    "text": review.text
                }
            }, status=201)
        else:
            return Response({"results": "Employee not exists"}, status=404)

    def retrieve(self, request, pk=None):
        
        review = review_models.Review.objects.filter(id=pk).first()
        if review:
            return Response({"results": {"id": review.id}}, status=200)
        else:
            return Response({"results": "Employee not exists"}, status=404)

    def partial_update(self, request, pk=None):
        
        data = request.data
        review = review_models.Review.objects.filter(id=pk).first()
        if review:
            review.rate = data.get("rate", review.rate)
            review.text = data.get("text", review.text)
            review.save()
            review = review_models.Review.objects.filter(id=pk).first()
            return Response({
                "results": {
                    "id": review.id,
                    "rate": review.rate,
                    "text": review.text
                }}, status=200)
        else:
            return Response({"results": "Review not exists"}, status=404)
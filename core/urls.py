from rest_framework.routers import SimpleRouter
from review import views
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path


router = SimpleRouter()

router.register(r'api/employee',
                views.EmployeeViewSet, 'Employee')

urlpatterns = router.urls
urlpatterns += [
    path('api-token-auth/', obtain_auth_token,
         name='api_token_auth'),
]

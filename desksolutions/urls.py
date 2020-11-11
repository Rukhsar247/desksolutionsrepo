from django.urls import path
from desksolutions.views import OrganizationRegister, signup

app_name = "signup"

urlpatterns = [
    path('', OrganizationRegister, name="home"),
    path('profile/', signup, name='signups'),
]

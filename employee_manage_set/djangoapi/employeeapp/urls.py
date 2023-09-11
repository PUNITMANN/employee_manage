from django.urls import re_path
from employeeapp import views


urlpatterns = [
    re_path(r'^department$', views.departmentApi),
    re_path(r'^department/([0-9]+)$', views.departmentApi),
    re_path(r'^employee$', views.employeeApi),
    re_path(r'^employee/([0-9]+)$', views.employeeApi),
    re_path(r'^department-list$', views.departmentlistApi),
]






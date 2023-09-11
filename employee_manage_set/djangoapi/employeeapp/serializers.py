from rest_framework import serializers
from employeeapp.models import Departments, Employees, DepartmentLists


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ('DepartmentId', 'DepartmentName', 'CreatedTime', 'ModifiedTime')


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ('EmployeeId', 'EmployeeName', 'EmployeeDepartment', 'DateOfJoining')


class DepartmentListsSerializers(serializers.ModelSerializer):
    class Meta:
        model = DepartmentLists
        fields = ('DeptListId', 'DeptListName')

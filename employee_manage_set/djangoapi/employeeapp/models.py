from django.db import models

# Create your models here.


class Departments(models.Model):
    DepartmentId = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=500)
    CreatedTime = models.DateTimeField(auto_now_add=True)
    ModifiedTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.DepartmentName


class Employees(models.Model):
    EmployeeId = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=500)
    EmployeeDepartment = models.CharField(max_length=500)
    DateOfJoining = models.DateTimeField(auto_now_add=True)
    # PhotoFileName = models.CharField(max_length=500)

    def __str__(self):
        return self.EmployeeName


class DepartmentLists(models.Model):
    DeptListId = models.AutoField(primary_key=True)
    DeptListName = models.CharField(max_length=500)

    def __str__(self):
        return self.DeptListName

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from employeeapp.models import Departments, Employees, DepartmentLists
from employeeapp.serializers import DepartmentSerializers, EmployeeSerializers, DepartmentListsSerializers

# Create your views here.


@csrf_exempt
def departmentApi(request, id=0):
    if request.method == 'GET':
        departments = Departments.objects.all()
        department_serializers = DepartmentSerializers(departments, many=True)

        if not departments:
            return JsonResponse({"message": "Data not Found"})
        return JsonResponse(department_serializers.data, safe=False)

    if request.method == 'POST':
        department_data = JSONParser().parse(request)
        department_name = department_data.get('DepartmentName', None)
        if not department_name:
            return JsonResponse({"message": "DepartmentName is required."}, safe=False)

        department_list_exists = DepartmentLists.objects.filter(DeptListName=department_name).exists()
        if not department_list_exists:
            return JsonResponse({"message": "DepartmentName is not Registered with the Company."}, safe=False)

        department_exists = Departments.objects.filter(DepartmentName=department_name).exists()
        if department_exists:
            return JsonResponse({"message": "DepartmentName is Already Exists."}, safe=False)

        department_serializers = DepartmentSerializers(data=department_data)
        if department_serializers.is_valid():
            department_serializers.save()
            return JsonResponse({"message": "Added Successfully"}, safe=False)
        return JsonResponse({"message": "Failed to Add"}, safe=False)
    if request.method == "PUT":
        department_data = JSONParser().parse(request)
        department_name = department_data.get('DepartmentName', None)
        department_id = department_data.get('DepartmentId', None)
        if not department_name:
            return JsonResponse({"message": "Department Name is Required"}, safe=False)
        if not department_id:
            return JsonResponse({"message": "DepartmentId is Required."}, safe=False)

        department_list_exists = DepartmentLists.objects.filter(DeptListName=department_name).exists()
        if not department_list_exists:
            return JsonResponse({"message": "DepartmentName is not Registered with the Company."}, safe=False)

        if department_id:
            try:
                existing_department = Departments.objects.get(DepartmentId=department_id)
                if existing_department.DepartmentName != department_name:
                    department_exists = Departments.objects.filter(DepartmentName=department_name).exists()
                    if department_exists:
                        return JsonResponse({"message": "Department Name Already Exists"}, safe=False)
            except Departments.DoesNotExist:
                return JsonResponse({"message": "Department Not Found with the provided EmployeeId."}, safe=False)
            department_serializers = DepartmentSerializers(existing_department, data=department_data)
            if department_serializers.is_valid():
                department_serializers.save()
                return JsonResponse({"message": "Updated Successfully"}, safe=False)
            return JsonResponse({"message": "Failed to Update"}, safe=False)
    if request.method == 'DELETE':
        try:
            department_id = int(id)
        except (ValueError, TypeError):
            return JsonResponse({"message": "DepartmentId should be an integer."}, safe=False)
        try:
            department_exists = Departments.objects.filter(DepartmentId=department_id).exists()
            if not department_exists:
                return JsonResponse({"message": "Department does not Exists."}, safe=False)
            department = Departments.objects.get(DepartmentId=department_id)
            if department.delete():
                return JsonResponse({"message": "Delete Successfully"}, safe=False)
            return JsonResponse({"message": "Failed to Delete"}, safe=False)
        except Departments.DoesNotExist:
            return JsonResponse({"message": "Department Not Found."}, safe=False)


@csrf_exempt
def employeeApi(request, id=0):
    if request.method == "GET":
        employees = Employees.objects.all()
        employees_serializers = EmployeeSerializers(employees, many=True)
        if not employees:
            return JsonResponse({"message": "Data Not Found"}, safe=False)
        return JsonResponse(employees_serializers.data, safe=False)
    if request.method == "POST":
        employees_data = JSONParser().parse(request)
        employee_name = employees_data.get('EmployeeName', None)
        employee_department = employees_data.get('EmployeeDepartment', None)
        if not employee_name:
            return JsonResponse({"message": "Employee Name is Required"})
        if not employee_department:
            return JsonResponse({"message": "Employee Department is Required"})
        employee_exists = Employees.objects.filter(EmployeeName=employee_name).exists()
        if employee_exists:
            return JsonResponse({"message": "Employee Name Already Exists"}, safe=False)
        department_exists = Departments.objects.filter(DepartmentName=employee_department).exists()
        if not department_exists:
            return JsonResponse({"message": "DepartmentName does not Exists."}, safe=False)
        employee_serializers = EmployeeSerializers(data=employees_data)
        if employee_serializers.is_valid():
            employee_serializers.save()
            return JsonResponse({"message": "Added Successfully"}, safe=False)
        return JsonResponse({"message": "Failed to Add"}, safe=False)
    if request.method == "PUT":
        employee_data = JSONParser().parse(request)
        employee_name = employee_data.get('EmployeeName', None)
        employee_id = employee_data.get('EmployeeId', None)
        employee_department = employee_data.get('EmployeeDepartment', None)
        if not employee_department:
            return JsonResponse({"message": "Employee Department is Required"})
        if not employee_name:
            return JsonResponse({"message": "Employee Name is Required"}, safe=False)
        if not employee_id:
            return JsonResponse({"message": "EmployeeId is required."}, safe=False)
        department_exists = Departments.objects.filter(DepartmentName=employee_department).exists()
        if not department_exists:
            return JsonResponse({"message": "DepartmentName does not Exists."}, safe=False)
        if employee_id:
            try:
                existing_employee = Employees.objects.get(EmployeeId=employee_id)
                if existing_employee.EmployeeName != employee_name:
                    employee_exists = Employees.objects.filter(EmployeeName=employee_name).exists()
                    if employee_exists:
                        return JsonResponse({"message": "Employee Name Already Exists"}, safe=False)
            except Employees.DoesNotExist:
                return JsonResponse({"message": "Employee Not Found with the provided EmployeeId."}, safe=False)
            employee_serializers = EmployeeSerializers(existing_employee, data=employee_data)
            if employee_serializers.is_valid():
                employee_serializers.save()
                return JsonResponse({"message": "Updated Successfully"}, safe=False)
            return JsonResponse({"message": "Failed to Update"}, safe=False)
    if request.method == "DELETE":
        try:
            employee_id = int(id)
        except (ValueError, TypeError):
            return JsonResponse({"message": "EmployeeId should be an integer."}, safe=False)
        try:
            employee_exists = Employees.objects.filter(EmployeeId=employee_id).exists()
            if not employee_exists:
                return JsonResponse({"message": "Employee does not Exists"}, safe=False)
            employee = Employees.objects.get(EmployeeId=employee_id)
            if employee.delete():
                return JsonResponse({"message": "Deleted Successfully"}, safe=False)
            return JsonResponse({"message": "Failed to Delete"}, safe=False)
        except Employees.DoesNotExist:
            return JsonResponse({"message": "Employee Not Found"}, safe=False)



@csrf_exempt
def departmentlistApi(request):
    if request.method == 'GET':
        departments_lists = DepartmentLists.objects.all()
        departments_lists_serializers = DepartmentListsSerializers(departments_lists, many=True)

        if not departments_lists:
            return JsonResponse({"message": "Data not Found"})
        return JsonResponse(departments_lists_serializers.data, safe=False)

    if request.method == 'POST':
        department_list_data = JSONParser().parse(request)
        department_name = department_list_data.get('DeptListName', None)
        if not department_name:
            return JsonResponse({"message": "DepartmentName is required."}, safe=False)
        department_exists = DepartmentLists.objects.filter(DeptListName=department_name).exists()
        if department_exists:
            return JsonResponse({"message": "DepartmentName is Already Exists."}, safe=False)

        department_serializers = DepartmentListsSerializers(data=department_list_data)
        if department_serializers.is_valid():
            department_serializers.save()
            return JsonResponse({"message": "Added Successfully"}, safe=False)
        return JsonResponse({"message": "Failed to Add"}, safe=False)


from django.contrib import admin
from .models import Department, Employee, Attendance, SalarySlip

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'dept_name', 'created_at']
    search_fields = ['dept_name']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'base_salary', 'join_date']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'month', 'working_days', 'present_days', 'overtime_hours']
    list_filter = ['month']
    search_fields = ['employee__name']

@admin.register(SalarySlip)
class SalarySlipAdmin(admin.ModelAdmin):
    list_display = ['id', 'employee', 'month', 'total_salary', 'calculated_at']
    list_filter = ['month']
    search_fields = ['employee__name']
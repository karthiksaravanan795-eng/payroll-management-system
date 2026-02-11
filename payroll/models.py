from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    dept_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.dept_name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    join_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # Format: Jan-2024
    working_days = models.IntegerField()
    present_days = models.IntegerField()
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['employee', 'month']
    
    def __str__(self):
        return f"{self.employee.name} - {self.month}"

class SalarySlip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    present_days = models.IntegerField()
    working_days = models.IntegerField()
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2)
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2)
    total_salary = models.DecimalField(max_digits=12, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee.name} - {self.month} - ₹{self.total_salary}"
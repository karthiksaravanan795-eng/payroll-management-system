from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Department, Employee, Attendance, SalarySlip

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']
        widgets = {
            'dept_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter department name'
            })
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'department', 'base_salary']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter employee name'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'base_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter base salary',
                'min': '0',
                'step': '0.01'
            })
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'month', 'working_days', 'present_days', 'overtime_hours']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Format: Jan-2024'
            }),
            'working_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter working days',
                'min': '1',
                'max': '31'
            }),
            'present_days': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter present days',
                'min': '0'
            }),
            'overtime_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter overtime hours',
                'min': '0',
                'step': '0.5'
            })
        }

class SalaryCalculationForm(forms.Form):
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    month = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Format: Jan-2024'
        })
    )
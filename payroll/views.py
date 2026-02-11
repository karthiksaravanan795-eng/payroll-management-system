from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Sum, Q
from .models import *
from .forms import *
import decimal

# ========================
# PERMISSION DECORATORS
# ========================
def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

def manager_required(view_func):
    return user_passes_test(lambda u: u.groups.filter(name='Manager').exists() or u.is_superuser)(view_func)

def hr_required(view_func):
    return user_passes_test(lambda u: u.groups.filter(name='HR').exists() or u.is_superuser)(view_func)

# ========================
# AUTHENTICATION VIEWS
# ========================
def custom_login(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Redirect based on user type
            if user.is_superuser:
                return redirect('admin_panel')
            elif user.groups.filter(name='Manager').exists():
                return redirect('manager_panel')
            elif user.groups.filter(name='HR').exists():
                return redirect('hr_panel')
            else:
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'payroll_app/login.html')

@login_required
def custom_logout(request):
    """Custom logout view"""
    logout(request)
    return redirect('login')

# ========================
# ADMIN VIEWS
# ========================
@login_required
@admin_required
def admin_panel(request):
    """Admin dashboard"""
    total_employees = Employee.objects.count()
    total_departments = Department.objects.count()
    total_salary_paid = SalarySlip.objects.aggregate(total=Sum('total_salary'))['total'] or 0
    
    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'total_salary_paid': total_salary_paid,
    }
    return render(request, 'payroll_app/admin_panel.html', context)

@login_required
@admin_required
def add_department(request):
    """Add new department"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully!')
            return redirect('add_department')
    else:
        form = DepartmentForm()
    
    return render(request, 'payroll_app/add_department.html', {'form': form})

# ========================
# MANAGER VIEWS
# ========================
@login_required
@manager_required
def manager_panel(request):
    """Manager dashboard"""
    return render(request, 'payroll_app/manager_panel.html')

# ========================
# HR VIEWS
# ========================
@login_required
@hr_required
def hr_panel(request):
    """HR dashboard"""
    return render(request, 'payroll_app/hr_panel.html')

# ========================
# COMMON VIEWS
# ========================
@login_required
def add_employee(request):
    """Add new employee"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee added successfully!')
            return redirect('add_employee')
    else:
        form = EmployeeForm()
    
    return render(request, 'payroll_app/add_employee.html', {'form': form})

@login_required
def view_employees(request):
    """View all employees"""
    employees = Employee.objects.select_related('department').all()
    return render(request, 'payroll_app/view_employees.html', {'employees': employees})

@login_required
def record_attendance(request):
    """Record employee attendance"""
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance recorded successfully!')
            return redirect('record_attendance')
    else:
        form = AttendanceForm()
    
    return render(request, 'payroll_app/record_attendance.html', {'form': form})

@login_required
def calculate_salary(request):
    """Calculate salary for employee"""
    if request.method == 'POST':
        form = SalaryCalculationForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            month = form.cleaned_data['month']
            
            try:
                attendance = Attendance.objects.get(employee=employee, month=month)
                
                # Calculate salary
                daily_salary = employee.base_salary / attendance.working_days
                earned_salary = daily_salary * attendance.present_days
                overtime_pay = attendance.overtime_hours * decimal.Decimal('100')
                total_salary = earned_salary + overtime_pay
                
                # Create salary slip
                salary_slip = SalarySlip.objects.create(
                    employee=employee,
                    month=month,
                    base_salary=employee.base_salary,
                    present_days=attendance.present_days,
                    working_days=attendance.working_days,
                    overtime_hours=attendance.overtime_hours,
                    overtime_pay=overtime_pay,
                    total_salary=total_salary
                )
                
                context = {
                    'form': form,
                    'calculated': True,
                    'employee': employee,
                    'month': month,
                    'base_salary': employee.base_salary,
                    'present_days': attendance.present_days,
                    'working_days': attendance.working_days,
                    'overtime_hours': attendance.overtime_hours,
                    'daily_salary': daily_salary,
                    'earned_salary': earned_salary,
                    'overtime_pay': overtime_pay,
                    'total_salary': total_salary,
                    'salary_slip': salary_slip
                }
                
                messages.success(request, 'Salary calculated successfully!')
                return render(request, 'payroll_app/calculate_salary.html', context)
                
            except Attendance.DoesNotExist:
                messages.error(request, 'Attendance record not found for this month!')
    
    else:
        form = SalaryCalculationForm()
    
    return render(request, 'payroll_app/calculate_salary.html', {'form': form})

@login_required
@admin_required
def view_all_data(request):
    """View all data - Admin only"""
    departments = Department.objects.all()
    employees = Employee.objects.select_related('department').all()
    salary_slips = SalarySlip.objects.select_related('employee').all()
    
    context = {
        'departments': departments,
        'employees': employees,
        'salary_slips': salary_slips
    }
    
    return render(request, 'payroll_app/view_all_data.html', context)

@login_required
def view_reports(request):
    """View salary reports"""
    salary_reports = SalarySlip.objects.select_related('employee__department').all()
    total_payout = salary_reports.aggregate(total=Sum('total_salary'))['total'] or 0
    
    context = {
        'salary_reports': salary_reports,
        'total_payout': total_payout
    }
    
    return render(request, 'payroll_app/view_reports.html', context)

@login_required
def salary_report(request, slip_id):
    """View individual salary slip"""
    salary_slip = get_object_or_404(SalarySlip, id=slip_id)
    return render(request, 'payroll_app/salary_report.html', {'salary_slip': salary_slip})

# ========================
# HELPER FUNCTIONS
# ========================
def create_default_users():
    """Create default users for the system"""
    try:
        # Create groups
        manager_group, _ = Group.objects.get_or_create(name='Manager')
        hr_group, _ = Group.objects.get_or_create(name='HR')
        
        # Create users
        users_data = [
            {'username': 'admin', 'password': 'admin123', 'is_superuser': True},
            {'username': 'manager', 'password': 'manager123', 'group': manager_group},
            {'username': 'hr', 'password': 'hr123', 'group': hr_group},
        ]
        
        for user_data in users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    password=user_data['password']
                )
                
                if user_data.get('is_superuser'):
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                else:
                    user.groups.add(user_data['group'])
        
        return True
    except Exception as e:
        print(f"Error creating users: {e}")
        return False
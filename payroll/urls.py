from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    # Admin URLs
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('add-department/', views.add_department, name='add_department'),
    
    # Manager URLs
    path('manager-panel/', views.manager_panel, name='manager_panel'),
    
    # HR URLs
    path('hr-panel/', views.hr_panel, name='hr_panel'),
    
    # Common URLs
    path('add-employee/', views.add_employee, name='add_employee'),
    path('view-employees/', views.view_employees, name='view_employees'),
    path('record-attendance/', views.record_attendance, name='record_attendance'),
    path('calculate-salary/', views.calculate_salary, name='calculate_salary'),
    path('view-all-data/', views.view_all_data, name='view_all_data'),
    path('view-reports/', views.view_reports, name='view_reports'),
    path('salary-report/<int:slip_id>/', views.salary_report, name='salary_report'),
]
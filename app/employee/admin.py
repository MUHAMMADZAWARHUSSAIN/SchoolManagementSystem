from django.contrib import admin
from django.contrib import admin
from .models import Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('employee_id', 'employee_name', 'email', 'contact_no', 'employee_status', 'date_of_joining', 'is_verified')

    # Fields to include in the search functionality
    search_fields = ('employee_name', 'employee_id', 'email', 'contact_no')

    # Fields to filter by in the admin interface
    list_filter = ('employee_status', 'gender', 'martial_status', 'date_of_joining', 'wing', 'province')

    # Default ordering of records
    ordering = ('date_of_joining',)

    # Optional: Add pagination
    list_per_page = 20  # Adjust this number as needed
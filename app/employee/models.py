'''
from django.db import models

class Employee(models.Model):
    employee_name = models.CharField(max_length=255)
    employee_id = models.CharField(max_length=50, unique=True)
    designation = models.ForeignKey('EmployeeDesignation', on_delete=models.SET_NULL, null=True)
    date_of_joining = models.DateField()
    contact_number = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.employee_name} ({self.employee_id})"

class EmployeeDesignation(models.Model):
    department = models.CharField(max_length=255)
    description = models.TextField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Qualification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    discipline = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    year_obtained = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.employee.employee_name} - {self.discipline}"

'''
from app.common.models import TimeStampedModel
from django.db import models
class Employee(TimeStampedModel, models.Model):
    account_no = models.CharField(max_length=50)
    address = models.TextField()
    bank = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    cnic = models.CharField(max_length=15)
    contact_no = models.CharField(max_length=15)
    country = models.CharField(max_length=50)
    covid_vaccinated = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    date_of_rejoining = models.DateField(null=True, blank=True)  # Optional field
    date_of_resignation = models.DateField(null=True, blank=True)  # Optional field
    email = models.EmailField(unique=True)
    employee_id = models.CharField(max_length=20, unique=True)
    employee_name = models.CharField(max_length=100)
    employee_status = models.CharField(max_length=20)
    father_cnic = models.CharField(max_length=15)
    father_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    martial_status = models.CharField(max_length=10)
    note = models.TextField(null=True, blank=True)  # Optional field
    province = models.CharField(max_length=50)
    wing = models.CharField(max_length=50)

    def __str__(self):
        return self.employee_name
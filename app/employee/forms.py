
from django import forms
from .models import Employee
from .models import StaffPerformance, Qualification
from .models import EmployeeDesignation

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        
        fields = [
             'employee_name', 'employee_id', 'designation', 'employee_pay_structure', 'account_no',
             'address', 'bank', 'city', 'cnic', 'contact_no', 'country', 'covid_vaccinated',
             'date_of_birth', 'date_of_joining', 'email', 'employee_status', 'father_cnic', 'father_name',
             'gender', 'is_verified', 'martial_status', 'province', 'wing',
             
         ]
        
        widgets = {
            'employee_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee name'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee ID'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'employee_pay_structure': forms.Select(attrs={'class': 'form-control'}),
            'account_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter account number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'bank': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter bank name'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'cnic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter CNIC number'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),
            'covid_vaccinated': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
            'employee_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter employee status'}),
            
            # Newly added fields
            'father_cnic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter father CNIC number'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter father name'}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female')], attrs={'class': 'form-control'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'martial_status': forms.Select(choices=[('Single', 'Single'), ('Married', 'Married')], attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter province'}),
            'wing': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter wing'}),
        }
class StaffPerformanceForm(forms.ModelForm):
    class Meta:
        model = StaffPerformance
        fields = ['employee', 'comments', 'rating', 'date_evaluated']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter comments'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter rating'}),
            'date_evaluated': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Enter evaluation date', 'type': 'date'}),
        }

class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['employee', 'discipline', 'institution', 'name', 'year_obtained']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'discipline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter discipline'}),
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter institution'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter qualification name'}),
            'year_obtained': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter year obtained'}),
        }

class EmployeeDesignationForm(forms.ModelForm):
    class Meta:
        model = EmployeeDesignation
        fields = ['name', 'department', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter designation name'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter department'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Designation Name"
        self.fields['department'].label = "Department"
        self.fields['description'].label = "Description"
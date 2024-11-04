from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import UpdateView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import CustomUser,Role,Profile
from .forms import CustomUserForm, LoginForm, ResetPasswordForm,ForgetPasswordForm ,ProfileForm
from app.account.utils.generate_Token import generate_verification_token
from app.account.utils.decodeVerficationToken import decode_verification_token
import jwt
from django.views import View
from app.assignment.models import Assignment,Submission
from app.academic.models import Course
from django.contrib import messages




@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    context = {'profile': profile}
    return render(request, 'accounts/profiles/profile.html', context)

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profiles/edit_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)
def get_student_data(request):
    upcoming_events = [
        {'name': 'Assignment 1', 'date': '2024-11-10'},
        {'name': 'Exam 1', 'date': '2024-11-15'}
    ]
    announcements = [
        {'message': 'School will be closed on November 5th.'},
        {'message': 'New library books are available.'}
    ]
    # Assuming you have models for grades and assignments
    recent_grades = Submission.objects.filter(student=request.user.id)
    # ... (fetch other data: my_courses, attendance_summary) ...
    context = {
        'upcoming_events': upcoming_events,
        'announcements': announcements,
        'recent_grades': recent_grades,
        'my_courses': Course.objects.all(),  # Example: Fetch all courses
        'attendance_summary': {'present': 20, 'absent': 2}  # Replace with actual data
    }
    return context

@login_required
def student_dashboard(request):
    """
    Renders the student dashboard with relevant data.
    """
    context = get_student_data(request)
    return render(request, 'accounts/dashboards/student_dashboard.html', context)


def get_teacher_data(request):
    # Assuming you have models for courses and assignments
    my_courses = Course.objects.all()  # Example: Fetch all courses
    recent_assignments = Assignment.objects.all()  # Example: Fetch all assignments
    pending_submissions = Submission.objects.filter(
        assignment__course__in=my_courses, status='not_submitted'
    )
    # ... (fetch other data: announcements) ...
    context = {
        'my_courses': my_courses,
        'recent_assignments': recent_assignments,
        'pending_submissions': pending_submissions,
        'announcements': [
            {'message': 'Staff meeting on November 6th.'},
            {'message': 'New curriculum updates available.'}
        ]
    }
    return context

@login_required
def teacher_dashboard(request):
    """
    Renders the teacher dashboard with relevant data.
    """
    context = get_teacher_data(request)
    return render(request, 'accounts/dashboards/teacher_dashboard.html', context)


def get_staff_data(request):
    # ... (fetch data for staff dashboard) ...
    context = {
        'tasks': [
            {'name': 'Process payments', 'status': 'Pending'},
            {'name': 'Generate reports', 'status': 'Completed'}
        ],
        'announcements': [
            {'message': 'Payroll processed.'},
            {'message': 'Holiday schedule updated.'}
        ]
    }
    return context

@login_required
def staff_dashboard(request):
    """
    Renders the staff dashboard with relevant data.
    """
    context = get_staff_data(request)
    return render(request, 'accounts/dashboards/staff_dashboard.html', context)


class SignupView(FormView):
    template_name = 'accounts/authentication/signup.html'
    form_class = CustomUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()  # Let the form handle the initial save
        default_role = Role.objects.get(name='pending')
        user.role = default_role
        user.save()  # Save again to update the role
        messages.success(self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)
    # def form_valid(self, form):
    #     try:
    #         user = form.save(commit=False)
    #         default_role = Role.objects.get(name='pending') 
    #         print(default_role) # Get the default role
    #         user.role = default_role
    #         user.save()
    #         messages.success(self.request, 'Account created successfully! Please log in.')
    #     except Exception as e:
    #         messages.error(self.request,f'Error creating form {e}')
    
    #     return super().form_valid(form)

# Login View
class LoginView(FormView):
    template_name = 'accounts/authentication/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('student_dashboard')
    redirect_authenticated_user = True

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, f'Welcome, {user.username}!')
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid username or password.")
            # form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)

# Logout View
class LogoutView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


# Send Email Verification
class SendEmailVerificationView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/authentication/verify_email.html'

    def post(self, request):
        user = request.user
        if not user.email_verified:
            token = generate_verification_token(user.pk)
            user.token_created_at = timezone.now()
            user.token_expiry_time = timezone.now() + timezone.timedelta(minutes=30)
            user.save()
            
            verification_link = f"{settings.FRONTEND_URL}/verify_email/?token={token}"
            send_mail(
                'Email Verification Request',
                f"Here is your email verification link: {verification_link}",
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            return redirect('email_sent')
        return redirect('profile')

# Verify Email View
class EmailVerifyView(TemplateView):
    template_name = 'accounts/authentication/verify_email_result.html'

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(pk=payload['user_id'])
            if user.is_token_valid():
                user.email_verified = True
                user.save()
                return render(request, self.template_name, {'message': "Email verified successfully"})
            return render(request, self.template_name, {'message': "Token has expired"})
        except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
            return render(request, self.template_name, {'message': "Invalid token"})
        
class ForgetPasswordView(FormView):
    template_name = 'accounts/authentication/forget_password.html'
    form_class = ForgetPasswordForm  # Use custom form
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        print("ForgetPasswordView: form_valid called") 
        print(f"Email submitted: {email}")  # Debugging statement

        # Fetch the user
        user = CustomUser.objects.filter(email=email).first()
        if user:
            print("User found with this email.")  # Debugging statement
            token = generate_verification_token(user.pk)
            reset_link = f"{settings.FRONTEND_URL}/reset_password/?token={token}"
            
            # Send email with reset link
            send_mail(
                'Password Reset Request',
                f"Here is your password reset link: {reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
            )
            return render(self.request, 'email_sent.html', {'message':messages.success(self.request, 'Password reset link has been sent to your email.')
})
        else:
            print("No user found with this email.")  # Debugging statement
            return render(self.request, 'accounts/authentication/forget_password.html', {'error': messages.error(self.request, 'User with this email does not exist.')})

class ResetPasswordView(View):
    template_name = 'accounts/authentication/reset_password.html'

    def get(self, request):
        # Token verification
        token = request.GET.get('token')
        user_id = decode_verification_token(token)  # Extracts user ID from token

        if user_id:
            request.session['reset_user_id'] = user_id
            form = ResetPasswordForm()
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'error.html', {'message': 'Invalid or expired token.'})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        user_id = request.session.get('reset_user_id')

        if not user_id:
            return render(request, 'error.html', {'message': 'Session expired. Try again.'})

        if form.is_valid():
            user = CustomUser.objects.get(pk=user_id)
            password = form.cleaned_data['password']
            user.password = make_password(password)
            user.save()
            messages.success(request, 'Password reset successfully!')
            # Clear session after reset
            del request.session['reset_user_id']
            return redirect(reverse_lazy('login'))
        else:
            return render(request, self.template_name, {'form': form})

@login_required
def redirect_to_dashboard(request):
    if request.user.role.name == 'student':
        return redirect('student_dashboard')
    elif request.user.role.name == 'teacher':
        return redirect('teacher_dashboard')
    elif request.user.role.name == 'staff':
        return redirect('staff_dashboard')
    # ... handle other roles ...
    else:
        return redirect('home')  # Or some other default page


def home(request):
    context = {
        'school_name': 'Army Public School',
        'about_school': 'Army Public School is a renowned educational institution committed to providing quality education and holistic development to students. We offer a comprehensive curriculum, experienced faculty, and state-of-the-art facilities to foster academic excellence and personal growth.',
        'admission_info': {
            'open': True,
            'last_date': '2024-12-15',
            'classes': 'Pre-Nursery to 12th Grade',
            'process': 'Visit the school office to obtain an admission form. Submit the completed form along with the required documents by the last date.',
            'contact': 'Call us at +92-XXX-XXXXXXX or email us at admissions@aps.edu.pk for any inquiries.'
        },
        'upcoming_events': [
            {'name': 'Open House', 'date': '2024-11-10'},
            {'name': 'Annual Day', 'date': '2024-12-20'}
        ],
        'testimonials': [
            {'quote': 'Army Public School has provided my child with an excellent learning environment. The teachers are dedicated, and the facilities are top-notch.', 'author': 'Parent of a 5th Grader'},
            {'quote': 'I am grateful for the opportunities and support I received at Army Public School. It helped me achieve my academic goals and prepared me for the future.', 'author': 'APS Alumnus'}
        ]
    }
    return render(request, 'home/home.html',context)
'''

from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .forms import CustomUserForm, LoginForm, ResetPasswordForm,ForgetPasswordForm 
from app.account.utils.generate_Token import generate_verification_token
from app.account.utils.decodeVerficationToken import decode_verification_token
import jwt
from django.views import View



class SignupView(FormView):
    template_name = 'signup.html'
    form_class = CustomUserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# Login View
class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard')
    redirect_authenticated_user = True

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        form.add_error(None, "Invalid username or password")
        return self.form_invalid(form)

# Logout View
class LogoutView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    
# Dashboard View
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


# Send Email Verification
class SendEmailVerificationView(LoginRequiredMixin, TemplateView):
    template_name = 'verify_email.html'

    def post(self, request):
        user = request.user
        if not user.email_verified:
            token = generate_verification_token(user.pk)
            user.token_created_at = timezone.now()
            user.token_expiry_time = timezone.now() + timezone.timedelta(minutes=30)
            user.save()
            
            verification_link = f"{settings.FRONTEND_URL}/verify_email/?token={token}"
            send_mail(
                'Email Verification Request',
                f"Here is your email verification link: {verification_link}",
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            return redirect('email_sent')
        return redirect('profile')

# Verify Email View
class EmailVerifyView(TemplateView):
    template_name = 'verify_email_result.html'

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(pk=payload['user_id'])
            if user.is_token_valid():
                user.email_verified = True
                user.save()
                return render(request, self.template_name, {'message': "Email verified successfully"})
            return render(request, self.template_name, {'message': "Token has expired"})
        except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
            return render(request, self.template_name, {'message': "Invalid token"})

# Send Email Verification
# class SendEmailVerificationView(LoginRequiredMixin, TemplateView):
#     template_name = 'verify_email.html'

#     def post(self, request):
#         user = request.user
#         if not user.email_verified:
#             token = generate_verification_token(user.pk)
#             user.token_created_at = timezone.now()
#             user.token_expiry_time = timezone.now() + timezone.timedelta(minutes=30)
#             user.save()
            
#             verification_link = f"{settings.FRONTEND_URL}/verify_email/?token={token}"
#             send_mail(
#                 'Email Verification Request',
#                 f"Here is your email verification link: {verification_link}",
#                 settings.EMAIL_HOST_USER,
#                 [user.email]
#             )
#             return redirect('email_sent')
#         return redirect('profile')

# # Verify Email View
# class EmailVerifyView(TemplateView):
#     template_name = 'verify_email_result.html'

#     def get(self, request, *args, **kwargs):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#             user = CustomUser.objects.get(pk=payload['user_id'])
#             if user.is_token_valid():
#                 user.email_verified = True
#                 user.save()
#                 return render(request, self.template_name, {'message': "Email verified successfully"})
#             return render(request, self.template_name, {'message': "Token has expired"})
#         except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
#             return render(request, self.template_name, {'message': "Invalid token"})

# Forget Password View
# class ForgetPasswordView(FormView):
#     template_name = 'forget_password.html'
#     form_class = forms.Form
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         email = form.cleaned_data.get('email')
#         user = CustomUser.objects.filter(email=email).first()
#         if user:
#             token = generate_verification_token(user.pk)
#             reset_link = f"{settings.FRONTEND_URL}/reset_password/?token={token}"
#             send_mail(
#                 'Password Reset Request',
#                 f"Here is your password reset link: {reset_link}",
#                 settings.EMAIL_HOST_USER,
#                 [email],
#             )
#             return render(self.request, 'email_sent.html', {'message': 'Password reset link has been sent.'})
#         return render(self.request, 'forget_password.html', {'error': 'User with this email does not exist.'})
class ForgetPasswordView(FormView):
    template_name = 'forget_password.html'
    form_class = ForgetPasswordForm  # Use custom form
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        print("ForgetPasswordView: form_valid called") 
        print(f"Email submitted: {email}")  # Debugging statement

        # Fetch the user
        user = CustomUser.objects.filter(email=email).first()
        if user:
            print("User found with this email.")  # Debugging statement
            token = generate_verification_token(user.pk)
            reset_link = f"{settings.FRONTEND_URL}/reset_password/?token={token}"
            
            # Send email with reset link
            send_mail(
                'Password Reset Request',
                f"Here is your password reset link: {reset_link}",
                settings.EMAIL_HOST_USER,
                [email],
            )
            return render(self.request, 'email_sent.html', {'message': 'Password reset link has been sent.'})
        else:
            print("No user found with this email.")  # Debugging statement
            return render(self.request, 'forget_password.html', {'error': 'User with this email does not exist.'})
# Reset Password View
# class ResetPasswordView(FormView):
#     template_name = 'reset_password.html'
#     form_class = ResetPasswordForm
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         token = self.request.GET.get('token')
#         new_password = form.cleaned_data.get('password')
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#             user = CustomUser.objects.get(pk=payload['user_id'])
#             user.set_password(new_password)
#             user.save()
#             return redirect('login')
#         except (jwt.ExpiredSignatureError, jwt.DecodeError, CustomUser.DoesNotExist):
#             return render(self.request, 'reset_password.html', {'error': "Invalid or expired token"})
class ResetPasswordView(View):
    template_name = 'reset_password.html'

    def get(self, request):
        # Token verification
        token = request.GET.get('token')
        user_id = decode_verification_token(token)  # Extracts user ID from token

        if user_id:
            request.session['reset_user_id'] = user_id
            form = ResetPasswordForm()
            return render(request, self.template_name, {'form': form})
        else:
            return render(request, 'error.html', {'message': 'Invalid or expired token.'})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        user_id = request.session.get('reset_user_id')

        if not user_id:
            return render(request, 'error.html', {'message': 'Session expired. Try again.'})

        if form.is_valid():
            user = CustomUser.objects.get(pk=user_id)
            password = form.cleaned_data['password']
            user.password = make_password(password)
            user.save()
            
            # Clear session after reset
            del request.session['reset_user_id']
            return redirect(reverse_lazy('login'))
        else:
            return render(request, self.template_name, {'form': form})
'''
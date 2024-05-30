from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.urls import reverse
from student_module.models import Student
from teacher_module.models import Teacher
from staff_module.models import Staff
from utils.auth_services import get_user_by_type
from .forms import StudentLoginForm, StaffTeacherLoginForm, ForgotPasswordForm, ChangePasswordForm, EditProfileForm
from django.contrib import messages


# Create your views here.


class StudentLoginPage(View):
    def get(self, request):
        form = StudentLoginForm()
        context = {
            'form': form,
        }
        return render(request, 'account_module/student_login_page.html', context)

    def post(self, request):
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student_number = form.cleaned_data.get('student_number')
            user_password = form.cleaned_data.get('password')
            student = Student.objects.filter(student_number=student_number).first()
            if student is not None:
                is_password_valid = student.check_password(user_password)
                if is_password_valid:
                    login(request, student, backend='account_module.backends.StudentAuthenticationBackend')
                    return redirect(reverse('home_page'))
                else:
                    return redirect(reverse('student_login'))
            else:
                return redirect(reverse('student_login'))
        pass


class StaffTeacherLoginPage(View):
    def get(self, request):
        form = StaffTeacherLoginForm()
        context = {
            'form': form,
        }
        return render(request, 'account_module/staff_teacher_login_page.html', context)

    def post(self, request):
        form = StaffTeacherLoginForm(request.POST)
        if form.is_valid():
            personnel_code = form.cleaned_data.get('personnel_code')
            user_password = form.cleaned_data.get('password')
            staff_or_teacher = Staff.objects.filter(personnel_code=personnel_code).first()
            authenticate_backend = 'account_module.backends.StaffAuthenticationBackend'
            if staff_or_teacher is None:
                staff_or_teacher = Teacher.objects.filter(personnel_code=personnel_code).first()
                authenticate_backend = 'account_module.backends.TeacherAuthenticationBackend'
            if staff_or_teacher is not None:
                is_password_valid = staff_or_teacher.check_password(user_password)
                if is_password_valid:
                    login(request, staff_or_teacher, backend=authenticate_backend)
                    return redirect(reverse('home_page'))
                else:
                    return redirect(reverse('staff_teacher_login'))
            else:
                return redirect(reverse('staff_teacher_login'))
        pass


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index_page'))


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    def get(self, request: HttpRequest):
        form = ChangePasswordForm()
        context = {
            'form': form
        }
        return render(request, 'account_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user._meta.model_name == 'student':
                current_user: Student = Student.objects.filter(student_number=request.user.student_number).first()
            elif request.user._meta.model_name == 'staff':
                current_user: Staff = Staff.objects.filter(personnel_code=request.user.personnel_code).first()
            elif request.user._meta.model_name == 'teacher':
                current_user: Teacher = Teacher.objects.filter(personnel_code=request.user.personnel_code).first()
            else:
                return HttpResponseBadRequest()

            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('new_password'))
                current_user.save()
                logout(request)
                return redirect(reverse('index_page'))
            else:
                form.add_error('new_password', 'کلمه عبور وارد شده اشتباه می باشد')

        context = {
            'form': form
        }
        return render(request, 'account_module/change_password_page.html', context)


class UserInformationView(View):
    def get(self, request: HttpRequest):
        user = request.user
        user_base = get_user_by_type(request.user)
        context = {
            'user': user,
            'user_base': user_base,
        }
        return render(request, 'account_module/user_information_page.html', context)


class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = request.user.user

        data = {'email': current_user.email, 'phone_number': current_user.phone_number}
        edit_form = EditProfileForm(initial=data)
        context = {
            'user': request.user,
            'user_base': request.user.user,
            'form': edit_form,
        }
        return render(request, 'account_module/edit_profile_page.html', context)

    def post(self, request: HttpRequest):
        current_user = request.user.user

        data = {
            'phone_number': current_user.phone_number,
            'email': current_user.email,
        }

        edit_form = EditProfileForm(request.POST, initial=data)

        if edit_form.is_valid():
            current_user.phone_number = edit_form.cleaned_data.get('phone_number')
            current_user.email = edit_form.cleaned_data.get('email')
            current_user.save()
            messages.success(request, 'اطلاعات شما با موفقیت ویرایش شد.')
            return redirect('edit_profile')
        else:
            context = {
                'user': request.user,
                'user_base': request.user.user,
                'form': edit_form,
            }

            return render(request, 'account_module/edit_profile_page.html', context)

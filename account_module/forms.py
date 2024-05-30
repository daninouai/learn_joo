from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class StudentLoginForm(forms.Form):
    student_number = forms.CharField(
        label='شماره دانشجویی',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ],
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
        }),

    )


class StaffTeacherLoginForm(forms.Form):
    personnel_code = forms.CharField(
        label='کد پرسنلی',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ],
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
        }),

    )


class ForgotPasswordForm(forms.Form):
    email = forms.CharField(
        label='ایمیل',
        widget=forms.TextInput(attrs={
            'placeholder': 'ایمیل',
            'class': 'form-control',
            'type': "email",
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ],
    )

    student_number_personnel_code = forms.IntegerField(
        label='شماره دانشجویی یا کد پرسنلی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='کلمه عبور فعلی',
        widget=forms.PasswordInput({
            'class': 'form-control'
        })
    )
    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput({
            'class': 'form-control'
        })
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput({
            'class': 'form-control'
        })
    )

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if new_password == confirm_password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class EditProfileForm(forms.Form):
    phone_number = forms.CharField(
        label='شماره تلفن',
        widget=forms.TextInput({
            'class': 'form-control',
        })
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.TextInput({
            'class': 'form-control',
        })
    )

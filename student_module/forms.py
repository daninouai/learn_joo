from django import forms
from service_module.models import Requests
from django.core.validators import MinValueValidator, MaxValueValidator

from student_module.models import EvaluationByStudent, StudentGradeAppeal


class StudentRequestsForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['request_type', 'request_text']

        widgets = {
            'request_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'request_text': forms.Textarea(attrs={
                'class': 'form-control',
                'style': "height: 100px",
            }),
        }


class StudentPresentationForm(forms.ModelForm):
    class Meta:
        model = EvaluationByStudent
        fields = ['teaching_skills', 'punctuality', 'respectful_behavior']

        widgets = {
            'teaching_skills': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'punctuality': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'respectful_behavior': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teaching_skills'].validators.append(MinValueValidator(1))
        self.fields['teaching_skills'].validators.append(MaxValueValidator(10))
        self.fields['punctuality'].validators.append(MinValueValidator(1))
        self.fields['punctuality'].validators.append(MaxValueValidator(10))
        self.fields['respectful_behavior'].validators.append(MinValueValidator(1))
        self.fields['respectful_behavior'].validators.append(MaxValueValidator(10))


class StudentGradeAppealForm(forms.ModelForm):
    class Meta:
        model = StudentGradeAppeal
        fields = ['appel_text']

        widgets = {
            'appel_text': forms.Textarea(attrs={
                'class': 'form-control',
                'label': 'متن درخواست',
                'style': 'height: 200px;'
            }),
        }

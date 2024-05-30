from django import forms

from student_module.models import StudentGradeAppeal


class StudentGradeAppealResponseForm(forms.ModelForm):
    class Meta:
        model = StudentGradeAppeal
        fields = ['response_teacher']

        widgets = {
            'response_teacher': forms.Textarea(attrs={
                'class': 'form-control',
                'label': 'پاسخ به اعتراض',
                'style': 'height: 200px;'
            }),
        }

        labels = {
            'response_teacher': 'پاسخ به اعتراض'
        }

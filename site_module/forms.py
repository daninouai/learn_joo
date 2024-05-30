from django import forms

from site_module.models import ContactRequest, ContactMessages


class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest

        fields = ['subject']

        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class ContactMessagesForm(forms.ModelForm):
    class Meta:
        model = ContactMessages

        fields = ['message']

        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'style': "height: 250px",
            }),
        }

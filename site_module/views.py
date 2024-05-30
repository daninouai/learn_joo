from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View, DetailView
from .models import Faq, ContactRequest, IndexMessages, ContactMessages
from service_module.models import Semester
from django.http import HttpResponseBadRequest
from .forms import ContactRequestForm, ContactMessagesForm
from django.urls import reverse


# Create your views here.


def error_404(request, exception):
    return render(request, 'site_module/404.html', status=404)


def site_header_component(request: HttpRequest):
    user = request.user
    if 'semester_number' in request.session:
        current_semester = Semester.objects.get(semester_number=request.session['semester_number'])
        other_semesters = Semester.objects.all().exclude(semester_number=current_semester.semester_number)
    else:
        current_semester = Semester.objects.filter(is_main_semester=True).first()
        other_semesters = Semester.objects.filter(is_main_semester=False)

    context = {
        'current_semester': current_semester,
        'other_semesters': other_semesters,
        'user': user,
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request: HttpRequest):
    return render(request, 'shared/site_footer_component.html')


def site_sidebar_component(request: HttpRequest):
    return render(request, 'shared/site_sidebar_component.html')


class IndexPageView(TemplateView):
    template_name = 'site_module/index_page.html'


@method_decorator(login_required, name='dispatch')
class HomePageView(View):
    def get(self, request):
        user = request.user
        if user._meta.model_name == 'student':
            user_type = 'student'
        elif user._meta.model_name == 'staff':
            user_type = 'staff'
        elif user._meta.model_name == 'teacher':
            user_type = 'teacher'
        else:
            return HttpResponseBadRequest()
        messages = IndexMessages.objects.filter(for_group__contains=user_type).order_by('priority')
        context = {
            'messages': messages,
        }
        return render(request, 'site_module/home_page.html', context)


class CreateNewContact(View):
    def get(self, request):
        new_request = ContactRequestForm()
        message_content = ContactMessagesForm()

        context = {
            'new_request': new_request,
            'message_content': message_content,
        }
        return render(request, 'site_module/create_new_ticket_page.html', context)

    def post(self, request):
        new_request = ContactRequestForm(request.POST)
        message_content = ContactMessagesForm(request.POST)
        user = request.user

        if new_request.is_valid() and message_content.is_valid():
            subject = new_request.cleaned_data.get('subject')
            message = message_content.cleaned_data.get('message')

            if user._meta.model_name == 'student':
                create_request = ContactRequest.objects.create(from_student=user, subject=subject)
                create_message = ContactMessages.objects.create(from_student=user, message=message)
            elif user._meta.model_name == 'staff':
                create_request = ContactRequest.objects.create(from_staff=user, subject=subject)
                create_message = ContactMessages.objects.create(from_operator=user, message=message)
            elif user._meta.model_name == 'teacher':
                return HttpResponseBadRequest()
            else:
                return HttpResponseBadRequest()

            create_request.contact_message.add(create_message)
            create_request.save()

            return redirect('contact_messages_page')

        context = {
            'new_request': new_request,
            'message_content': message_content,
        }
        return render(request, 'site_module/create_new_ticket_page.html', context)


class ContactPageView(View):
    def get(self, request):
        all_contacts = ContactRequest.objects.filter()
        context = {
            'all_contacts': all_contacts,
        }
        return render(request, 'site_module/contact_page.html', context)


class ContactDetailView(View):
    def get(self, request: HttpRequest, pk):
        get_ticket = ContactRequest.objects.get(id=pk)
        message_content = ContactMessagesForm()

        context = {
            'get_ticket': get_ticket,
            'message_content': message_content,
        }
        return render(request, 'site_module/contact_detail_page.html', context)

    def post(self, request: HttpRequest, pk):
        get_ticket = ContactRequest.objects.get(id=pk)
        message_content = ContactMessagesForm(request.POST)
        user = request.user

        if message_content.is_valid():
            message = message_content.cleaned_data.get('message')

            if user._meta.model_name == 'student':
                create_message = ContactMessages.objects.create(from_student=user, message=message)
            elif user._meta.model_name == 'staff':
                create_message = ContactMessages.objects.create(from_operator=user, message=message)
            elif user._meta.model_name == 'teacher':
                return HttpResponseBadRequest()
            else:
                return HttpResponseBadRequest()

            get_ticket.contact_message.add(create_message)
            get_ticket.save()

            return redirect(reverse('contact_messages_detail', args=[get_ticket.pk]))

        context = {
            'get_ticket': get_ticket,
            'message_content': message_content,
        }
        return render(request, 'site_module/contact_detail_page.html', context)


class UsersFaqPage(View):
    def get(self, request):
        user = request.user
        if user._meta.model_name == 'student':
            user_type = 'student'
        elif user._meta.model_name == 'staff':
            user_type = 'staff'
        elif user._meta.model_name == 'teacher':
            user_type = 'teacher'
        else:
            return HttpResponseBadRequest()
        fags = Faq.objects.filter(for_group__contains=user_type)
        context = {
            'fags': fags,
        }
        return render(request, 'site_module/fags_page.html', context)

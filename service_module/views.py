import json
import uuid
import requests
from django.conf import settings
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseBadRequest, HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from service_module.models import Presentation, Semester, Payment, Bill
from student_module.models import Marks
from utils.student_services import check_time_conflict, check_presentation_conflict, calculate_variable_tuition_bill


# Create your views here.


class SearchLessonsPageView(View):
    def get(self, request):
        context = {
        }
        return render(request, 'service_module/search_lessons_page.html', context)


def search_lessons_queries(request: HttpRequest):
    lesson_name = request.GET.get('lessonName')
    lesson_code = request.GET.get('lessonCode')

    if 'semester_number' in request.session:
        current_semester = Semester.objects.get(semester_number=request.session['semester_number'])
    else:
        current_semester = Semester.objects.filter(is_main_semester=True).first()

    if lesson_name and not lesson_code:
        lessons = Presentation.objects.filter(lesson__lesson_name__icontains=lesson_name, for_semester=current_semester)
    elif lesson_code and not lesson_name:
        lessons = Presentation.objects.filter(lesson__lesson_code=lesson_code, for_semester=current_semester)
    elif lesson_name and lesson_code:
        lessons = Presentation.objects.filter(Q(lesson__lesson_name__icontains=lesson_name) | Q(lesson__lesson_code=lesson_code), for_semester=current_semester)
    else:
        return HttpResponseBadRequest()

    context = {
        'lessons': lessons,
    }
    return render(request, 'service_module/result_lessons_page.html', context)


def change_semester(request: HttpRequest):
    selected_semester = request.POST.get('semester_number')
    request.session['semester_number'] = selected_semester
    return HttpResponse()


def change_semester_to_default(request: HttpRequest):
    request.session['semester_number'] = Semester.objects.filter(is_main_semester=True).first().semester_number
    return HttpResponse()

class SelectUnitPage(View):
    def get(self, request: HttpRequest):
        # TODO: اگر کاربر مجوز انتخاب واحد گرفته بود بتونه ببینه
        current_semester = Semester.objects.filter(is_main_semester=True).first()
        user = request.user
        today = timezone.now()
        if current_semester.select_unit_permission:
            if current_semester.start_select_unit_time and current_semester.end_select_unit_time:
                if current_semester.start_select_unit_time <= today <= current_semester.end_select_unit_time:
                    permission_select_unit = user.requests_set.filter(request_type='permission_select_unit', for_semester=current_semester, status='confirmed').first()
                    if permission_select_unit:
                        current_presentation = Presentation.objects.filter(for_semester=current_semester, student=request.user)
                        token = uuid.uuid4()
                        request.session['search_token'] = str(token)

                        context = {
                            'current_presentation': current_presentation,
                            'search_token': str(token)
                        }
                        return render(request, 'service_module/select_unit_page.html', context)
                    else:
                        return render(request, 'service_module/forbidden_select_unit_page.html')
                else:
                    return render(request, 'service_module/forbidden_select_unit_page.html')
            else:
                return render(request, 'service_module/forbidden_select_unit_page.html')
        else:
            return render(request, 'service_module/forbidden_select_unit_page.html')


def select_unit_search_lessons_queries(request: HttpRequest):
    lesson_name = request.GET.get('lessonName')
    lesson_code = request.GET.get('lessonCode')

    if 'semester_number' in request.session:
        current_semester = Semester.objects.get(semester_number=request.session['semester_number'])
    else:
        current_semester = Semester.objects.filter(is_main_semester=True).first()

    if lesson_name and not lesson_code:
        lessons = Presentation.objects.filter(lesson__lesson_name__icontains=lesson_name, for_semester=current_semester)
    elif lesson_code and not lesson_name:
        lessons = Presentation.objects.filter(lesson__lesson_code=lesson_code, for_semester=current_semester)
    elif lesson_name and lesson_code:
        lessons = Presentation.objects.filter(Q(lesson__lesson_name__icontains=lesson_name) | Q(lesson__lesson_code=lesson_code), for_semester=current_semester)
    else:
        return HttpResponseBadRequest()

    context = {
        'lessons': lessons,
        'search_token': request.session['search_token'],
    }
    return render(request, 'service_module/result_select_lessons_page.html', context)


def select_unit_action(request):
    if request.method == 'POST':
        get_token = request.POST.get('search_token')
        selected_lesson_id = request.POST.get('selected_lesson_id')
        current_semester = Semester.objects.filter(is_main_semester=True).first()

        if request.session.get('search_token') == get_token:
            student = request.user
            new_class = Presentation.objects.get(pk=selected_lesson_id, for_semester=current_semester)
            new_class_time = new_class.class_formation_time
            existing_classes = student.presentation_set.all()

            if not check_presentation_conflict(new_class, existing_classes):
                if not check_time_conflict(new_class_time, existing_classes):
                    get_presentation = Presentation.objects.filter(pk=selected_lesson_id, for_semester=current_semester).first()
                    user_all_presentations_passed = Marks.objects.filter(for_student=request.user, mark__gte=10)
                    lesson_all_presentations = get_presentation.lesson.prerequisite_lesson.all()
                    if all(item in user_all_presentations_passed for item in lesson_all_presentations):
                        get_presentation.student.add(student)
                    else:
                        missing_prerequisites = [item.lesson_name for item in lesson_all_presentations if item not in user_all_presentations_passed]
                        missing_prerequisites_names = ', '.join(missing_prerequisites)
                        messages.error(request, f'پیش نیاز لازم است: {missing_prerequisites_names}')
                    # get_presentation.student.add(student)
                    # del request.session['search_token']
                else:
                    messages.error(request, 'تداخل زمانی با کلاس‌ های قبلی وجود دارد!')
            else:
                messages.error(request, 'این واحد درسی از قبل انتخاب شده است!')
            del request.session['search_token']


def remove_unit_action(request: HttpRequest):
    if request.method == 'POST':
        selected_lesson_id = request.POST.get('selected_lesson_id')
        current_semester = Semester.objects.filter(is_main_semester=True).first()
        student = request.user
        get_presentation = Presentation.objects.filter(pk=selected_lesson_id, for_semester=current_semester).first()
        get_presentation.student.remove(student)
        return redirect(reverse('select_unit'))


if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

amount = 30000  # Rial / Required
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify-payment/'


def send_request(request: HttpRequest):
    bill_id = request.POST.get('bill_id')
    user = request.user

    current_semester = Semester.objects.filter(is_main_semester=True).first()

    if bill_id:
        get_bill = Bill.objects.get(bill_id=bill_id)
        amount = get_bill.amount
        Payment.objects.create(for_student=user, for_semester=current_semester, amount=amount, status='pending', for_bill=get_bill)
    else:
        amount = request.POST.get('paymentAmount')
        Payment.objects.create(for_student=user, for_semester=current_semester, amount=amount, status='pending')

    data = {
        "MerchantID": settings.MERCHANT,
        # "Amount": amount * 10, # Rial
        "Amount": amount,  # Toman
        "Description": f'پرداخت وجه به مبلغ {amount} تومان ',
        "Email": user.user.email,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)

    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response_data = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

        if response_data.status_code == 200:
            response_data = response_data.json()
            if response_data['Status'] == 100:
                return redirect(ZP_API_STARTPAY + str(response_data['Authority']))
            else:
                return {'status': False, 'code': str(response_data['Status'])}
        return response_data

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}


def verify(request: HttpRequest):
    authority = request.GET['Authority']

    user = request.user

    get_payment = Payment.objects.filter(for_student=user, status='pending').first()

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": str(get_payment.amount),
        "Authority": authority,
    }

    data = json.dumps(data)

    headers = {'content-type': 'application/json', 'content-length': str(len(data))}

    response_data = requests.post(ZP_API_VERIFY, data=data, headers=headers)

    if response_data.status_code == 200:
        response = response_data.json()
        if response['Status'] == 100:
            get_payment.status = 'confirmed'
            user.amount_paid += int(get_payment.amount)
            if get_payment.for_bill:
                get_payment.for_bill.is_paid = True
                get_payment.for_bill.save()
            get_payment.save()
            user.save()
            print('تراکنش انجام و تایید شد')
            messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
            return redirect('student_manage_payments')
        elif response['Status'] == 101:
            get_payment.status = 'rejected'
            get_payment.save()
            print('این تراکنش قبلا انجام شده است')
        else:
            get_payment.status = 'rejected'
            get_payment.save()
            print('پرداخت انجام نشد')

    return response_data


def task_issuance_variable_tuition_billing(request):
    calculate_variable_tuition_bill(request.user)

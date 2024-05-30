from django import template
from utils.student_services import unit_count_convertor

register = template.Library()


@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    return '{:,}'.format(value)


@register.filter(name='toman_suffix')
def three_digits_currency(value):
    return f'{value} تومان '


@register.filter(name='get_model_name')
def get_model_name(obj):
    return obj._meta.model_name


@register.filter(name='person_suffix')
def person_suffix(obj):
    return f'{obj} نفر '


@register.filter(name='get_user_role')
def get_user_role(obj):
    if obj._meta.model_name == 'student':
        return 'دانشجو'
    elif obj._meta.model_name == 'staff':
        return 'کارمند'
    elif obj._meta.model_name == 'teacher':
        return 'استاد'
    else:
        return 'مشخص نشده'


@register.filter(name='get_mark_with_coefficient')
def get_mark_with_coefficient(obj, lesson):
    all_unit = unit_count_convertor(lesson.theoretical_unit) + unit_count_convertor(lesson.practical_units)
    return obj * all_unit


@register.filter(name='summation')
def summation(obj, operand):
    return obj + operand


@register.filter(name='balance_status')
def balance_status(pain, unpaid):
    if pain == unpaid:
        return 'تسویه'
    elif unpaid > pain:
        return 'بدهکار'
    else:
        return 'بستانکار'


@register.filter(name='balance')
def balance(pain, unpaid):
    return unpaid - pain


@register.filter(name='bootstrap_class')
def bootstrap_class(message_tags):
    return 'danger' if 'error' in message_tags else message_tags

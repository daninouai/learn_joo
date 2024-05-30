from service_module.models import *
import re
from service_module.models import VariableTuition


def unit_count_convertor(unit):
    if unit == 'half_units':
        return 0.5
    elif unit == 'single_units':
        return 1
    elif unit == 'two_units':
        return 2
    elif unit == 'three_units':
        return 3
    elif unit == 'four_units':
        return 4
    elif unit == 'five_units':
        return 5
    else:
        return 0


def calculate_gpa(marks):
    obtained_units = 0
    passed_units = 0
    rejected_units = 0
    all_marks = 0
    for mark in marks:
        all_units = (unit_count_convertor(mark.presentation.lesson.practical_units) + unit_count_convertor(mark.presentation.lesson.theoretical_unit))
        obtained_units += all_units
        all_marks += mark.mark * all_units
        if mark.mark > 10:
            passed_units += all_units
        if mark.mark < 10:
            rejected_units += all_units

    if obtained_units != 0:
        avg_marks = all_marks / obtained_units
    else:
        avg_marks = 0

    return obtained_units, passed_units, rejected_units, avg_marks


def calculate_fixed_tuition(user):
    fixed_tuition = FixedTuition.objects.get(entrance_semester=user.admission_semester, section=user.major.section)
    if fixed_tuition:
        return fixed_tuition.cost
    return 0


def parse_custom_time_format(time_str):
    print(time_str)
    # format 1:
    match = re.match(r'(\w+)_(\d{1,2})_(\d{1,2})', time_str)
    if match:
        day, start_hour, end_hour = match.groups()
        print(day)
        print(start_hour)
        print(end_hour)
        return day, int(start_hour), int(end_hour), 0, 0

    # format 2:
    match = re.match(r'(\w+)_(\d{1,2})_(\d{1,2})d(\d{1,2})_and_(\d{1,2})_(\d{1,2})d(\d{1,2})', time_str)
    if match:
        day, start_hour, start_minute, end_hour, end_minute = match.groups()
        return day, int(start_hour), int(end_hour), int(start_minute), int(end_minute)

    raise ValueError("Invalid custom time format")


def check_time_conflict(new_class_time, existing_classes):
    new_day, new_start_hour, new_end_hour, new_start_minute, new_end_minute = parse_custom_time_format(new_class_time)

    for existing_class in existing_classes:
        existing_day, existing_start_hour, existing_end_hour, existing_start_minute, existing_end_minute = parse_custom_time_format(existing_class.class_formation_time)

        if existing_day == new_day:
            # check on format 1:
            if (existing_start_hour <= new_start_hour < existing_end_hour) or (existing_start_hour <= new_end_hour < existing_end_hour):
                print('تداخل')
                return True
            # check on format 2:
            if new_start_minute and new_end_minute and existing_start_minute and existing_end_minute:
                if (existing_start_hour == new_start_hour and existing_start_minute <= new_start_minute < existing_end_minute) or (existing_start_hour == new_end_hour and existing_start_minute <= new_end_minute < existing_end_minute):
                    print('تداخل')
                    return True

    print('عدم تداخل')
    return False


def check_presentation_conflict(new_class, existing_classes):
    for existing_class in existing_classes:
        if new_class.lesson == existing_class.lesson and new_class.for_semester == existing_class.for_semester:
            print('در این ترم درسی با همین عنوان وجود دارد')
            return True
    print('درسی با همین عنوان وجود ندارد و میتوانید بردارید!')
    return False


def calculate_variable_tuition_bill(student):
    lessons = student.presentation_set.all()
    current_semester = Semester.objects.filter(is_main_semester=True).first()
    get_variable_tuition = VariableTuition.objects.get(for_semester__is_main_semester=True, educational_group=student.major.educational_group, section=student.major.section)
    total_tuition = 0
    for lesson in lessons:
        practical_units = unit_count_convertor(lesson.lesson.practical_units) * get_variable_tuition.one_practical_unit
        theoretical_unit = unit_count_convertor(lesson.lesson.theoretical_unit) * get_variable_tuition.one_theoretical_unit
        total_tuition += practical_units + theoretical_unit
    if total_tuition > 0:
        student.amount_payable += total_tuition
        student.save()
        Bill.objects.create(for_semester=current_semester, for_student=student, type='variable_tuition', amount=total_tuition)

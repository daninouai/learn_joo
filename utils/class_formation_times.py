from django.db import models


class ClassFormationTime(models.TextChoices):
    MON_8_10 = 'mon_8_10', 'دوشنبه از 8 تا 10'
    MON_10_12 = 'mon_10_12', 'دوشنبه از 10 تا 12'
    MON_13_15 = 'mon_13_15', 'دوشنبه از 13 تا 15'
    MON_15_17 = 'mon_15_17', 'دوشنبه از 15 تا 17'
    MON_8_11 = 'mon_8_11', 'دوشنبه از 8 تا 11'
    MON_11_12D30_AND_13_14D30 = 'mon_11_12d30_and_13_14d30', 'دوشنبه از 11 تا 12:30 و 13 تا 14:30'
    MON_15_18 = 'mon_15_18', 'دوشنبه از 15 تا 18'
    MON_18_21 = 'mon_18_21', 'دوشنبه از 18 تا 21'

    TUE_8_10 = 'tue_8_10', 'سه‌شنبه از 8 تا 10'
    TUE_10_12 = 'tue_10_12', 'سه‌شنبه از 10 تا 12'
    TUE_13_15 = 'tue_13_15', 'سه‌شنبه از 13 تا 15'
    TUE_15_17 = 'tue_15_17', 'سه‌شنبه از 15 تا 17'
    TUE_8_11 = 'tue_8_11', 'سه‌شنبه از 8 تا 11'
    TUE_11_12D30_AND_13_14D30 = 'tue_11_12d30_and_13_14d30', 'سه‌شنبه از 11 تا 12:30 و 13 تا 14:30'
    TUE_15_18 = 'tue_15_18', 'سه‌شنبه از 15 تا 18'
    TUE_18_21 = 'tue_18_21', 'سه‌شنبه از 18 تا 21'

    WED_8_10 = 'wed_8_10', 'چهارشنبه از 8 تا 10'
    WED_10_12 = 'wed_10_12', 'چهارشنبه از 10 تا 12'
    WED_13_15 = 'wed_13_15', 'چهارشنبه از 13 تا 15'
    WED_15_17 = 'wed_15_17', 'چهارشنبه از 15 تا 17'
    WED_8_11 = 'wed_8_11', 'چهارشنبه از 8 تا 11'
    WED_11_12D30_AND_13_14D30 = 'wed_11_12d30_and_13_14d30', 'چهارشنبه از 11 تا 12:30 و 13 تا 14:30'
    WED_15_18 = 'wed_15_18', 'چهارشنبه از 15 تا 18'
    WED_18_21 = 'wed_18_21', 'چهارشنبه از 18 تا 21'

    THU_8_10 = 'thu_8_10', 'پنج‌شنبه از 8 تا 10'
    THU_10_12 = 'thu_10_12', 'پنج‌شنبه از 10 تا 12'
    THU_13_15 = 'thu_13_15', 'پنج‌شنبه از 13 تا 15'
    THU_15_17 = 'thu_15_17', 'پنج‌شنبه از 15 تا 17'
    THU_8_11 = 'thu_8_11', 'پنج‌شنبه از 8 تا 11'
    THU_11_12D30_AND_13_14D30 = 'thu_11_12d30_and_13_14d30', 'پنج‌شنبه از 11 تا 12:30 و 13 تا 14:30'
    THU_15_18 = 'thu_15_18', 'پنج‌شنبه از 15 تا 18'
    THU_18_21 = 'thu_18_21', 'پنج‌شنبه از 18 تا 21'

    FRI_8_10 = 'fri_8_10', 'جمعه از 8 تا 10'
    FRI_10_12 = 'fri_10_12', 'جمعه از 10 تا 12'
    FRI_13_15 = 'fri_13_15', 'جمعه از 13 تا 15'
    FRI_15_17 = 'fri_15_17', 'جمعه از 15 تا 17'
    FRI_8_11 = 'fri_8_11', 'جمعه از 8 تا 11'
    FRI_11_12D30_AND_13_14D30 = 'fri_11_12d30_and_13_14d30', 'جمعه از 11 تا 12:30 و 13 تا 14:30'
    FRI_15_18 = 'fri_15_18', 'جمعه از 15 تا 18'
    FRI_18_21 = 'fri_18_21', 'جمعه از 18 تا 21'

<img src="https://raw.githubusercontent.com/daninouai/learn_joo/master/static/assets/img/apple-touch-icon.png" alt="logo" align="left" height="100"/>

# Learn Joo <br> ![version badge](https://img.shields.io/badge/latest--release-v1.0-blue)

سلام XD
<br>
این سیستم برای امور دانشگاهی دانشگاه های آزاد طراحی شده تقریبا مشابه سیستم فعلی "آموزشیار" که همه ما با اون سروکار داریم!
<br>
در اصل این مربوط به یکی از درس های دانشگاه "تحلیل و طراحی سیستم" هست. که به عنوان پروژه ای برای درس انجام شده...
<br>
همینطور فایل های مربوط به فاز تحلیل و طراحی اون توی همین ریپوزیتوری موجود هست فایلی با نام systemDesign.pdf 
<br>
و در نهایت از زحمات استاد عزیز خانم دکتر شیشه چی تشکر میکنم 
<br>



اینجا یه راهنمایی کوچیک هست که بتونی این برنامه رو اجرا کنی (:
# راه اندازی
دریافت سورس فایل برنامه

```python
git clone https://github.com/daninouai/learn_joo.git
```
ورود به فولدر اصلی برنامه
```python
cd learn_joo
```
ساخت محیط ویرچوآل برای اجرا برنامه
```python
python -m venv venv 
```
فعال کردن محیط ویرچوآل
```python
source venv/bin/activate
```
نصب پکیج های مورد نیاز
```python
pip install -r requirements.txt
```
در مسیر ریشه برنامه اجرا دستورات به ترتیب
```python
python manage.py makemigrations
python manage.py migrate
```
و اجرای برنامه 
```python
python manage.py runserver
```
**البته که لازمه پایتون رو نصب داشته باشی**

# Frameworks And Languages
* [Django](https://www.djangoproject.com/)
* HTML, CSS, JS

# Authors
* [daninouai](https://github.com/daninouai)

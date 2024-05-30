from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPageView.as_view(), name='index_page'),
    path('home', views.HomePageView.as_view(), name='home_page'),
    path('faqs', views.UsersFaqPage.as_view(), name='faq_page'),
    path('contact-messages', views.ContactPageView.as_view(), name='contact_messages_page'),
    path('new-ticket', views.CreateNewContact.as_view(), name='new_ticket_page'),
    path('contact-messages-detail/<pk>', views.ContactDetailView.as_view(), name='contact_messages_detail'),
]

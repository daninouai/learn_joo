from django.shortcuts import render
from django.views.generic import ListView, View

from service_module.models import Presentation


# Create your views here.


class PresentationListView(ListView):
    model = Presentation
    template_name = ''
    paginate_by = 12


class AddPresentationView(View):
    def get(self, request):
        context = {}
        return render(request, '', context)

    def post(self, request):
        context = {}
        return render(request, '', context)


class EditPresentationView(View):
    def get(self, request):
        context = {}
        return render(request, '', context)

    def post(self, request):
        context = {}
        return render(request, '', context)


def delete_presentation(request, id):
    pass

import os

from django.http import HttpResponse
from django.template import loader

from app import Client
from app import db_session
from lab2.settings import BASE_DIR


def index(request):
    if request.method == 'GET':
        template = loader.get_template('list.html')
        context = {'title': 'CHECK IN'}
        return HttpResponse(template.render(context, request))

from django.http import HttpResponse

from app import db_session, client
from app import hotel



def index(request):
    return HttpResponse('Check database.')


def clients_list(request):
    db_session.get_list(client)
    return None


def clients_post(request):
    db_session.create(client, {'first_name': 'Yura', 'last_name': 'Shatunov', 'phone_number': '+367393548813'})
    return None


def hotels_post(request):
    db_session.create(hotel, {'country': 'Ukraine',
                            'city': 'Kyiv',
                            'street': 'Khreshchatyk',
                            'building': 1, })
    return None


def clients_get(request, id):
    db_session.get(client, id)
    return None


def clients_update(request, id):
    db_session.update(client, id, {'phone_number': '+320729764890'})
    return None


def hotels_update(request, id):
    db_session.update(hotel, id, {'building': 3})
    return None


def hotels_get(request, id):
    db_session.get(hotel, id)
    return None


def clients_delete(request, id):
    db_session.delete(client, id)
    return None
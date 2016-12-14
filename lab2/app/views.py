from django.shortcuts import render, redirect

from app import CheckIn
from app import Client
from app import Hotel
from app import Room
from app import db_session
from app.forms import SearchForm, CheckInInsert, CheckInUpdate


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            return render(request, 'search.html', {'search_list': CheckIn.search(db_session, **form.cleaned_data)})
    else:
        form = SearchForm()
    return render(request, 'check_in_list.html', {'form': form,
                                                  'check_in': CheckIn.get_all(db_session)})


def client_list(request):
    return render(request, 'client_list.html', {'client': Client.get_all(db_session)})


def room_list(request):
    return render(request, 'room_list.html', {'room': Room.get_all(db_session)})


def hotel_list(request):
    return render(request, 'hotel_list.html', {'hotel': Hotel.get_all(db_session)})


def client_xml_fill(request):
    db_session.fill_from_xml(Client, 'client.xml')
    return redirect('client_list')


def room_xml_fill(request):
    db_session.fill_from_xml(Room, 'room.xml')
    return redirect('room_list')


def hotel_xml_fill(request):
    db_session.fill_from_xml(Hotel, 'hotel.xml')
    return redirect('hotel_list')


def new(request):
    if request.method == 'POST':
        form = CheckInInsert(request.POST)
        if form.is_valid():
            modify_check_in(CheckIn(db_session), form.cleaned_data)
            return redirect('index')
    else:

        form = CheckInInsert()
    return render(request, 'new_check_in.html', {'form': form})


def detail(request, id):
    check_in = CheckIn(db_session, id)
    if request.method == 'POST':
        form = CheckInUpdate(request.POST)
        if form.is_valid():
            modify_check_in(check_in, form.cleaned_data)
            return redirect('index')
    else:

        form = CheckInUpdate(check_in=check_in)
    return render(request, 'update_check_in.html', {'form': form, 'id': id})


def delete(request, id):
    CheckIn(db_session, id).delete()
    return redirect('index')


def modify_check_in(check_in, data):
    for field, value in data.items():
        if value:
            exec('check_in.%s = value' % field)
    check_in.total_price = check_in.days * Room(db_session, check_in.idroom).price
    check_in.save()

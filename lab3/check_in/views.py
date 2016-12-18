from django.shortcuts import render, redirect
import xml.etree.ElementTree as ET
from check_in.forms import SearchForm, CheckInInsert, CheckInUpdate
from check_in.models import CheckIn, Room, Client, Hotel


def index(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            queries = {}
            if data['min_price'] and data['max_price']:
                queries['room__price__range'] = (data['min_price'], data['max_price'])
            if data['min_people'] and data['max_people']:
                queries['room__number_of_people__range'] = (data['min_people'], data['max_people'])
            if data['is_lux']:
                queries['room__is_lux'] = data['is_lux']
            boolean = ''
            if data['include']:
                boolean += '+{} '.format(data['include'])
            if data['exclude']:
                boolean += '-{}'.format(data['exclude'])
            if boolean:
                queries['room__hotel__description__search'] = boolean
            return render(request, 'search.html', {'search_list': CheckIn.objects.filter(**queries)})
    else:
        form = SearchForm()
    return render(request, 'check_in_list.html', {'form': form,
                                                  'check_in': CheckIn.objects.all()})


def new(request):
    if request.method == 'POST':
        form = CheckInInsert(request.POST)
        if form.is_valid():
            check_in = CheckIn(**form.cleaned_data)
            check_in.total_price = check_in.days * check_in.room.price
            check_in.save()
            return redirect('index')
    else:

        form = CheckInInsert()
    return render(request, 'new_check_in.html', {'form': form})


def detail(request, id):
    check_in = CheckIn.objects.get(pk=id)
    if request.method == 'POST':
        form = CheckInUpdate(request.POST, check_in=check_in)
        if form.is_valid():
            for attr, value in form.cleaned_data.items():
                setattr(check_in, attr, value)
            check_in.total_price = check_in.days * check_in.room.price
            check_in.save()
            return redirect('index')
    else:

        form = CheckInUpdate(check_in=check_in)
    return render(request, 'update_check_in.html', {'form': form, 'id': id})


def delete(request, id):
    CheckIn.objects.get(pk=id).delete()
    return redirect('index')


def client_list(request):
    return render(request, 'client_list.html', {'client': Client.objects.all()})


def room_list(request):
    return render(request, 'room_list.html', {'room': Room.objects.all()})


def hotel_list(request):
    return render(request, 'hotel_list.html', {'hotel': Hotel.objects.all()})


def fill_from_xml(model, xml_file):
    for row in model.objects.all():
        row.delete()
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for child in root:
        new = model(**{column.tag: column.text for column in child})
        new.save()


def client_xml_fill(request):
    fill_from_xml(Client, 'client.xml')
    return redirect('client_list')


def room_xml_fill(request):
    fill_from_xml(Room, 'room.xml')
    return redirect('room_list')


def hotel_xml_fill(request):
    fill_from_xml(Hotel, 'hotel.xml')
    return redirect('hotel_list')
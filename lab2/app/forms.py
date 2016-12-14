from django.forms import forms, NullBooleanField, IntegerField, CharField, FloatField, DateField, ChoiceField
from flask import request

from app import Client
from app import Room
from app import db_session


def get_room_choice_list():
    return list((room.id, room.id) for room in Room.get_all(db_session))


def get_client_choice_list():
    return list((client.id, client.id) for client in Client.get_all(db_session))


class CheckInInsert(forms.Form):
    date = DateField(label="Date")
    days = IntegerField(label="Number of days")
    idclient = ChoiceField(label="Client ID", required=False,
                           choices=get_client_choice_list())
    idroom = ChoiceField(label="Room ID", required=False,
                         choices=get_room_choice_list())


class CheckInUpdate(forms.Form):
    date = DateField(label="Date", required=False)
    days = IntegerField(label="Number of days", required=False)
    idclient = ChoiceField(
        label="Client ID", required=False,
        choices=get_client_choice_list()
    )
    idroom = ChoiceField(
        label="Room ID", required=False,
        choices=get_room_choice_list()
    )

    def __init__(self, *args, **kwargs):
        self.check_in = kwargs.pop('check_in')
        super(CheckInUpdate, self).__init__(*args, **kwargs)
        self.fields['date'].initial = self.check_in.date
        self.fields['days'].initial = self.check_in.days
        self.fields['idclient'].initial = self.check_in.idclient
        self.fields['idroom'].initial = self.check_in.idroom


class SearchForm(forms.Form):
    is_lux = NullBooleanField(label="Lux room", required=False)
    min_price = FloatField(label="Minimum price per room", required=False)
    max_price = FloatField(label="Maximum price per room", required=False)
    min_people = IntegerField(label="Minimum number of people in the room", required=False)
    max_people = IntegerField(label="Maximum number of people in the room", required=False)
    include = CharField(label="Word to include in hotel description", required=False)
    exclude = CharField(label="Word to exclude from hotel description", required=False)

    def clean_include(self):
        include = self.cleaned_data.get('include')
        if include:
            if len(include.rstrip().split(' ')) > 1:
                raise forms.ValidationError("Must contain only one word.")
        return include

    def clean_exclude(self):
        exclude = self.cleaned_data.get('exclude')
        if exclude:
            if len(exclude.rstrip().split(' ')) > 1:
                raise forms.ValidationError("Must contain only one word.")
        return exclude

    def clean(self):
        data = super(SearchForm, self).clean()
        min_price = data.get('min_price')
        max_price = data.get('max_price')
        if min_price and max_price:
            if max_price < min_price:
                raise forms.ValidationError("Minimum price cannot be  bigger than maximum price")
        min_people = data.get('min_people')
        max_people = data.get('max_people')
        if min_people and max_people:
            if max_people < min_people:
                raise forms.ValidationError("Minimum number of people cannot be  bigger than maximum")

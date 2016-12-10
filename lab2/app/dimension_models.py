from app.base_model import BaseModel
import xml.etree.ElementTree as ET


class DimensionModel(BaseModel):
    def fill_from_xml(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for child in root:
            row = {column.tag: column.text for column in child}
            self.session.create(self, row)


class Client(DimensionModel):
    table_name = 'client'
    columns = {
        'id': 'INT',
        'first_name': 'VARCHAR(45)',
        'last_name': 'VARCHAR(45)',
        'phone_number': 'VARCHAR(13)'
    }


class Hotel(DimensionModel):
    table_name = 'hotel'
    columns = {
        'id': 'INT',
        'country': 'VARCHAR(45)',
        'city': 'VARCHAR(45)',
        'street': 'VARCHAR(45)',
        'building': 'INT',
        'description': 'MEDIUMTEXT',
    }
    null = ['description']


class Room(DimensionModel):
    table_name = 'room'
    columns = {
        'id': 'INT',
        'number_of_people': 'INT',
        'price': 'DOUBLE',
        'is_lux': 'BOOLEAN',
        'idhotel': 'INT'
    }

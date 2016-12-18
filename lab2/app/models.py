from app.base_model import BaseModel


class CheckIn(BaseModel):
    table_name = 'check_in'
    columns = {
        'id': 'INT',
        'date': 'DATE',
        'days': 'INT',
        'total_price': 'DOUBLE',
        'client_id': 'INT',
        'room_id': 'INT'
    }

    @classmethod
    def search(
            cls,
            session,
            is_lux=None,
            min_price=None,
            max_price=None,
            min_people=None,
            max_people=None,
            include=None,
            exclude=None
    ):
        conditions = []
        if is_lux is not None:
            conditions.append('{}.is_lux IS {}'.format(Room.table_name, is_lux))
        if min_price and max_price:
            conditions.append('{}.price BETWEEN {} AND {}'.format(Room.table_name, min_price, max_price))
        if min_people and max_people:
            conditions.append('{}.number_of_people BETWEEN {} AND {}'.format(Room.table_name, min_people,
                                                                             max_people))
        if include or exclude:
            boolean = "MATCH ({}.description) AGAINST ('".format(Hotel.table_name)
            if include:
                boolean += "+{} ".format(include)
            if exclude:
                boolean += "-{}".format(exclude)
            boolean += "' IN BOOLEAN MODE)"
            conditions.append(boolean)
        condition = ''
        if conditions:
            condition = "WHERE {}.{} = {}.{}".format(cls.table_name, Room.ref[cls], Room.table_name, cls.primary_key)
            for cond in conditions:
                condition += " AND {}".format(cond)
        session.general_select([cls, Room, Hotel], ["{}.{}".format(cls.table_name, cls.primary_key)], condition)
        return [cls(session, row[cls.primary_key]) for row in session.cur.fetchall()]


class Client(BaseModel):
    table_name = 'client'
    columns = {
        'id': 'INT',
        'first_name': 'VARCHAR(45)',
        'last_name': 'VARCHAR(45)',
        'phone_number': 'VARCHAR(13)'
    }
    ref = {CheckIn: 'client_id'}


class Room(BaseModel):
    table_name = 'room'
    columns = {
        'id': 'INT',
        'number_of_people': 'INT',
        'price': 'DOUBLE',
        'is_lux': 'BOOLEAN',
        'hotel_id': 'INT'
    }
    ref = {CheckIn: 'room_id'}

    @property
    def is_lux(self):
        return bool(self.__getattr__('is_lux'))


class Hotel(BaseModel):
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
    ref = {Room: 'hotel_id'}

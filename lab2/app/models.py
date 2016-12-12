from app.base_model import BaseModel


class CheckIn(BaseModel):
    table_name = 'check_in'
    columns = {
        'id': 'INT',
        'date': 'DATE',
        'days': 'INT',
        'total_price': 'DOUBLE',
        'idclient': 'INT',
        'idroom': 'INT'
    }

    @classmethod
    def search(cls, session, is_lux=None, room_price=None, number_of_people=None, hotel_description=None):
        """

        :param is_lux: bool
        :param room_price: 2-element tuple with min and max room price
        :param number_of_people: 2-element tuple with min and max number of people in the room
        :param hotel_description:  dict with '+' and '-' as keys and words to include and exclude as values
        """
        conditions = []
        if is_lux is not None:
            conditions.append('{}.is_lux IS {}'.format(Room.table_name, is_lux))
        if room_price:
            conditions.append('{}.price BETWEEN {} AND {}'.format(Room.table_name, room_price[0], room_price[1]))
        if number_of_people:
            conditions.append('{}.number_of_people BETWEEN {} AND {}'.format(Room.table_name, number_of_people[0], number_of_people[1]))
        if hotel_description:
            boolean = "MATCH ({}.description) AGAINST ('".format(Hotel.table_name)
            include = hotel_description.get('+', None)
            if include:
                boolean += "+{} ".format(include)
            exclude = hotel_description.get('+', None)
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
    ref = {CheckIn: 'idclient'}


class Room(BaseModel):
    table_name = 'room'
    columns = {
        'id': 'INT',
        'number_of_people': 'INT',
        'price': 'DOUBLE',
        'is_lux': 'BOOLEAN',
        'idhotel': 'INT'
    }
    ref = {CheckIn: 'idroom'}


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
    ref = {Room: 'idhotel'}

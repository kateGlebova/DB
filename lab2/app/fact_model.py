from app.base_model import BaseModel


class FactModel(BaseModel):
    pass


class CheckIn(FactModel):
    table_name = 'check_in'
    columns = {
        'id': 'INT',
        'date': 'DATE',
        'days': 'INT',
        'total_price': 'DOUBLE',
        'idclient': 'INT',
        'idroom': 'INT'
    }


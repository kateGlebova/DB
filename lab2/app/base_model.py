class BaseModel:
    table_name = ''
    columns = {}
    primary_key = 'id'
    null = []

    def __init__(self, session):
        self.session = session
        self.session.create_table(self)

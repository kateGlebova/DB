from app import connection
from app.models import Client, Hotel, Room, CheckIn
from app.session import Session

db_session = Session(connection.get_connection())
db_session.create_table(Client)
db_session.create_table(Hotel)
db_session.create_table(Room)
db_session.create_table(CheckIn)
# db_session.make_fulltext(Hotel, 'description')


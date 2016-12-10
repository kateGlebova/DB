from app import connection
from app.dimension_models import Client, Hotel, Room
from app.fact_model import CheckIn
from app.session import Session

db_session = Session(connection.get_connection())
client = Client(db_session)
hotel = Hotel(db_session)
room = Room(db_session)
check_in = CheckIn(db_session)
